---
name: agent-setup
description: Creates or refreshes evidence-backed agent instructions. Use even when asked only for AGENTS.md, an agent entrypoint, verified commands, protected files, completion gates, nested overrides, or risk rules. Excludes project-context creation, feature work, and unsafe instruction rewrites.
---

# Agent Setup

## Overview

Use this skill to create the repo-level operating manual for coding agents. `AGENTS.md` or `CLAUDE.md` should tell the agent how to work, while `$project-start` context files tell the agent what the product is and how it is built.

This is not the same as `$project-start` or `$docs-audit`. Agent Setup links accepted project truth to safe implementation behavior. If project context is missing or materially stale, route that gap to `$project-start` instead of inventing it.

## Sequence Fit

Use this in the normal project sequence:

1. `$project-start`: create project memory and six context files.
2. `$grill-me`: pressure-test unclear product, scope, architecture, and execution assumptions.
3. `$agent-setup`: create or refresh `AGENTS.md` and/or `CLAUDE.md`.
4. Implementation: build from context and specs.
5. `$docs-audit`: regularly verify human-facing docs and repo handoff docs.

## Workflow

1. Inspect the repo before writing.
   - Read existing `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/`, `.windsurf/rules/`, `context/`, `README.md`, `docs/`, package files, lockfiles, scripts, tests, CI, Docker, env examples, and deployment config when present.
   - Do not infer commands, architecture, or providers from convention alone.
2. Choose the entrypoint target.
   - Use `AGENTS.md` for Codex.
   - Use `CLAUDE.md` when the repo is primarily used with Claude Code.
   - Preserve other assistants' documented instruction files. Do not claim they automatically discover `AGENTS.md` unless their current official documentation confirms it.
   - If multiple entrypoints exist, keep shared policy aligned through concise links instead of duplicated blocks.
3. Apply official AGENTS.md discovery rules.
   - If `$openai-docs` is available, use it to refresh current official guidance before creating or materially changing Codex instruction discovery rules. Otherwise consult the official OpenAI source identified in `references/openai-agents-md-guide.md`.
   - Codex reads global guidance from `~/.codex/AGENTS.override.md` if present, otherwise `~/.codex/AGENTS.md`.
   - Codex then reads project guidance from the project root down to the current working directory.
   - In each directory, `AGENTS.override.md` wins over `AGENTS.md`; Codex includes at most one instruction file per directory.
   - Guidance closer to the current working directory appears later and can override broader guidance.
   - Keep instruction files small; split specialized rules into nested directories when needed.
4. Preserve existing repo-specific rules.
   - Add missing sections and links.
   - Do not replace mature project doctrine unless it is stale and the user approved the rewrite.
5. Link to project context.
   - Point agents to the six `$project-start` files before implementation.
   - Keep product, architecture, UI, code standards, workflow, and progress truth in `context/`, not repeated in the entrypoint.
   - If required context is absent or contradicted by the repo, record the gap and route it to `$project-start`.
6. Capture execution rules.
   - Required read order.
   - Repo commands for install, dev, test, lint, typecheck, build, migration, and deploy when supported by repo evidence.
   - Protected files and high-risk operations.
   - Verification gates before marking work done.
   - Branch, PR, commit, and deployment rules when known.
7. Add docs lookup policy.
   - Use current official OpenAI documentation for Codex instruction discovery, overrides, fallback filenames, verification commands, and OpenAI product claims.
   - Prefer a host-provided official docs integration when one exists. Do not require a Codex-only skill in entrypoints intended for other assistants.
   - Use repo evidence, not OpenAI docs, for generic project workflow rules.
8. Verify before finishing.
   - Confirm no secrets, private data, real `.env` values, production exports, or unsupported claims were added.
   - Confirm every command came from repo evidence or is labeled as missing.
   - If possible, verify instruction discovery with the official Codex command pattern from the current OpenAI guide.
   - Report created files, updated files, skipped files, and unresolved decisions.

## Scaffold Script

Run from the skill folder:

```bash
python3 scripts/scaffold_agent_entrypoint.py /path/to/project --target agents
```

Useful options:

- `--target agents`: create `AGENTS.md` if missing.
- `--target claude`: create `CLAUDE.md` if missing.
- `--target both`: create both if missing.
- `--context-dir context`: set the context folder name.
- `--dry-run`: show planned changes.
- `--force`: overwrite existing files only with explicit user approval.

The script preflights every destination before writing. It rejects unsafe context paths and symlink destinations, and it preserves existing files unless `--force` is supplied.

## Resources

- Read `references/entrypoint-checklist.md` when reviewing or creating a complete entrypoint.
- Read `references/openai-agents-md-guide.md` when you need the current official AGENTS.md discovery model captured from OpenAI docs.
- Use `assets/templates/AGENTS.md` for a Codex entrypoint and `assets/templates/CLAUDE.md` for a Claude Code entrypoint.
- Use `scripts/scaffold_agent_entrypoint.py` for safe initial file creation.
- Run `python3 -m unittest discover -s tests -p 'test_*.py'` after changing the scaffolder; the regression suite lives at `tests/test_scaffold_agent_entrypoint.py`.
- Keep `agents/openai.yaml` aligned with the trigger boundary when changing scope or description metadata.

## Output Standard

- Keep the entrypoint short enough for agents to read every session.
- Prefer links to context files over duplicated facts.
- Distinguish rules, commands, and open questions.
- Make irreversible or user-visible actions require explicit permission.
- Make verification concrete: exact commands when known, exact gaps when unknown.
- Report created, updated, skipped, and unresolved items. Preparing instructions does not authorize implementation.
