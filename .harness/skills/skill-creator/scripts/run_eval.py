#!/usr/bin/env python3
"""Evaluate skill triggering through a provider-neutral runner protocol."""


from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import TypedDict, cast

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.utils import parse_skill_md


class EvalItem(TypedDict):
    """One trigger-evaluation query."""

    id: str
    query: str
    should_trigger: bool


def find_project_root() -> Path:
    """Find the nearest repository root using portable project markers."""
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file():
            return candidate
        if (candidate / ".harness" / "manifest.yaml").is_file():
            return candidate
        if (candidate / ".git").exists():
            return candidate
    return current


def load_runner_command(
    runner_config: Path | None,
    runner_command_json: str | None,
) -> list[str]:
    """Load a shell-free runner command from exactly one source."""
    if bool(runner_config) == bool(runner_command_json):
        raise ValueError(
            "Provide exactly one of --runner-config or --runner-command-json"
        )

    raw: object
    if runner_config is not None:
        parsed = json.loads(runner_config.read_text())
        if not isinstance(parsed, dict):
            raise ValueError("Runner config must be a JSON object")
        raw = parsed.get("command")
    else:
        raw = json.loads(cast(str, runner_command_json))

    if not isinstance(raw, list) or not raw or not all(
        isinstance(argument, str) and argument for argument in raw
    ):
        raise ValueError("Runner command must be a non-empty JSON string array")
    return cast(list[str], raw)


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    skill_path: str,
    runner_command: list[str],
    model: str | None = None,
) -> bool:
    """Return whether an external runner reports that the skill triggered."""
    request = {
        "schema_version": "1.0",
        "operation": "evaluate_trigger",
        "query": query,
        "skill": {
            "name": skill_name,
            "description": skill_description,
            "path": str(Path(skill_path).resolve()),
        },
        "model": model,
    }
    result = subprocess.run(
        runner_command,
        input=json.dumps(request),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        diagnostic = result.stderr.strip() or "no diagnostic output"
        raise RuntimeError(
            f"Runner exited with status {result.returncode}: {diagnostic}"
        )

    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("Runner did not return valid JSON") from error
    if not isinstance(response, dict) or not isinstance(
        response.get("triggered"), bool
    ):
        raise RuntimeError("Runner response must contain boolean 'triggered'")
    return cast(bool, response["triggered"])


def run_eval(
    eval_set: list[EvalItem],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    skill_path: Path,
    runner_command: list[str],
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict[str, object]:
    """Run an evaluation set and aggregate trigger rates by stable ID."""
    trigger_results: dict[str, list[bool | None]] = {
        item["id"]: [] for item in eval_set
    }
    items_by_id = {item["id"]: item for item in eval_set}

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_id = {}
        for item in eval_set:
            for _ in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(skill_path),
                    runner_command,
                    model,
                )
                future_to_id[future] = item["id"]

        for future in as_completed(future_to_id):
            item_id = future_to_id[future]
            try:
                trigger_results[item_id].append(future.result())
            except Exception as error:
                print(f"Warning: eval {item_id} failed: {error}", file=sys.stderr)
                trigger_results[item_id].append(None)

    results: list[dict[str, object]] = []
    for item_id, outcomes in trigger_results.items():
        item = items_by_id[item_id]
        valid = [outcome for outcome in outcomes if outcome is not None]
        errors = len(outcomes) - len(valid)
        trigger_rate = sum(valid) / len(valid) if valid else None
        should_trigger = item["should_trigger"]
        passed = False
        if trigger_rate is not None and errors == 0:
            passed = (
                trigger_rate >= trigger_threshold
                if should_trigger
                else trigger_rate < trigger_threshold
            )
        results.append(
            {
                "id": item_id,
                "query": item["query"],
                "should_trigger": should_trigger,
                "trigger_rate": trigger_rate,
                "triggers": sum(valid),
                "runs": len(valid),
                "errors": errors,
                "pass": passed,
            }
        )

    passed_count = sum(1 for result in results if result["pass"])
    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed_count,
            "failed": len(results) - passed_count,
        },
    }


def _parse_eval_set(path: Path) -> list[EvalItem]:
    """Validate and normalize a trigger evaluation set."""
    raw = json.loads(path.read_text())
    if not isinstance(raw, list) or not raw:
        raise ValueError("Eval set must be a non-empty JSON array")

    items: list[EvalItem] = []
    seen_ids: set[str] = set()
    for index, value in enumerate(raw):
        if not isinstance(value, dict):
            raise ValueError(f"Eval item {index} must be a JSON object")
        item_id = str(value.get("id", index))
        query = value.get("query")
        should_trigger = value.get("should_trigger")
        if item_id in seen_ids:
            raise ValueError(f"Duplicate eval id: {item_id}")
        if not isinstance(query, str) or not query.strip():
            raise ValueError(f"Eval {item_id} requires a non-empty query")
        if not isinstance(should_trigger, bool):
            raise ValueError(f"Eval {item_id} requires boolean should_trigger")
        seen_ids.add(item_id)
        items.append(
            {"id": item_id, "query": query, "should_trigger": should_trigger}
        )
    return items


def main() -> None:
    """Run trigger evaluation from the command line."""
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation through an external runner"
    )
    parser.add_argument("--eval-set", required=True, type=Path)
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--runner-config", type=Path)
    parser.add_argument("--runner-command-json")
    parser.add_argument("--description")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--trigger-threshold", type=float, default=0.5)
    parser.add_argument("--model")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    skill_path = args.skill_path.resolve()
    if not (skill_path / "SKILL.md").exists():
        parser.error(f"No SKILL.md found at {skill_path}")

    try:
        eval_set = _parse_eval_set(args.eval_set)
        runner_command = load_runner_command(
            args.runner_config, args.runner_command_json
        )
    except (json.JSONDecodeError, OSError, ValueError) as error:
        parser.error(str(error))

    name, original_description, _ = parse_skill_md(skill_path)
    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=args.description or original_description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        skill_path=skill_path,
        runner_command=runner_command,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        summary = cast(dict[str, int], output["summary"])
        print(
            f"Results: {summary['passed']}/{summary['total']} passed",
            file=sys.stderr,
        )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
