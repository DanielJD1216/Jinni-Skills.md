from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "install_skills.py"


class InstallSkillsTests(unittest.TestCase):
    def run_installer(
        self, *args: str, home: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        if home is not None:
            environment["HOME"] = home
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=environment,
        )

    def test_list_reports_every_published_skill(self) -> None:
        result = self.run_installer("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "agent-setup",
                "incident-triage",
                "project-flow-router",
                "project-start",
                "understand-before-approve",
            ],
        )

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "skills"
            result = self.run_installer(
                "--dest", str(destination), "--dry-run", "project-start"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("DRY RUN", result.stdout)
            self.assertFalse(destination.exists())

    def test_codex_target_uses_current_agents_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer(
                "--target",
                "codex",
                "--dry-run",
                "project-start",
                home=directory,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(Path(directory) / ".agents" / "skills"), result.stdout)

    def test_legacy_codex_target_remains_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer(
                "--target",
                "codex-legacy",
                "--dry-run",
                "project-start",
                home=directory,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(Path(directory) / ".codex" / "skills"), result.stdout)

    def test_installs_selected_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer(
                "--dest", directory, "incident-triage"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((Path(directory) / "incident-triage" / "SKILL.md").is_file())

    def test_existing_skill_requires_force(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = self.run_installer("--dest", directory, "agent-setup")
            second = self.run_installer("--dest", directory, "agent-setup")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("Already installed", second.stderr)

    def test_dry_run_reports_existing_skill_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(
                self.run_installer("--dest", directory, "agent-setup").returncode,
                0,
            )
            result = self.run_installer(
                "--dest", directory, "--dry-run", "agent-setup"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("blocked by existing skill", result.stdout)

    def test_force_keeps_backup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(
                self.run_installer("--dest", directory, "project-start").returncode,
                0,
            )
            marker = Path(directory) / "project-start" / "local-marker.txt"
            marker.write_text("preserve me", encoding="utf-8")
            result = self.run_installer(
                "--dest", directory, "--force", "project-start"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            backups = list(Path(directory).glob("project-start.backup-*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(
                (backups[0] / "local-marker.txt").read_text(encoding="utf-8"),
                "preserve me",
            )

    def test_unknown_skill_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer("--dest", directory, "not-a-skill")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unknown skill", result.stderr)

    def test_all_installs_five_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_installer("--dest", directory, "--all")
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = sorted(
                path.name for path in Path(directory).iterdir() if path.is_dir()
            )
            self.assertEqual(len(installed), 5)


if __name__ == "__main__":
    unittest.main()
