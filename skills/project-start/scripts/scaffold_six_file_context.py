#!/usr/bin/env python3
"""Safely scaffold Six-File Context templates into a project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "templates"

CONTEXT_FILES = [
    "project-overview.md",
    "architecture.md",
    "ui-context.md",
    "code-standards.md",
    "ai-workflow-rules.md",
    "progress-tracker.md",
]

RUNBOOK_FILES = [
    ("docs/guides/diagnostic-runbook.md", "docs/guides/diagnostic-runbook.md"),
]


def relative_directory(value: str) -> Path:
    """Return a safe project-relative directory from a command-line value."""
    if not value or any(ord(char) < 32 for char in value):
        raise argparse.ArgumentTypeError("context directory must be a non-empty path without control characters")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise argparse.ArgumentTypeError("context directory must stay inside the project root")
    return path


def safe_destination(project_root: Path, relative: Path) -> Path:
    """Resolve a destination and reject project-root escapes or symlinks."""
    destination = project_root / relative
    if destination.is_symlink():
        raise SystemExit(f"Refusing symlink destination: {destination}")
    resolved = destination.resolve(strict=False)
    try:
        resolved.relative_to(project_root)
    except ValueError as exc:
        raise SystemExit(f"Destination escapes project root: {destination}") from exc
    return destination


def render_template(src: Path, context_dir: Path) -> str:
    text = src.read_text(encoding="utf-8")
    if src.name not in {"AGENTS.md", "CLAUDE.md"} or context_dir == Path("context"):
        return text
    prefix = "" if context_dir == Path(".") else f"{context_dir.as_posix().rstrip('/')}/"
    return text.replace("context/", prefix)


def copy_file(
    src: Path,
    dest: Path,
    *,
    context_dir: Path,
    force: bool,
    dry_run: bool,
) -> str:
    if not src.is_file() or src.is_symlink():
        raise SystemExit(f"Template is missing or unsafe: {src}")
    if dest.exists() and not force:
        return f"skip existing {dest}"
    action = "overwrite" if dest.exists() else "create"
    if dry_run:
        return f"{action} {dest}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.name in {"AGENTS.md", "CLAUDE.md"}:
        dest.write_text(render_template(src, context_dir), encoding="utf-8")
    else:
        shutil.copyfile(src, dest)
    return f"{action} {dest}"


def entry_files(entry: str) -> list[str]:
    if entry == "none":
        return []
    if entry == "agents":
        return ["AGENTS.md"]
    if entry == "claude":
        return ["CLAUDE.md"]
    if entry == "both":
        return ["AGENTS.md", "CLAUDE.md"]
    raise ValueError(f"Unsupported entry value: {entry}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", help="Target project root")
    parser.add_argument(
        "--context-dir",
        type=relative_directory,
        default=Path("context"),
        help="Context directory relative to project root. Default: context",
    )
    parser.add_argument(
        "--entry",
        choices=["agents", "claude", "both", "none"],
        default="none",
        help="Entrypoint file to create if missing. Default: none",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files. Use only with explicit approval.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files.",
    )
    parser.add_argument(
        "--skip-runbook",
        action="store_true",
        help="Do not create docs/guides/diagnostic-runbook.md.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        raise SystemExit(f"Project root does not exist: {project_root}")
    if not project_root.is_dir():
        raise SystemExit(f"Project root is not a directory: {project_root}")

    operations: list[tuple[Path, Path]] = []
    for name in CONTEXT_FILES:
        src = TEMPLATE_DIR / "context" / name
        dest = safe_destination(project_root, args.context_dir / name)
        operations.append((src, dest))

    if not args.skip_runbook:
        for src_name, dest_name in RUNBOOK_FILES:
            src = TEMPLATE_DIR / src_name
            dest = safe_destination(project_root, Path(dest_name))
            operations.append((src, dest))

    for name in entry_files(args.entry):
        src = TEMPLATE_DIR / name
        dest = safe_destination(project_root, Path(name))
        operations.append((src, dest))

    for src, _ in operations:
        if not src.is_file() or src.is_symlink():
            raise SystemExit(f"Template is missing or unsafe: {src}")

    for src, dest in operations:
        line = copy_file(
            src,
            dest,
            context_dir=args.context_dir,
            force=args.force,
            dry_run=args.dry_run,
        )
        print(line)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
