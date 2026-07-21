# Incident Triage

## Plain English

Use this skill when something important is broken but the failed layer is unclear. It investigates before anyone redeploys, requeues work, edits data, rotates credentials, or guesses at a fix.

The goal is not to fix everything immediately. The goal is to prove where the failure starts and identify the smallest safe next action.

## When To Use It

- missing data with no proven failed layer;
- broken staging or production behavior;
- webhook, queue, worker, provider, authentication, and deployment incidents;
- conflicting evidence across UI, API, database, infrastructure, and external services;
- runbooks whose shortcuts may be stale.

## When Not To Use It

- a small deterministic bug with a known failing function;
- a localized test failure with a clear stack trace;
- routine CI repair where the failed command and cause are already known;
- preventive code review without an active incident.

## What It Produces

- the user-visible symptom and affected environment;
- the first proven or most tightly bounded failed layer;
- evidence checked and evidence still missing;
- safe read-only checks;
- actions that must not happen yet;
- the next decision or narrowly scoped diagnostic action.

## Example

The report says, "Customer emails are not appearing." Instead of immediately changing the parser, the skill checks provider delivery, authentication, API receipt, database state, queue progress, and extraction in that order. It returns the first failed layer and a diagnostic packet before any fix begins.

## Install

Place the `incident-triage` directory in the skill directory used by your coding assistant.

- Codex: `~/.codex/skills/incident-triage/`
- Claude Code: `~/.claude/skills/incident-triage/`
- Other Agent Skills compatible tools: use the documented user or project skill directory.

Keep the directory name and the `name` field in `SKILL.md` as `incident-triage`.

## Safety Model

Triage begins read-only. The skill separates diagnosis from mutation and requires a proven or tightly bounded failed layer, a targeted edit, and a known verification check before fixing. Production changes and other consequential actions still require explicit user approval.

Project runbooks are treated as evidence, not permanent truth. Any shortcut that could have drifted must be checked against the current repository or runtime before use.

## Package Contents

- `SKILL.md`: trigger boundary, evidence contract, diagnostic packet, freshness gate, and fix gate
- `agents/openai.yaml`: optional Codex discovery metadata
- `evals/evals.json`: behavioral evaluation cases
- `evals/trigger-evals.json`: trigger and near-miss queries

## License

Released under the MIT License. See `LICENSE`.
