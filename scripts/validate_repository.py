#!/usr/bin/env python3
"""Validate the public Jinni Skills repository using reproducible checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
FRONTMATTER_NAME_RE = re.compile(r"^name:\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*$", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN_TEXT = {
    "em dash": "\u2014",
    "macOS local path": "/" + "Users" + "/",
    "Linux home path": "/" + "home" + "/",
    "private key": "BEGIN" + " PRIVATE KEY",
}
GENERATED_NAMES = {".DS_Store"}


class ValidationFailure(RuntimeError):
    """One or more repository checks failed."""


def text_files() -> list[Path]:
    allowed = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
    return [path for path in ROOT.rglob("*") if path.is_file() and path.suffix in allowed]


def validate_skill_structure(errors: list[str]) -> list[Path]:
    skill_dirs = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("No skill directories found")
        return []
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for directory in skill_dirs:
        skill_file = directory / "SKILL.md"
        readme = directory / "README.md"
        if not skill_file.is_file():
            errors.append(f"Missing SKILL.md: {directory.relative_to(ROOT)}")
            continue
        if not readme.is_file():
            errors.append(f"Missing README.md: {directory.relative_to(ROOT)}")
        text = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER_NAME_RE.search(text.split("\n---\n", 1)[0])
        if match is None:
            errors.append(f"Missing or invalid frontmatter name: {skill_file.relative_to(ROOT)}")
        elif match.group(1) != directory.name:
            errors.append(
                f"Skill name mismatch: {directory.name} != {match.group(1)}"
            )
        if f"skills/{directory.name}/" not in root_readme:
            errors.append(f"Root README does not link to {directory.name}")
    return skill_dirs


def validate_json(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")


def validate_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local = target.split("#", 1)[0]
            if local and not (path.parent / local).resolve().exists():
                errors.append(f"Broken link in {path.relative_to(ROOT)}: {target}")


def validate_privacy_and_cleanliness(errors: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        if path.is_file() and (path.name in GENERATED_NAMES or path.suffix == ".pyc"):
            errors.append(f"Generated artifact: {path.relative_to(ROOT)}")
    for path in text_files():
        text = path.read_text(encoding="utf-8")
        for label, token in FORBIDDEN_TEXT.items():
            if token in text:
                errors.append(f"Forbidden {label} in {path.relative_to(ROOT)}")


def run_command(command: list[str], cwd: Path, errors: list[str], label: str) -> None:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        detail = (result.stdout + result.stderr).strip()
        errors.append(f"{label} failed:\n{detail}")


def validate_scripts_and_tests(skill_dirs: list[Path], errors: list[str]) -> None:
    for directory in skill_dirs:
        profile = directory / "references" / "routing-profile.yaml"
        validator = directory / "scripts" / "validate_routing_profile.py"
        if profile.is_file() and validator.is_file():
            version_match = re.search(
                r'^version:\s*["\']([^"\']+)["\']\s*$',
                profile.read_text(encoding="utf-8"),
                flags=re.MULTILINE,
            )
            if version_match is None:
                errors.append(f"{directory.name} profile has no quoted version")
                continue
            run_command(
                [
                    sys.executable,
                    str(validator),
                    "--expected-version",
                    version_match.group(1),
                    str(profile),
                ],
                directory,
                errors,
                f"{directory.name} profile validation",
            )
        tests = directory / "tests"
        if tests.is_dir():
            run_command(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"],
                directory,
                errors,
                f"{directory.name} tests",
            )
    repository_tests = ROOT / "scripts" / "tests"
    if repository_tests.is_dir():
        run_command(
            [sys.executable, "-m", "unittest", "discover", "-s", "scripts/tests", "-p", "test_*.py", "-v"],
            ROOT,
            errors,
            "repository tests",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-tests", action="store_true")
    args = parser.parse_args(argv)
    errors: list[str] = []
    skill_dirs = validate_skill_structure(errors)
    validate_json(errors)
    validate_markdown_links(errors)
    validate_privacy_and_cleanliness(errors)
    if not args.skip_tests:
        validate_scripts_and_tests(skill_dirs, errors)
    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        f"VALID: {len(skill_dirs)} skills, JSON, links, privacy, generated files, scripts, and tests"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
