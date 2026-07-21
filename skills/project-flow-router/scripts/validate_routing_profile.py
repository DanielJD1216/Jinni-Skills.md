#!/usr/bin/env python3
"""Validate the complete Project Flow Router profile on Python 3.9 or newer.

The profile intentionally uses a small YAML subset: indentation-based mappings and
sequences plus quoted or plain scalar values. This parser rejects aliases, anchors,
tags, flow collections, block scalars, duplicate keys, tabs anywhere, excessive
nesting, and malformed indentation. Rejecting unsupported YAML is safer than
partially interpreting it. The validator has no third-party dependencies.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
import os
from dataclasses import dataclass
from pathlib import Path
import re
import stat
import sys
from typing import Any, NoReturn, Optional, Sequence


MAX_PROFILE_BYTES = 1_048_576
MAX_YAML_NESTING_DEPTH = 64
OWNER_SECTIONS = (
    "non_candidate_owners",
    "auto_route",
    "conditional",
    "blocked",
)
_KEY_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*\Z")
_IDENTIFIER_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
_OWNER_RE = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9._-]*(?::[A-Za-z0-9][A-Za-z0-9._-]*)*\Z"
)
_INTEGER_RE = re.compile(r"[-+]?(?:0|[1-9][0-9]*)\Z")
_UNSUPPORTED_PLAIN_RE = re.compile(r"(?:^|\s)[&*!](?:\S|$)")
_VERSION_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?\Z")
_ISO_DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")

ROOT_KEYS = frozenset(
    {
        "schema_version",
        "profile_id",
        "status",
        "version",
        "updated_at",
        "catalog_source",
        "require_valid_live_catalog",
        "default_unlisted",
        "tier_semantics",
        "explicit_owner_precedence",
        "missing_profile_behavior",
        "invalid_profile_behavior",
        "absent_from_live_catalog_behavior",
        "non_candidate_owners",
        "auto_route",
        "conditional",
        "blocked",
        "unresolved_conflict_groups",
        "prerequisite_rules",
        "active_fabled_rules",
        "maintenance",
        "profile_end",
    }
)
TIER_SEMANTIC_KEYS = frozenset(
    {"auto_route", "conditional", "explicit_only", "blocked"}
)
OWNER_ENTRY_KEYS = {
    "non_candidate_owners": frozenset({"name", "reason"}),
    "auto_route": frozenset(
        {"name", "condition", "excludes", "first_stop", "mandatory_gate"}
    ),
    "conditional": frozenset(
        {
            "name",
            "all_conditions",
            "external_action",
            "state_changing",
            "conflict_behavior",
        }
    ),
    "blocked": frozenset({"name", "reason", "replacement_behavior"}),
}
CONFLICT_GROUP_KEYS = frozenset(
    {"id", "owners", "automatic_selection", "resolution"}
)
PREREQUISITE_RULE_KEYS = frozenset(
    {"id", "when", "first_owner", "then_owner", "add_then_only_if"}
)
ACTIVE_FABLED_KEYS = frozenset(
    {
        "proof_required",
        "generic_active_run_phrase_is_proof",
        "select_fabled_downstream",
        "return_only_first_unresolved_downstream_owner",
        "boundary",
    }
)
MAINTENANCE_KEYS = frozenset(
    {
        "review_interval_days",
        "promote_to_auto_route_requires",
        "demote_to_explicit_only_when",
        "block_only_when",
        "delete_only_after",
    }
)
BROWSER_SESSION_OWNERS = frozenset(
    {"browser:control-in-app-browser", "chrome:control-chrome"}
)
DYNAMIC_PREREQUISITE_OWNER = "The fitting domain or release owner."
DYNAMIC_PREREQUISITE_RULE_ID = "comprehension-before-consequential-action"


class ProfileError(ValueError):
    """A safe, user-facing parse or path error."""


@dataclass(frozen=True)
class Token:
    line: int
    indent: int
    text: str


def _strip_comment(raw: str, line_number: int) -> str:
    """Strip a YAML comment while respecting quoted scalar text."""

    quote: Optional[str] = None
    escaped = False
    index = 0
    while index < len(raw):
        char = raw[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = None
        elif quote == "'":
            if char == "'":
                if index + 1 < len(raw) and raw[index + 1] == "'":
                    index += 1
                else:
                    quote = None
        elif char in {'"', "'"}:
            quote = char
        elif char == "#" and (index == 0 or raw[index - 1].isspace()):
            return raw[:index].rstrip()
        index += 1

    if quote is not None:
        raise ProfileError(f"line {line_number}: unterminated quoted scalar")
    return raw.rstrip()


def _tokenize(text: str) -> list[Token]:
    if "\x00" in text:
        raise ProfileError("profile contains a NUL byte")

    tokens: list[Token] = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw:
            raise ProfileError(f"line {line_number}: tabs are not allowed")
        uncommented = _strip_comment(raw, line_number)
        if not uncommented.strip():
            continue
        indent = len(uncommented) - len(uncommented.lstrip(" "))
        if indent % 2:
            raise ProfileError(
                f"line {line_number}: indentation must use multiples of two spaces"
            )
        if indent // 2 > MAX_YAML_NESTING_DEPTH:
            raise ProfileError(
                f"line {line_number}: nesting exceeds the "
                f"{MAX_YAML_NESTING_DEPTH}-level safety limit"
            )
        content = uncommented[indent:]
        if content in {"---", "..."}:
            raise ProfileError(f"line {line_number}: YAML document markers are unsupported")
        tokens.append(Token(line_number, indent, content))
    if not tokens:
        raise ProfileError("profile is empty")
    if tokens[0].indent != 0:
        raise ProfileError(f"line {tokens[0].line}: root content must start at column 1")
    return tokens


def _split_pair(text: str, line_number: int) -> tuple[str, str]:
    quote: Optional[str] = None
    escaped = False
    for index, char in enumerate(text):
        if quote == '"':
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = None
        elif quote == "'":
            if char == "'":
                quote = None
        elif char in {'"', "'"}:
            quote = char
        elif char == ":" and (index + 1 == len(text) or text[index + 1].isspace()):
            key = text[:index].strip()
            value = text[index + 1 :].strip()
            if not _KEY_RE.fullmatch(key):
                raise ProfileError(f"line {line_number}: unsupported mapping key {key!r}")
            return key, value
    raise ProfileError(f"line {line_number}: expected a key-value mapping")


def _parse_scalar(value: str, line_number: int) -> Any:
    if not value:
        raise ProfileError(f"line {line_number}: missing scalar value")
    if value[0] == '"':
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ProfileError(
                f"line {line_number}: invalid double-quoted scalar"
            ) from exc
        if not isinstance(parsed, str):
            raise ProfileError(f"line {line_number}: expected a quoted string")
        return parsed
    if value[0] == "'":
        if len(value) < 2 or value[-1] != "'":
            raise ProfileError(f"line {line_number}: invalid single-quoted scalar")
        return value[1:-1].replace("''", "'")

    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "~"}:
        return None
    if _INTEGER_RE.fullmatch(value):
        return int(value)
    if value[0] in "[{|>" or _UNSUPPORTED_PLAIN_RE.search(value):
        raise ProfileError(
            f"line {line_number}: unsupported YAML feature in plain scalar"
        )
    return value


class StrictYamlParser:
    """Parse only the non-executable YAML subset used by the routing profile."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def parse(self) -> Any:
        value, index = self._parse_block(0, 0)
        if index != len(self.tokens):
            token = self.tokens[index]
            raise ProfileError(f"line {token.line}: unexpected trailing content")
        return value

    def _parse_block(self, index: int, indent: int) -> tuple[Any, int]:
        if index >= len(self.tokens):
            raise ProfileError("unexpected end of profile")
        token = self.tokens[index]
        if token.indent != indent:
            raise ProfileError(
                f"line {token.line}: expected indentation {indent}, got {token.indent}"
            )
        if token.text == "-" or token.text.startswith("- "):
            return self._parse_sequence(index, indent)
        return self._parse_mapping(index, indent)

    def _parse_mapping(
        self,
        index: int,
        indent: int,
        seed: Optional[dict[str, Any]] = None,
    ) -> tuple[dict[str, Any], int]:
        result = {} if seed is None else seed
        while index < len(self.tokens):
            token = self.tokens[index]
            if token.indent < indent:
                break
            if token.indent > indent:
                raise ProfileError(
                    f"line {token.line}: unexpected indentation {token.indent}"
                )
            if token.text == "-" or token.text.startswith("- "):
                break
            key, raw_value = _split_pair(token.text, token.line)
            if key in result:
                raise ProfileError(f"line {token.line}: duplicate key {key!r}")
            index += 1
            if raw_value:
                result[key] = _parse_scalar(raw_value, token.line)
                continue
            if index >= len(self.tokens) or self.tokens[index].indent <= indent:
                raise ProfileError(f"line {token.line}: key {key!r} has no value")
            child = self.tokens[index]
            if child.indent != indent + 2:
                raise ProfileError(
                    f"line {child.line}: nested value for {key!r} must be indented two spaces"
                )
            result[key], index = self._parse_block(index, indent + 2)
        return result, index

    def _parse_sequence(self, index: int, indent: int) -> tuple[list[Any], int]:
        result: list[Any] = []
        while index < len(self.tokens):
            token = self.tokens[index]
            if token.indent < indent:
                break
            if token.indent > indent:
                raise ProfileError(
                    f"line {token.line}: unexpected indentation {token.indent}"
                )
            if not (token.text == "-" or token.text.startswith("- ")):
                break
            raw_item = token.text[1:].strip()
            index += 1
            if not raw_item:
                if index >= len(self.tokens) or self.tokens[index].indent != indent + 2:
                    raise ProfileError(f"line {token.line}: sequence item has no value")
                item, index = self._parse_block(index, indent + 2)
                result.append(item)
                continue

            try:
                key, raw_value = _split_pair(raw_item, token.line)
            except ProfileError:
                result.append(_parse_scalar(raw_item, token.line))
                continue
            if not raw_value:
                raise ProfileError(
                    f"line {token.line}: nested mapping values on sequence markers are unsupported"
                )
            item = {key: _parse_scalar(raw_value, token.line)}
            if index < len(self.tokens) and self.tokens[index].indent == indent + 2:
                item, index = self._parse_mapping(index, indent + 2, item)
            result.append(item)
        return result, index


