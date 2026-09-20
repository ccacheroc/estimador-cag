#!/usr/bin/env python3
"""Generate an offline-safe trigger-evaluation editor."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.run_eval import _parse_eval_set
from scripts.utils import parse_skill_md


def _safe_json(value: object) -> str:
    """Serialize JSON without allowing script-block termination."""
    return (
        json.dumps(value)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def generate_review(skill_path: Path, eval_set_path: Path, output_path: Path) -> None:
    """Write a standalone review page with safely embedded data."""
    name, description, _ = parse_skill_md(skill_path)
    evals = _parse_eval_set(eval_set_path)
    template = (
        Path(__file__).resolve().parents[1] / "assets" / "eval_review.html"
    ).read_text()
    payload = {
        "skill_name": name,
        "description": description,
        "evals": evals,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        template.replace("/*__EMBEDDED_DATA__*/", _safe_json(payload))
    )


def main() -> None:
    """Generate one review document."""
    parser = argparse.ArgumentParser(description="Generate trigger eval review HTML")
    parser.add_argument("--skill-path", required=True, type=Path)
    parser.add_argument("--eval-set", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    generate_review(
        args.skill_path.resolve(), args.eval_set.resolve(), args.output.resolve()
    )


if __name__ == "__main__":
    main()
