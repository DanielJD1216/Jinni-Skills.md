from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "scaffold_agent_entrypoint.py"


class ScaffoldAgentEntrypointTests(unittest.TestCase):
    def run_script(self, project: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(project), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_default_creates_agents_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            result = self.run_script(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / "AGENTS.md").is_file())
            self.assertFalse((project / "CLAUDE.md").exists())

    def test_both_target_creates_both_entrypoints(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            result = self.run_script(project, "--target", "both")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / "AGENTS.md").is_file())
            self.assertTrue((project / "CLAUDE.md").is_file())

    def test_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            result = self.run_script(project, "--target", "both", "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("create", result.stdout)
            self.assertEqual(list(project.iterdir()), [])

    def test_existing_file_is_skipped_unless_force_is_set(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            entrypoint = project / "AGENTS.md"
            entrypoint.write_text("keep me", encoding="utf-8")

            skipped = self.run_script(project)
            self.assertEqual(skipped.returncode, 0, skipped.stderr)
            self.assertEqual(entrypoint.read_text(encoding="utf-8"), "keep me")

            forced = self.run_script(project, "--force")
            self.assertEqual(forced.returncode, 0, forced.stderr)
            self.assertNotEqual(entrypoint.read_text(encoding="utf-8"), "keep me")

    def test_custom_context_directory_updates_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir)
            result = self.run_script(project, "--context-dir", "docs/project-context")
            self.assertEqual(result.returncode, 0, result.stderr)
            entrypoint = (project / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("docs/project-context/project-overview.md", entrypoint)
            self.assertNotIn("`context/project-overview.md`", entrypoint)

    def test_rejects_unsafe_context_directories_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "project"
            project.mkdir()
            for unsafe in ("../escaped", str(Path(temp_dir) / "absolute"), "bad\npath"):
                result = self.run_script(project, "--context-dir", unsafe)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(list(project.iterdir()), [])

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_force_refuses_symlink_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project = root / "project"
            project.mkdir()
            outside = root / "outside.md"
            outside.write_text("outside", encoding="utf-8")
            os.symlink(outside, project / "AGENTS.md")

            result = self.run_script(project, "--force")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stderr.lower())
            self.assertEqual(outside.read_text(encoding="utf-8"), "outside")


if __name__ == "__main__":
    unittest.main()