def _read_regular_file(path: Path) -> str:
    try:
        initial_metadata = os.lstat(path)
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise ProfileError(f"cannot inspect profile path: {detail}") from exc
    if stat.S_ISLNK(initial_metadata.st_mode):
        raise ProfileError("profile path must not be a symlink")
    if not stat.S_ISREG(initial_metadata.st_mode):
        raise ProfileError("profile path is not a regular file")

    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if hasattr(os, "O_NONBLOCK"):
        flags |= os.O_NONBLOCK
    try:
        descriptor = os.open(path, flags)
    except (OSError, ValueError) as exc:
        detail = getattr(exc, "strerror", None) or str(exc)
        raise ProfileError(f"cannot open profile as a regular file: {detail}") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ProfileError("profile path is not a regular file")
        if metadata.st_size > MAX_PROFILE_BYTES:
            raise ProfileError(
                f"profile exceeds the {MAX_PROFILE_BYTES}-byte safety limit"
            )
        chunks: list[bytes] = []
        remaining = MAX_PROFILE_BYTES + 1
        while remaining:
            chunk = os.read(descriptor, min(65_536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        if len(raw) > MAX_PROFILE_BYTES:
            raise ProfileError(f"profile exceeds the {MAX_PROFILE_BYTES}-byte safety limit")
    finally:
        os.close(descriptor)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProfileError("profile is not valid UTF-8") from exc


def load_profile(path: Path) -> dict[str, Any]:
    try:
        parsed = StrictYamlParser(_tokenize(_read_regular_file(path))).parse()
    except RecursionError as exc:
        raise ProfileError(
            f"profile nesting exceeds the {MAX_YAML_NESTING_DEPTH}-level safety limit"
        ) from exc
    if not isinstance(parsed, dict):
        raise ProfileError("profile root must be a mapping")
    return parsed


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _check_allowed_keys(
    value: dict[str, Any], path: str, allowed: frozenset[str], errors: list[str]
) -> None:
    for key in sorted(set(value) - allowed):
        errors.append(f"{path}.{key}: unexpected field")


def _check_identifier(value: Any, path: str, errors: list[str]) -> Optional[str]:
    if not _is_nonempty_string(value):
        errors.append(f"{path}: expected a non-empty identifier")
        return None
    if value != value.strip() or not _IDENTIFIER_RE.fullmatch(value):
        errors.append(
            f"{path}: expected a canonical identifier without whitespace padding"
        )
        return None
    return value


def _check_owner_name(value: Any, path: str, errors: list[str]) -> Optional[str]:
    if not _is_nonempty_string(value):
        errors.append(f"{path}: expected a non-empty owner name")
        return None
    if value != value.strip() or not _OWNER_RE.fullmatch(value):
        errors.append(
            f"{path}: expected a canonical owner name using letters, digits, '.', ':', "
            "'_', or '-' without whitespace padding"
        )
        return None
    return value


def _check_string_list(value: Any, path: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: expected a non-empty list of strings")
        return []
    strings: list[str] = []
    for index, item in enumerate(value):
        if not _is_nonempty_string(item):
            errors.append(f"{path}[{index}]: expected a non-empty string")
        else:
            strings.append(item.strip())
    return strings


def _require_exact(
    profile: dict[str, Any], key: str, expected: Any, errors: list[str]
) -> None:
    if key not in profile:
        errors.append(f"$.{key}: required field is missing")
    elif type(profile[key]) is not type(expected) or profile[key] != expected:
        errors.append(f"$.{key}: expected {expected!r}, got {profile[key]!r}")


def validate_profile(profile: dict[str, Any], expected_version: str) -> list[str]:
    """Return deterministic contract errors for a parsed profile mapping."""

    errors: list[str] = []
    _check_allowed_keys(profile, "$", ROOT_KEYS, errors)
    _require_exact(profile, "schema_version", 1, errors)
    _check_identifier(profile.get("profile_id"), "$.profile_id", errors)
    _require_exact(profile, "status", "active", errors)
    _require_exact(profile, "version", expected_version, errors)
    updated_at = profile.get("updated_at")
    if not isinstance(updated_at, str) or not _ISO_DATE_RE.fullmatch(updated_at):
        errors.append("$.updated_at: expected an ISO calendar date in YYYY-MM-DD form")
    else:
        try:
            date.fromisoformat(updated_at)
        except ValueError:
            errors.append("$.updated_at: expected a valid ISO calendar date")
    _require_exact(profile, "catalog_source", "host_exposed", errors)
    _require_exact(profile, "require_valid_live_catalog", True, errors)
    _require_exact(profile, "default_unlisted", "explicit_only", errors)
    _require_exact(profile, "explicit_owner_precedence", True, errors)
    _require_exact(profile, "missing_profile_behavior", "stop_and_confirm", errors)
    _require_exact(profile, "invalid_profile_behavior", "stop_and_confirm", errors)
    _require_exact(
        profile, "absent_from_live_catalog_behavior", "unavailable_and_stop", errors
    )
    _require_exact(profile, "profile_end", True, errors)
    if profile and next(reversed(profile)) != "profile_end":
        errors.append("$.profile_end: must be the final root field")

    tier_semantics = profile.get("tier_semantics")
    if not isinstance(tier_semantics, dict):
        errors.append("$.tier_semantics: expected a mapping")
    else:
        _check_allowed_keys(tier_semantics, "$.tier_semantics", TIER_SEMANTIC_KEYS, errors)
        for tier in ("auto_route", "conditional", "explicit_only", "blocked"):
            if not _is_nonempty_string(tier_semantics.get(tier)):
                errors.append(f"$.tier_semantics.{tier}: expected a non-empty string")

    sections: dict[str, list[Any]] = {}
    for section in OWNER_SECTIONS:
        value = profile.get(section)
        if not isinstance(value, list):
            errors.append(f"$.{section}: expected a list")
            sections[section] = []
        else:
            sections[section] = value

    seen_owners: dict[str, str] = {}
    routable_owners: set[str] = set()
    browser_conflict_behaviors: dict[str, str] = {}

    def register_owner(name: Any, path: str) -> Optional[str]:
        canonical = _check_owner_name(name, path, errors)
        if canonical is None:
            return None
        previous = seen_owners.get(canonical)
        if previous is not None:
            errors.append(
                f"{path}: duplicate owner {canonical!r}; first declared at {previous}"
            )
        else:
            seen_owners[canonical] = path
        return canonical

    for section, entries in sections.items():
        for index, entry in enumerate(entries):
            base = f"$.{section}[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{base}: expected a mapping")
                continue
            _check_allowed_keys(entry, base, OWNER_ENTRY_KEYS[section], errors)
            name = register_owner(entry.get("name"), f"{base}.name")
            if section == "non_candidate_owners":
                if not _is_nonempty_string(entry.get("reason")):
                    errors.append(f"{base}.reason: expected a non-empty string")
            elif section == "auto_route":
                if not _is_nonempty_string(entry.get("condition")):
                    errors.append(f"{base}.condition: expected a non-empty string")
                if not _is_nonempty_string(entry.get("first_stop")):
                    errors.append(f"{base}.first_stop: expected a non-empty string")
                if "excludes" in entry:
                    _check_string_list(entry["excludes"], f"{base}.excludes", errors)
                if "mandatory_gate" in entry and not isinstance(
                    entry["mandatory_gate"], bool
                ):
                    errors.append(f"{base}.mandatory_gate: expected a boolean")
                elif entry.get("mandatory_gate") is True and name != "understand-before-approve":
                    errors.append(
                        f"{base}.mandatory_gate: only 'understand-before-approve' "
                        "may be a mandatory gate"
                    )
            elif section == "conditional":
                _check_string_list(entry.get("all_conditions"), f"{base}.all_conditions", errors)
                for optional_bool in ("external_action", "state_changing"):
                    if optional_bool in entry and not isinstance(entry[optional_bool], bool):
                        errors.append(f"{base}.{optional_bool}: expected a boolean")
                if "conflict_behavior" in entry and not _is_nonempty_string(
                    entry["conflict_behavior"]
                ):
                    errors.append(f"{base}.conflict_behavior: expected a non-empty string")
                if name in BROWSER_SESSION_OWNERS:
                    conflict_behavior = entry.get("conflict_behavior")
                    if not _is_nonempty_string(conflict_behavior):
                        if "conflict_behavior" not in entry:
                            errors.append(
                                f"{base}.conflict_behavior: required for browser-session owners"
                            )
                    else:
                        browser_conflict_behaviors[name] = conflict_behavior.strip()
            elif section == "blocked":
                if not _is_nonempty_string(entry.get("reason")):
                    errors.append(f"{base}.reason: expected a non-empty string")
                if not _is_nonempty_string(entry.get("replacement_behavior")):
                    errors.append(
                        f"{base}.replacement_behavior: expected a non-empty string"
                    )

            if section in {"auto_route", "conditional"} and name in {
                "project-flow-router",
                "fabled",
            }:
                errors.append(f"{base}.name: {name!r} cannot be a downstream candidate")
            elif section in {"auto_route", "conditional"} and name is not None:
                routable_owners.add(name)

    if len(browser_conflict_behaviors) == len(BROWSER_SESSION_OWNERS):
        if len(set(browser_conflict_behaviors.values())) != 1:
            errors.append(
                "$.conditional: browser-session owners must use the same conflict_behavior"
            )

    for required_non_candidate in ("project-flow-router", "fabled"):
        path = seen_owners.get(required_non_candidate, "")
        if not path.startswith("$.non_candidate_owners["):
            errors.append(
                f"$.non_candidate_owners: missing required owner {required_non_candidate!r}"
            )

    approval_gate = [
        entry
        for entry in sections["auto_route"]
        if isinstance(entry, dict) and entry.get("name") == "understand-before-approve"
    ]
    if len(approval_gate) != 1 or approval_gate[0].get("mandatory_gate") is not True:
        errors.append(
            "$.auto_route: understand-before-approve must appear once with mandatory_gate: true"
        )

    conflict_groups = profile.get("unresolved_conflict_groups")
    if not isinstance(conflict_groups, list):
        errors.append("$.unresolved_conflict_groups: expected a list")
        conflict_groups = []
    seen_group_ids: dict[str, str] = {}
    for index, group in enumerate(conflict_groups):
        base = f"$.unresolved_conflict_groups[{index}]"
        if not isinstance(group, dict):
            errors.append(f"{base}: expected a mapping")
            continue
        _check_allowed_keys(group, base, CONFLICT_GROUP_KEYS, errors)
        group_id = group.get("id")
        canonical_group_id = _check_identifier(group_id, f"{base}.id", errors)
        if canonical_group_id is not None:
            if canonical_group_id in seen_group_ids:
                errors.append(
                    f"{base}.id: duplicate id {canonical_group_id!r}; first declared at "
                    f"{seen_group_ids[canonical_group_id]}"
                )
            else:
                seen_group_ids[canonical_group_id] = f"{base}.id"
        owners = group.get("owners")
        if not isinstance(owners, list) or len(owners) < 2:
            errors.append(f"{base}.owners: expected at least two owner names")
        else:
            for owner_index, owner in enumerate(owners):
                register_owner(owner, f"{base}.owners[{owner_index}]")
        if group.get("automatic_selection") != "disabled":
            errors.append(f"{base}.automatic_selection: expected 'disabled'")
        if not _is_nonempty_string(group.get("resolution")):
            errors.append(f"{base}.resolution: expected a non-empty string")

    prerequisite_rules = profile.get("prerequisite_rules")
    if not isinstance(prerequisite_rules, list):
        errors.append("$.prerequisite_rules: expected a list")
        prerequisite_rules = []
    seen_rule_ids: dict[str, str] = {}
    for index, rule in enumerate(prerequisite_rules):
        base = f"$.prerequisite_rules[{index}]"
        if not isinstance(rule, dict):
            errors.append(f"{base}: expected a mapping")
            continue
        _check_allowed_keys(rule, base, PREREQUISITE_RULE_KEYS, errors)
        rule_id = rule.get("id")
        canonical_rule_id = _check_identifier(rule_id, f"{base}.id", errors)
        if canonical_rule_id is not None:
            if canonical_rule_id in seen_rule_ids:
                errors.append(
                    f"{base}.id: duplicate id {canonical_rule_id!r}; first declared at "
                    f"{seen_rule_ids[canonical_rule_id]}"
                )
            else:
                seen_rule_ids[canonical_rule_id] = f"{base}.id"
        for field in ("when", "first_owner", "then_owner", "add_then_only_if"):
            if not _is_nonempty_string(rule.get(field)):
                errors.append(f"{base}.{field}: expected a non-empty string")
        for field in ("first_owner", "then_owner"):
            reference = rule.get(field)
            if not _is_nonempty_string(reference):
                continue
            if reference == DYNAMIC_PREREQUISITE_OWNER:
                if (
                    field != "then_owner"
                    or canonical_rule_id != DYNAMIC_PREREQUISITE_RULE_ID
                ):
                    errors.append(
                        f"{base}.{field}: the dynamic owner placeholder is allowed only "
                        f"as then_owner for {DYNAMIC_PREREQUISITE_RULE_ID!r}"
                    )
                continue
            canonical_reference = _check_owner_name(
                reference, f"{base}.{field}", errors
            )
            if canonical_reference is not None and canonical_reference not in routable_owners:
                errors.append(
                    f"{base}.{field}: owner {canonical_reference!r} is not declared in "
                    "auto_route or conditional"
                )

    active_fabled = profile.get("active_fabled_rules")
    if not isinstance(active_fabled, dict):
        errors.append("$.active_fabled_rules: expected a mapping")
    else:
        _check_allowed_keys(
            active_fabled, "$.active_fabled_rules", ACTIVE_FABLED_KEYS, errors
        )
        _check_string_list(
            active_fabled.get("proof_required"),
            "$.active_fabled_rules.proof_required",
            errors,
        )
        expected_fabled = {
            "generic_active_run_phrase_is_proof": False,
            "select_fabled_downstream": False,
            "return_only_first_unresolved_downstream_owner": True,
            "boundary": "compact-handoff",
        }
        for key, expected in expected_fabled.items():
            value = active_fabled.get(key)
            if type(value) is not type(expected) or value != expected:
                errors.append(
                    f"$.active_fabled_rules.{key}: expected {expected!r}, got {value!r}"
                )

    maintenance = profile.get("maintenance")
    if not isinstance(maintenance, dict):
        errors.append("$.maintenance: expected a mapping")
    else:
        _check_allowed_keys(maintenance, "$.maintenance", MAINTENANCE_KEYS, errors)
        interval = maintenance.get("review_interval_days")
        if not _is_integer(interval) or interval <= 0:
            errors.append("$.maintenance.review_interval_days: expected a positive integer")
        for field in (
            "promote_to_auto_route_requires",
            "demote_to_explicit_only_when",
            "block_only_when",
            "delete_only_after",
        ):
            _check_string_list(maintenance.get(field), f"$.maintenance.{field}", errors)

    return errors


def _fail(message: str, exit_code: int) -> NoReturn:
    print(message, file=sys.stderr)
    raise SystemExit(exit_code)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the complete Project Flow Router profile."
    )
    parser.add_argument("profile", type=Path, help="path to routing-profile.yaml")
    parser.add_argument(
        "--expected-version",
        required=True,
        help="exact router contract version expected in the profile",
    )
    args = parser.parse_args(argv)
    if not _VERSION_RE.fullmatch(args.expected_version):
        _fail(
            "INVALID expected version: use a semantic version such as 1.10.0",
            2,
        )

    try:
        profile = load_profile(args.profile)
    except ProfileError as exc:
        _fail(f"INVALID routing profile: {exc}", 2)

    errors = validate_profile(profile, args.expected_version)
    if errors:
        print(f"INVALID routing profile: {args.profile}", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    owner_count = sum(
        len(profile[section])
        for section in OWNER_SECTIONS
        if isinstance(profile.get(section), list)
    )
    conflict_count = sum(
        len(group.get("owners", []))
        for group in profile.get("unresolved_conflict_groups", [])
        if isinstance(group, dict) and isinstance(group.get("owners"), list)
    )
    print(
        f"VALID routing profile: {args.profile} "
        f"({owner_count} tier owners, {conflict_count} conflict owners)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
