# Agent Entrypoint Checklist

Use this checklist when creating or auditing `AGENTS.md` or `CLAUDE.md`.

## Required Sections

- Purpose: who the file is for and what it controls.
- Context read order: links to `$project-start` context files.
- Instruction scope: whether the file is global, repo-root, or nested-directory guidance.
- Repo map: major folders and ownership boundaries.
- Commands: install, dev, test, lint, typecheck, build, migration, deploy, and docs commands found in repo evidence.
- Workflow: discovery, plan, implement, verify, report.
- Protected files: generated code, lockfiles, migrations, production config, secrets, security policy, legal files, or other high-risk files.
- Verification gates: what must pass before work is complete.
- Documentation sync: when to update context files or docs.
- Tool policy: when to use `$openai-docs`, browser tools, GitHub tools, design tools, or other project-specific tools.
- Risk policy: when to stop and ask before destructive, expensive, irreversible, or user-visible work.

## Good Entrypoint Rules

- Rules are repo-specific.
- Commands are copied from manifests, scripts, docs, or CI.
- Unknowns are labeled instead of guessed.
- Product and architecture details link to `context/` instead of being repeated.
- Official Codex AGENTS.md behavior is checked against current official OpenAI documentation when creating or materially changing instruction discovery rules.
- OpenAI product or API claims require a current official OpenAI source when accuracy matters.
- Nested `AGENTS.override.md` files are used only when a subdirectory genuinely needs narrower rules.

## Red Flags

- Generic advice that could apply to any repo.
- Commands that do not exist in package scripts, Makefiles, CI, docs, or source comments.
- Claims that the app is production-ready without deployment or acceptance evidence.
- Real secrets, API keys, tokens, provider payloads, financial data, or private customer data.
- Instructions that conflict with existing repo doctrine.
- Large duplicated blocks from context files.
- A large root `AGENTS.md` that should be split into nested guidance.
- A nested `AGENTS.md` ignored because `AGENTS.override.md` exists in the same directory.

## Suggested Structure

```markdown
# AGENTS.md

## Purpose

## Instruction Scope

## Required Read Order

## Repo Map

## Commands

## Workflow

## Protected Files

## Verification

## Documentation Sync

## Tooling Policy

## Risk Rules
```
