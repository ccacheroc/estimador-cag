"""Behavioral tests for the provider-neutral skill-creator core."""

from __future__ import annotations

import sys
import importlib.util
from pathlib import Path

import pytest

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from scripts import aggregate_benchmark, improve_description, quick_validate, run_eval  # noqa: E402


def _load_review_module() -> object:
    module_path = SKILL_ROOT / "eval-viewer" / "generate_review.py"
    spec = importlib.util.spec_from_file_location("generate_review", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_runner(path: Path) -> None:
    path.write_text(
        """import json
import sys

request = json.load(sys.stdin)
if request["operation"] == "evaluate_trigger":
    print(json.dumps({"triggered": "portable" in request["query"]}))
elif request["operation"] == "generate_text":
    print(json.dumps({"text": "Use when creating portable skills."}))
else:
    raise SystemExit(2)
"""
    )


def test_trigger_evaluation_uses_provider_neutral_runner_protocol(
    tmp_path: Path,
) -> None:
    runner_path = tmp_path / "runner.py"
    _write_runner(runner_path)

    triggered = run_eval.run_single_query(
        query="Create a portable coding-agent skill",
        skill_name="example-skill",
        skill_description="Use when creating portable skills.",
        timeout=5,
        skill_path=str(tmp_path / "example-skill"),
        runner_command=[sys.executable, str(runner_path)],
        model="test-model",
    )

    assert triggered is True


def test_description_improvement_uses_same_runner_protocol(tmp_path: Path) -> None:
    runner_path = tmp_path / "runner.py"
    _write_runner(runner_path)

    response = improve_description.call_model(
        prompt="Improve this description",
        model="test-model",
        runner_command=[sys.executable, str(runner_path)],
        timeout=5,
    )

    assert response == "Use when creating portable skills."


def test_project_root_uses_portable_repository_markers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = tmp_path / "repository"
    nested = repository / "src" / "package"
    nested.mkdir(parents=True)
    (repository / "AGENTS.md").write_text("# Agent instructions\n")
    (repository / ".harness").mkdir()
    (repository / ".harness" / "manifest.yaml").write_text("schema_version: '1.0'\n")
    monkeypatch.chdir(nested)

    assert run_eval.find_project_root() == repository


def test_canonical_skill_instructions_do_not_name_a_provider() -> None:
    content = (SKILL_ROOT / "SKILL.md").read_text().lower()
    provider_terms = (
        "claude",
        "codex",
        "cursor",
        "copilot",
        "antigravity",
        "cowork",
    )

    assert not any(term in content for term in provider_terms)


def test_runner_output_must_be_valid_json(tmp_path: Path) -> None:
    runner_path = tmp_path / "invalid_runner.py"
    runner_path.write_text("print('not-json')\n")

    with pytest.raises(RuntimeError, match="valid JSON"):
        run_eval.run_single_query(
            query="Create a portable skill",
            skill_name="example-skill",
            skill_description="Use when creating portable skills.",
            timeout=5,
            skill_path=str(tmp_path / "example-skill"),
            runner_command=[sys.executable, str(runner_path)],
        )


def test_runner_errors_cannot_pass_negative_evals(tmp_path: Path) -> None:
    runner_path = tmp_path / "failing_runner.py"
    runner_path.write_text("raise SystemExit(3)\n")
    results = run_eval.run_eval(
        eval_set=[{"id": "negative", "query": "near miss", "should_trigger": False}],
        skill_name="example-skill",
        description="Use when creating portable skills.",
        num_workers=1,
        timeout=5,
        skill_path=tmp_path / "example-skill",
        runner_command=[sys.executable, str(runner_path)],
    )

    result = results["results"][0]
    assert result["pass"] is False
    assert result["errors"] == 1


def test_viewer_escapes_script_block_breakout() -> None:
    review_module = _load_review_module()
    payload = "</script><script>alert('unsafe')</script>"
    html = review_module.generate_html(
        [{"id": "run", "prompt": payload, "outputs": [], "grading": None}],
        "example-skill",
    )

    assert payload not in html
    assert "\\u003c/script\\u003e" in html


def test_portable_validator_requires_directory_name_match(tmp_path: Path) -> None:
    skill_path = tmp_path / "actual-name"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text(
        "---\nname: different-name\ndescription: Use when testing.\n---\n"
    )

    valid, message = quick_validate.validate_skill(skill_path, portable=True)

    assert valid is False
    assert "must match directory" in message


def test_benchmark_delta_is_candidate_minus_baseline_regardless_of_order() -> None:
    summary = aggregate_benchmark.aggregate_results(
        {
            "baseline": [{"pass_rate": 0.25, "time_seconds": None, "tokens": None}],
            "candidate": [{"pass_rate": 0.75, "time_seconds": None, "tokens": None}],
        }
    )

    assert summary["delta"]["pass_rate"] == "+0.50"
    assert summary["delta"]["time_seconds"] is None
    assert summary["delta"]["tokens"] is None
