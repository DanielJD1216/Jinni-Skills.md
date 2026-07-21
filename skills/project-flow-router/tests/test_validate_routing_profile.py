"""Regression tests for the closed Project Flow Router profile contract."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL = SKILL_ROOT / "SKILL.md"
SCRIPT = SKILL_ROOT / "scripts" / "validate_routing_profile.py"
PROFILE = SKILL_ROOT / "references" / "routing-profile.yaml"
SKILL_TEXT = SKILL.read_text(encoding="utf-8")
PROFILE_TEXT = PROFILE.read_text(encoding="utf-8")
_VERSION_TOKEN = r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?"


def required_version(pattern: str, text: str, source: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if match is None:
        raise RuntimeError(f"{source} has no contract version at the required location")
    return match.group("version")


_FRONTMATTER_END = SKILL_TEXT.find("\n---\n", 4)
if _FRONTMATTER_END < 0:
    raise RuntimeError("SKILL.md has no closing frontmatter delimiter")
SKILL_VERSION = required_version(
    rf"^\s{{2}}version:\s*[\"'](?P<version>{_VERSION_TOKEN})[\"']\s*$",
    SKILL_TEXT[:_FRONTMATTER_END],
    "SKILL.md metadata",
)
PROFILE_VERSION = required_version(
    rf'^version:\s*["\'](?P<version>{_VERSION_TOKEN})["\']\s*$',
    PROFILE_TEXT,
    "routing-profile.yaml",
)
COMMAND_VERSION = required_version(
    rf"^python3 scripts/validate_routing_profile\.py --expected-version "
    rf"(?P<version>{_VERSION_TOKEN}) references/routing-profile\.yaml$",
    SKILL_TEXT,
    "SKILL.md validator command",
)
EXPECTED_VERSION = SKILL_VERSION
_BROWSER_CONFLICT_LINE = (
    '    conflict_behavior: "If the session location is not established, stop and ask '
    'which browser contains it."\n'
)


class RoutingProfileValidatorTests(unittest.TestCase):
    def run_validator(
        self, path: Path, expected_version: str = EXPECTED_VERSION
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--expected-version",
                expected_version,
                str(path),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def write_profile(self, directory: str, text: str) -> Path:
        path = Path(directory) / "routing-profile.yaml"
        path.write_text(text, encoding="utf-8")
        return path

    def test_current_complete_profile_is_valid(self) -> None:
        result = self.run_validator(PROFILE)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALID routing profile", result.stdout)
        self.assertIn("tier owners", result.stdout)

    def test_contract_version_is_synchronized_across_skill_profile_and_command(
        self,
    ) -> None:
        self.assertEqual(PROFILE_VERSION, SKILL_VERSION)
        self.assertEqual(COMMAND_VERSION, SKILL_VERSION)

    def test_unknown_keys_fail_in_every_closed_mapping(self) -> None:
        cases = (
            (
                "root",
                "\nprofile_end: true\n",
                "\nunexpected_root: true\nprofile_end: true\n",
                "$.unexpected_root: unexpected field",
            ),
            (
                "tier semantics",
                "tier_semantics:\n",
                "tier_semantics:\n  unexpected_tier: true\n",
                "$.tier_semantics.unexpected_tier: unexpected field",
            ),
            (
                "non-candidate owner",
                "  - name: project-flow-router\n",
                "  - name: project-flow-router\n    unexpected_owner: true\n",
                "$.non_candidate_owners[0].unexpected_owner: unexpected field",
            ),
            (
                "automatic owner",
                "  - name: project-start\n",
                "  - name: project-start\n    unexpected_owner: true\n",
                "$.auto_route[0].unexpected_owner: unexpected field",
            ),
            (
                "conditional owner",
                "  - name: taste-skill\n",
                "  - name: taste-skill\n    unexpected_owner: true\n",
                "$.conditional[0].unexpected_owner: unexpected field",
            ),
            (
                "blocked owner",
                "  - name: legacy-project-router\n",
                "  - name: legacy-project-router\n    unexpected_owner: true\n",
                "$.blocked[0].unexpected_owner: unexpected field",
            ),
            (
                "conflict group",
                "  - id: pdf-owner\n",
                "  - id: pdf-owner\n    unexpected_group: true\n",
                "$.unresolved_conflict_groups[0].unexpected_group: unexpected field",
            ),
            (
                "prerequisite rule",
                "  - id: incident-before-local-diagnosis\n",
                "  - id: incident-before-local-diagnosis\n    unexpected_rule: true\n",
                "$.prerequisite_rules[0].unexpected_rule: unexpected field",
            ),
            (
                "active Fabled rules",
                "active_fabled_rules:\n",
                "active_fabled_rules:\n  unexpected_rule: true\n",
                "$.active_fabled_rules.unexpected_rule: unexpected field",
            ),
            (
                "maintenance",
                "maintenance:\n",
                "maintenance:\n  unexpected_rule: true\n",
                "$.maintenance.unexpected_rule: unexpected field",
            ),
        )
        for label, old, new, expected_error in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                text = PROFILE_TEXT.replace(old, new, 1)
                self.assertNotEqual(text, PROFILE_TEXT)
                result = self.run_validator(self.write_profile(directory, text))
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(expected_error, result.stderr)

    def test_only_understand_before_approve_can_be_a_mandatory_gate(self) -> None:
        text = PROFILE_TEXT.replace(
            "  - name: project-start\n",
            "  - name: project-start\n    mandatory_gate: true\n",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn("only 'understand-before-approve' may be a mandatory gate", result.stderr)

    def test_browser_session_owner_requires_conflict_behavior(self) -> None:
        text = PROFILE_TEXT.replace(_BROWSER_CONFLICT_LINE, "", 1)
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn("conflict_behavior: required for browser-session owners", result.stderr)

    def test_browser_session_owners_require_matching_conflict_behavior(self) -> None:
        text = PROFILE_TEXT.replace(
            _BROWSER_CONFLICT_LINE + "\n  - name: playwright",
            '    conflict_behavior: "Choose Chrome automatically."\n\n  - name: playwright',
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn("browser-session owners must use the same conflict_behavior", result.stderr)

    def test_prerequisite_owner_reference_must_resolve(self) -> None:
        text = PROFILE_TEXT.replace(
            "    first_owner: domain-modeling\n",
            "    first_owner: domain-modelling\n",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "owner 'domain-modelling' is not declared in auto_route or conditional",
            result.stderr,
        )

    def test_dynamic_prerequisite_reference_is_rule_specific(self) -> None:
        text = PROFILE_TEXT.replace(
            "    then_owner: diagnose\n",
            '    then_owner: "The fitting domain or release owner."\n',
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "the dynamic owner placeholder is allowed only as then_owner",
            result.stderr,
        )

    def test_owner_names_reject_whitespace_padding(self) -> None:
        text = PROFILE_TEXT.replace(
            "  - name: project-start\n", '  - name: " project-start "\n', 1
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn("expected a canonical owner name", result.stderr)

    def test_tabs_are_rejected_anywhere(self) -> None:
        text = PROFILE_TEXT.replace("status: active", "status:\tactive", 1)
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 2)
        self.assertIn("tabs are not allowed", result.stderr)

    def test_excessive_nesting_fails_closed_without_a_traceback(self) -> None:
        text = "\n".join(
            f"{'  ' * level}level_{level}:" for level in range(66)
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 2)
        self.assertIn("nesting exceeds the 64-level safety limit", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_tail_rule_is_validated_not_ignored(self) -> None:
        text = PROFILE.read_text(encoding="utf-8").replace(
            "generic_active_run_phrase_is_proof: false",
            "generic_active_run_phrase_is_proof: true",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "$.active_fabled_rules.generic_active_run_phrase_is_proof",
            result.stderr,
        )

    def test_duplicate_owner_across_tier_and_conflict_group_fails(self) -> None:
        text = PROFILE.read_text(encoding="utf-8").replace(
            "      - pdf\n      - pdf:pdf",
            "      - project-start\n      - pdf:pdf",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate owner 'project-start'", result.stderr)
        self.assertIn("first declared at $.auto_route[0].name", result.stderr)

    def test_duplicate_yaml_key_fails_closed(self) -> None:
        text = PROFILE.read_text(encoding="utf-8") + "\nstatus: active\n"
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate key 'status'", result.stderr)

    def test_unsupported_yaml_anchor_fails_closed(self) -> None:
        text = PROFILE.read_text(encoding="utf-8").replace(
            "status: active", "status: &status active", 1
        )
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported YAML feature", result.stderr)

    def test_wrong_contract_version_reports_exact_field(self) -> None:
        result = self.run_validator(PROFILE, "0.0.0")
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            f"$.version: expected '0.0.0', got {EXPECTED_VERSION!r}", result.stderr
        )

    def test_missing_profile_end_sentinel_fails(self) -> None:
        text = PROFILE.read_text(encoding="utf-8").replace("\nprofile_end: true\n", "\n", 1)
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn("$.profile_end: required field is missing", result.stderr)

    def test_profile_end_must_be_terminal(self) -> None:
        text = PROFILE.read_text(encoding="utf-8") + "\nunexpected_tail: true\n"
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(self.write_profile(directory, text))
        self.assertEqual(result.returncode, 1)
        self.assertIn("$.profile_end: must be the final root field", result.stderr)

    def test_invalid_expected_version_is_rejected_before_validation(self) -> None:
        result = self.run_validator(PROFILE, "latest")
        self.assertEqual(result.returncode, 2)
        self.assertIn("INVALID expected version", result.stderr)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_symlink_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            link = Path(directory) / "profile-link.yaml"
            link.symlink_to(PROFILE)
            result = self.run_validator(link)
        self.assertEqual(result.returncode, 2)
        self.assertIn("profile path must not be a symlink", result.stderr)

    def test_directory_path_is_rejected_without_opening_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator(Path(directory))
        self.assertEqual(result.returncode, 2)
        self.assertIn("profile path is not a regular file", result.stderr)

    def test_oversized_input_is_rejected_before_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "oversized.yaml"
            path.write_bytes(b"x" * (1_048_576 + 1))
            result = self.run_validator(path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("exceeds the 1048576-byte safety limit", result.stderr)


if __name__ == "__main__":
    unittest.main()
