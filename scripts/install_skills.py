#!/usr/bin/env python3
"""Install selected Jinni Skills without silently overwriting existing work."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import shutil
import sys
import uuid


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
TARGETS = {
    "codex": Path.home() / ".agents" / "skills",
    "claude": Path.home() / ".claude" / "skills",
    "agents": Path.home() / ".agents" / "skills",
    "codex-legacy": Path.home() / ".codex" / "skills",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class InstallError(RuntimeError):
    """A user-facing installation error."""


def frontmatter_name(skill_file: Path) -> str:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise InstallError(f"Missing YAML frontmatter: {skill_file}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise InstallError(f"Unclosed YAML frontmatter: {skill_file}")
    for line in text[4:end].splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip('"\'')
            if NAME_RE.fullmatch(name):
                return name
            raise InstallError(f"Invalid skill name {name!r}: {skill_file}")
    raise InstallError(f"Missing frontmatter name: {skill_file}")


def discover_skills() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for directory in sorted(SKILLS_ROOT.iterdir()):
        skill_file = directory / "SKILL.md"
        if not directory.is_dir() or not skill_file.is_file():
            continue
        name = frontmatter_name(skill_file)
        if name != directory.name:
            raise InstallError(
                f"Directory {directory.name!r} does not match frontmatter name {name!r}"
            )
        found[name] = directory
    if not found:
        raise InstallError("No installable skills were found")
    return found


def resolve_destination(target: str | None, destination: str | None) -> Path:
    if bool(target) == bool(destination):
        raise InstallError("Choose exactly one of --target or --dest")
    raw = TARGETS[target] if target else Path(destination).expanduser()
    return raw.resolve()


def backup_path(target: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate = target.with_name(f"{target.name}.backup-{stamp}")
    counter = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = target.with_name(f"{target.name}.backup-{stamp}-{counter}")
        counter += 1
    return candidate


def install_one(source: Path, destination_root: Path, force: bool, dry_run: bool) -> str:
    target = destination_root / source.name
    if target.is_symlink():
        raise InstallError(f"Refusing to replace symlink destination: {target}")
    if dry_run:
        if target.exists() and not force:
            return f"DRY RUN: blocked by existing skill {target} (use --force to replace safely)"
        action = "replace with backup" if target.exists() else "install"
        return f"DRY RUN: {action} {source.name} -> {target}"
    if target.exists() and not force:
        raise InstallError(f"Already installed: {target}. Use --force to replace it safely.")

    destination_root.mkdir(parents=True, exist_ok=True)
    staging = destination_root / f".{source.name}.tmp-{uuid.uuid4().hex}"
    backup: Path | None = None
    try:
        shutil.copytree(
            source,
            staging,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
        )
        if target.exists():
            backup = backup_path(target)
            target.rename(backup)
        staging.rename(target)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        if backup is not None and backup.exists() and not target.exists():
            backup.rename(target)
        raise

    if backup is not None:
        return f"INSTALLED: {source.name} -> {target} (backup: {backup.name})"
    return f"INSTALLED: {source.name} -> {target}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install Jinni Skills into Codex, Claude Code, or another skill directory."
    )
    location = parser.add_mutually_exclusive_group()
    location.add_argument("--target", choices=sorted(TARGETS))
    location.add_argument("--dest", help="Custom skill directory")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--all", action="store_true", help="Install every published skill")
    selection.add_argument("--list", action="store_true", help="List published skills and exit")
    parser.add_argument("--force", action="store_true", help="Replace existing skills after creating backups")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    parser.add_argument("skills", nargs="*", help="Skill names to install")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        available = discover_skills()
        if args.list:
            if args.skills or args.all or args.target or args.dest:
                raise InstallError("--list cannot be combined with an install selection or destination")
            for name in available:
                print(name)
            return 0

        if args.all and args.skills:
            raise InstallError("Use --all or explicit skill names, not both")
        selected = list(available) if args.all else args.skills
        if not selected:
            raise InstallError("Choose --all or provide at least one skill name")
        unknown = sorted(set(selected) - set(available))
        if unknown:
            raise InstallError(f"Unknown skill: {', '.join(unknown)}")
        destination = resolve_destination(args.target, args.dest)
        for name in selected:
            print(install_one(available[name], destination, args.force, args.dry_run))
        return 0
    except InstallError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    sys.exit(main())
