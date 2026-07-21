# AGENTS.md

## Purpose

This file tells AI coding agents how to work in this repository.

## Instruction Scope

This is the repository-root instruction file. Put narrower rules in nested `AGENTS.md` or `AGENTS.override.md` files only when a subdirectory needs different guidance.

## Required Read Order

Before implementation, read:

1. `context/project-overview.md`
2. `context/architecture.md`
3. `context/ui-context.md`
4. `context/code-standards.md`
5. `context/ai-workflow-rules.md`
6. `context/progress-tracker.md`

## Repo Map

- `[folder]`: [responsibility]
- `[folder]`: [responsibility]
- `[folder]`: [responsibility]

## Commands

- Install: `[command or "not found"]`
- Dev: `[command or "not found"]`
- Test: `[command or "not found"]`
- Lint: `[command or "not found"]`
- Typecheck: `[command or "not found"]`
- Build: `[command or "not found"]`

## Workflow

1. Inspect relevant files before editing.
2. Make the smallest useful change that satisfies the task.
3. Update context files when scope, architecture, UI rules, code standards, or progress changes.
4. Run supported verification commands.
5. Report changed files, verification, and unresolved risks.

## Protected Files

Do not modify these without explicit instruction:

- [protected path]
- [protected path]

## Verification

Before marking work complete:

- [ ] Required tests pass, or the blocker is documented.
- [ ] No secrets or private data were added.
- [ ] Context or docs were updated when behavior changed.

## Tooling Policy

- Use a current official OpenAI documentation source before changing Codex AGENTS.md discovery rules or making claims about current OpenAI products, APIs, or Codex behavior.
- Use repo evidence before documenting commands, architecture, deployment, or environment requirements.

## Risk Rules

Ask before destructive, expensive, irreversible, production-facing, or user-visible actions unless the user explicitly requested them.
