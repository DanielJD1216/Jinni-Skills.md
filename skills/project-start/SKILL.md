---
name: project-start
description: Creates or refreshes evidence-backed project memory and an operational runbook. Use even when the repo is inherited or messy and goals, architecture, UI rules, code standards, progress, or first-debug steps are stale. Excludes routine docs sync, narrow fixes, and agent-instruction design.
---

# Project Start

## Overview

Use this skill to establish stable AI-readable project truth before implementation. Keep product, architecture, UI, standards, workflow, and progress truth in six context files, and keep first-debug procedures in an operational diagnostic runbook.

This is not a docs audit or a full agent-entrypoint workflow. `$agent-setup` owns complete `AGENTS.md` and `CLAUDE.md` operating instructions. The default output is the six context files plus the diagnostic runbook. Do not create or modify an agent entrypoint unless the user explicitly requests one in the current task.

## Decision Rules

- New product or vague build: create the six files before implementation.
- New project or operationally unclear build: also create `docs/guides/diagnostic-runbook.md`.
- Existing repo with no context files: scaffold first, then fill from repo evidence and user decisions.
- Existing repo with partial context: patch the smallest stale or missing parts, do not rewrite working docs.
- Existing repo with accepted, current context: report that Project Start is not needed and preserve the files.
- Existing repo with runbooks already present: keep the existing convention and patch only missing first-debug details.
- Missing agent entrypoint: leave it missing unless the user explicitly requests a minimal pointer file. A missing `AGENTS.md` or `CLAUDE.md` is not implicit permission to create one.
- Active feature work: read the entrypoint and six files before coding; update `progress-tracker.md` after meaningful implementation changes.
- Handoff, launch, or repo cleanup: pair this with `$docs-audit` for README, setup, runbook, and reference docs.

## Workflow

1. Inspect the target project before writing.
   - Read existing `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`, runbooks, package files, lockfiles, `.env.example`, source folders, tests, CI, deployment config, and task trackers when present.
   - Use repo evidence for commands, stack, boundaries, and implemented behavior. Put unknowns in open questions.
2. Choose the context location.
   - Prefer `context/`.
   - If the project already uses a different context or docs folder for agent memory, keep the existing convention.
   - Prefer `docs/guides/diagnostic-runbook.md` for the operational runbook unless the repo already has a runbook convention.
3. Scaffold only missing files.
   - Use `scripts/scaffold_six_file_context.py` when a clean template pack is useful.
   - Run the scaffolder with its default `--entry none` unless the current user request explicitly names an entrypoint.
   - Do not overwrite existing context files unless the user explicitly asks.
   - Keep `--context-dir` inside the target project. The script rejects absolute paths, parent traversal, control characters, and symlink destinations.
4. Fill or update each file with repo-specific truth.
   - `project-overview.md`: product, user, core flow, goals, features, scope, success criteria.
   - `architecture.md`: stack, system boundaries, storage, auth/access, invariants.
   - `ui-context.md`: visual language, tokens, typography, component library, layout patterns.
   - `code-standards.md`: language, framework, styling, API, data, and file organization rules.
   - `ai-workflow-rules.md`: scoping, missing requirements, protected files, verification rules.
   - `progress-tracker.md`: current phase, current goal, completed, in progress, next up, open questions, decisions, session notes.
5. Fill or update the diagnostic runbook with repo-specific first-debug truth.
   - `docs/guides/diagnostic-runbook.md`: environments, health checks, logs, DB checks, queue checks, provider checks, deployment checks, safe recovery actions, redaction rules, and known failure modes.
   - Keep unknown operational details as explicit placeholders or open questions. Do not invent ports, URLs, commands, credentials, owners, or provider setup.
6. Add or update the entrypoint.
   - Skip this step unless the user explicitly requests a minimal pointer file during scaffolding.
   - Leave complete entrypoint creation and policy to `$agent-setup`.
   - If an entrypoint already exists, preserve it. Do not replace project-specific instructions.
7. For spec-driven builds, add `context/specs/`.
   - Start with `00-build-plan.md` when planning a multi-unit build.
   - Add one spec per unit only when implementation is imminent.
8. Verify before finishing.
   - Check that no secrets, real credentials, production exports, private data, or unsupported claims were added.
   - Confirm unresolved facts are labeled as open questions.
   - Report created files, updated files, skipped existing files, and remaining decisions.

## Scaffold Script

Run from the skill folder:

```bash
python3 scripts/scaffold_six_file_context.py /path/to/project
```

Useful options:

- `--entry agents`: create `AGENTS.md` if the current user request explicitly asks for it.
- `--entry claude`: create `CLAUDE.md` if the current user request explicitly asks for it.
- `--entry both`: create both entrypoints only when the current user request explicitly asks for both.
- `--entry none`: create only context files.
- `--context-dir docs`: place the six files under another directory.
- `--skip-runbook`: scaffold only the six context files and any explicitly requested entrypoint, without `docs/guides/diagnostic-runbook.md`.
- `--dry-run`: show what would be created.
- `--force`: overwrite existing files only when explicitly approved by the user.

The script preflights every destination before writing. It fails without partial output when a destination escapes the project root or is a symlink.

## Resources

- Read `references/methodology.md` for the phase map, file responsibilities, and spec pattern.
- Use `assets/templates/context/project-overview.md`, `assets/templates/context/architecture.md`, `assets/templates/context/ui-context.md`, `assets/templates/context/code-standards.md`, `assets/templates/context/ai-workflow-rules.md`, and `assets/templates/context/progress-tracker.md` as the six context templates.
- Use `assets/templates/docs/guides/diagnostic-runbook.md` for first-debug procedures.
- Use `assets/templates/AGENTS.md` and `assets/templates/CLAUDE.md` only for optional minimal entrypoints.
- Use `scripts/scaffold_six_file_context.py` for safe template installation.
- Run `python3 -m unittest discover -s tests -p 'test_*.py'` after changing the scaffolder; the regression suite lives at `tests/test_scaffold_six_file_context.py`.
- Keep `agents/openai.yaml` aligned with the trigger boundary when changing scope or description metadata.

## Output Standard

- Keep context files specific to the project, not generic methodology notes.
- Prefer short, direct bullets over long essays.
- Distinguish implemented, planned, mocked, blocked, and out of scope work.
- Do not invent architecture, commands, env vars, ownership, security posture, deployment steps, or product readiness.
- Do not create or modify `AGENTS.md`, `CLAUDE.md`, or another agent entrypoint unless the current user request explicitly asks for it.
- When evidence is thin, write the uncertainty into `progress-tracker.md` instead of making a confident claim.
- Report created, updated, skipped, and unresolved items. Creating context does not authorize implementation.
