#!/usr/bin/env python3
"""Validate the portable Agent Skills core without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.utils import parse_skill_md

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PROVIDER_FRONTMATTER_KEYS = {
    "agent",
    "background",
    "context",
    "disable-model-invocation",
    "effort",
    "hooks",
    "model",
    "paths",
    "shell",
    "user-invocable",
    "when_to_use",
}


def _frontmatter_keys(content: str) -> set[str]:
    """Extract top-level frontmatter keys from a valid skill document."""
    lines = content.splitlines()
    closing = next(
        (index for index, line in enumerate(lines[1:], start=1) if line == "---"),
        None,
    )
    if closing is None:
        return set()
    keys: set[str] = set()
    for line in lines[1:closing]:
        if line and not line[0].isspace() and ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def _broken_relative_links(skill_path: Path, content: str) -> list[str]:
    """Return missing local Markdown references from SKILL.md."""
    broken: list[str] = []
    for target in MARKDOWN_LINK_PATTERN.findall(content):
        clean_target = target.split("#", 1)[0].strip()
        if not clean_target or "://" in clean_target or clean_target.startswith("#"):
            continue
        path = Path(clean_target)
        if path.is_absolute() or not (skill_path / path).exists():
            broken.append(target)
    return broken


def validate_skill(skill_path: str | Path, portable: bool = False) -> tuple[bool, str]:
    """Validate required metadata, naming and optional portability constraints."""
    path = Path(skill_path).resolve()
    skill_file = path / "SKILL.md"
    if not skill_file.is_file():
        return False, "SKILL.md not found"

    try:
        name, description, content = parse_skill_md(path)
    except (OSError, ValueError) as error:
        return False, str(error)

    if not name:
        return False, "Name must be a non-empty string"
    if not NAME_PATTERN.fullmatch(name):
        return False, "Name must use lowercase letters, digits, and single hyphens"
    if len(name) > 64:
        return False, "Name must not exceed 64 characters"
    if name != path.name:
        return False, f"Name '{name}' must match directory '{path.name}'"

    if not description:
        return False, "Description must be a non-empty string"
    if len(description) > 1024:
        return False, "Description must not exceed 1024 characters"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets"

    broken_links = _broken_relative_links(path, content)
    if broken_links:
        return False, f"Broken or non-portable local links: {', '.join(broken_links)}"

    if portable:
        unsupported = sorted(_frontmatter_keys(content) & PROVIDER_FRONTMATTER_KEYS)
        if unsupported:
            return False, (
                "Provider-specific frontmatter is not portable: "
                + ", ".join(unsupported)
            )

    return True, "Skill is structurally valid and portable" if portable else "Skill is valid"


def main() -> None:
    """Validate one skill directory."""
    parser = argparse.ArgumentParser(description="Validate an Agent Skill")
    parser.add_argument("skill_directory", type=Path)
    parser.add_argument("--portable", action="store_true")
    args = parser.parse_args()
    valid, message = validate_skill(args.skill_directory, portable=args.portable)
    print(message)
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()
