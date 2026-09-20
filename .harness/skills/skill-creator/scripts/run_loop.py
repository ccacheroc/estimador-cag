#!/usr/bin/env python3
"""Optimize a skill description with held-out trigger evaluations."""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import webbrowser
from pathlib import Path
from typing import cast

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.generate_report import generate_html
from scripts.improve_description import improve_description
from scripts.run_eval import (
    EvalItem,
    _parse_eval_set,
    load_runner_command,
    run_eval,
)
from scripts.utils import parse_skill_md


def split_eval_set(
    eval_set: list[EvalItem], holdout: float, seed: int = 42
) -> tuple[list[EvalItem], list[EvalItem]]:
    """Create a deterministic stratified split without emptying a class."""
    if not 0 <= holdout < 1:
        raise ValueError("holdout must be between 0 (inclusive) and 1 (exclusive)")
    if holdout == 0:
        return list(eval_set), []

    positives = [item for item in eval_set if item["should_trigger"]]
    negatives = [item for item in eval_set if not item["should_trigger"]]
    if len(positives) < 2 or len(negatives) < 2:
        raise ValueError(
            "A holdout split requires at least two positive and two negative evals"
        )

    generator = random.Random(seed)
    generator.shuffle(positives)
    generator.shuffle(negatives)

    def split_group(group: list[EvalItem]) -> tuple[list[EvalItem], list[EvalItem]]:
        test_count = min(len(group) - 1, max(1, round(len(group) * holdout)))
        return group[test_count:], group[:test_count]

    positive_train, positive_test = split_group(positives)
    negative_train, negative_test = split_group(negatives)
    return positive_train + negative_train, positive_test + negative_test


def _subset_results(
    all_results: dict[str, object], item_ids: set[str]
) -> dict[str, object]:
    results = cast(list[dict[str, object]], all_results["results"])
    subset = [result for result in results if result["id"] in item_ids]
    passed = sum(1 for result in subset if result["pass"])
    return {
        "results": subset,
        "summary": {
            "passed": passed,
            "failed": len(subset) - passed,
            "total": len(subset),
        },
    }


def run_loop(
    eval_set: list[EvalItem],
    skill_path: Path,
    runner_command: list[str],
    description_override: str | None,
    num_workers: int,
    timeout: int,
    max_iterations: int,
    runs_per_query: int,
    trigger_threshold: float,
    holdout: float,
    model: str | None,
    verbose: bool,
    live_report_path: Path | None = None,
    log_dir: Path | None = None,
) -> dict[str, object]:
    """Evaluate and improve descriptions, selecting by held-out performance."""
    name, original_description, content = parse_skill_md(skill_path)
    current_description = description_override or original_description
    train_set, test_set = split_eval_set(eval_set, holdout)
    history: list[dict[str, object]] = []
    exit_reason = "unknown"

    for iteration in range(1, max_iterations + 1):
        started_at = time.monotonic()
        all_results = run_eval(
            eval_set=train_set + test_set,
            skill_name=name,
            description=current_description,
            num_workers=num_workers,
            timeout=timeout,
            skill_path=skill_path,
            runner_command=runner_command,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
            model=model,
        )
        train_results = _subset_results(
            all_results, {item["id"] for item in train_set}
        )
        test_results = _subset_results(
            all_results, {item["id"] for item in test_set}
        )
        train_summary = cast(dict[str, int], train_results["summary"])
        test_summary = cast(dict[str, int], test_results["summary"])

        entry: dict[str, object] = {
            "iteration": iteration,
            "description": current_description,
            "train_passed": train_summary["passed"],
            "train_failed": train_summary["failed"],
            "train_total": train_summary["total"],
            "train_results": train_results["results"],
            "test_passed": test_summary["passed"] if test_set else None,
            "test_failed": test_summary["failed"] if test_set else None,
            "test_total": test_summary["total"] if test_set else None,
            "test_results": test_results["results"] if test_set else None,
            "passed": train_summary["passed"],
            "failed": train_summary["failed"],
            "total": train_summary["total"],
            "results": train_results["results"],
        }
        history.append(entry)

        if verbose:
            elapsed = time.monotonic() - started_at
            print(
                f"Iteration {iteration}: train "
                f"{train_summary['passed']}/{train_summary['total']}, test "
                f"{test_summary['passed']}/{test_summary['total']} "
                f"({elapsed:.1f}s)",
                file=sys.stderr,
            )

        if live_report_path is not None:
            partial = {
                "original_description": original_description,
                "best_description": current_description,
                "best_score": "in progress",
                "iterations_run": len(history),
                "holdout": holdout,
                "train_size": len(train_set),
                "test_size": len(test_set),
                "history": history,
            }
            live_report_path.write_text(
                generate_html(partial, auto_refresh=True, skill_name=name)
            )

        train_complete = train_summary["failed"] == 0
        test_complete = not test_set or test_summary["failed"] == 0
        if train_complete and test_complete:
            exit_reason = f"all_passed (iteration {iteration})"
            break
        if iteration == max_iterations:
            exit_reason = f"max_iterations ({max_iterations})"
            break

        blinded_history = [
            {key: value for key, value in item.items() if not key.startswith("test_")}
            for item in history
        ]
        current_description = improve_description(
            skill_name=name,
            skill_content=content,
            current_description=current_description,
            eval_results=train_results,
            history=blinded_history,
            model=model,
            runner_command=runner_command,
            log_dir=log_dir,
            iteration=iteration,
        )

    def rank(item: dict[str, object]) -> tuple[int, int, int]:
        test_passed = item["test_passed"]
        return (
            cast(int, test_passed) if test_passed is not None else -1,
            cast(int, item["train_passed"]),
            -len(cast(str, item["description"])),
        )

    best = max(history, key=rank)
    best_score = (
        f"{best['test_passed']}/{best['test_total']}"
        if test_set
        else f"{best['train_passed']}/{best['train_total']}"
    )
    return {
        "exit_reason": exit_reason,
        "original_description": original_description,
        "best_description": best["description"],
        "best_score": best_score,
        "best_train_score": f"{best['train_passed']}/{best['train_total']}",
        "best_test_score": (
            f"{best['test_passed']}/{best['test_total']}" if test_set else None
        ),
        "final_description": current_description,
        "iterations_run": len(history),
        "holdout": holdout,
        "train_size": len(train_set),
        "test_size": len(test_set),
        "history": history,
    }


