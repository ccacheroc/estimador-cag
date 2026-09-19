"""Comprueba los componentes obligatorios sin impedir ampliaciones del proyecto."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "app/__init__.py",
    "app/main.py",
    "app/http_errors.py",
    "app/config.py",
    "app/routers/__init__.py",
    "app/routers/estimations.py",
    "app/services/__init__.py",
    "app/services/llm_service.py",
    "app/context/__init__.py",
    "app/context/examples.py",
    "app/schemas/__init__.py",
    "app/schemas/estimation.py",
    "app/schemas/problem.py",
    "app/streamlit_app.py",
    ".harness/rules/technology-standards.md",
    "docs/PRD.md",
    "docs/decisions/ADR-001-fastapi.md",
    "docs/decisions/ADR-002-playwright-e2e.md",
    ".env.example",
    "pyproject.toml",
    "uv.lock",
)


class ProjectStructureTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        for relative_path in REQUIRED_FILES:
            with self.subTest(path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)


if __name__ == "__main__":
    unittest.main()