def main() -> None:
    """Run the optimization loop from the command line."""
    parser = argparse.ArgumentParser(description="Optimize a skill description")
    parser.add_argument("--eval-set", required=True, type=Path)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--runner-config", type=Path)
    parser.add_argument("--runner-command-json")
    parser.add_argument("--description")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--holdout", type=float, default=0.4)
    parser.add_argument("--model")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--open-report", action="store_true")
    parser.add_argument("--results-dir", type=Path)
    args = parser.parse_args()

    skill_path = args.skill_path.resolve()
    if not (skill_path / "SKILL.md").exists():
        parser.error(f"No SKILL.md found at {skill_path}")
    try:
        eval_set = _parse_eval_set(args.eval_set)
        runner_command = load_runner_command(
            args.runner_config, args.runner_command_json
        )
        split_eval_set(eval_set, args.holdout)
    except (json.JSONDecodeError, OSError, ValueError) as error:
        parser.error(str(error))

    name, _, _ = parse_skill_md(skill_path)
    report_path = args.report.resolve() if args.report else None
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text("<html><body><h1>Starting...</h1></body></html>")
        if args.open_report:
            webbrowser.open(report_path.as_uri())

    results_dir: Path | None = None
    if args.results_dir is not None:
        stamp = time.strftime("%Y-%m-%d_%H%M%S")
        results_dir = args.results_dir / stamp
        results_dir.mkdir(parents=True, exist_ok=True)

    output = run_loop(
        eval_set=eval_set,
        skill_path=skill_path,
        runner_command=runner_command,
        description_override=args.description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        max_iterations=args.max_iterations,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        holdout=args.holdout,
        model=args.model,
        verbose=args.verbose,
        live_report_path=report_path,
        log_dir=results_dir / "logs" if results_dir else None,
    )

    json_output = json.dumps(output, indent=2)
    print(json_output)
    if results_dir is not None:
        (results_dir / "results.json").write_text(json_output)
    if report_path is not None:
        report_path.write_text(generate_html(output, skill_name=name))
    if results_dir is not None:
        (results_dir / "report.html").write_text(
            generate_html(output, skill_name=name)
        )


if __name__ == "__main__":
    main()
