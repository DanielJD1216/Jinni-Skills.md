# Incident Triage

`incident-triage` turns unclear operational failures into a strict diagnostic packet before anyone redeploys, requeues, edits data, rotates credentials, or guesses at a fix.

## Use It For

- missing data with no proven failed layer;
- broken staging or production behavior;
- webhook, queue, worker, provider, authentication, and deployment incidents;
- conflicting evidence across UI, API, database, infrastructure, and external services;
- runbooks whose shortcuts may be stale.

Use a narrower diagnostic or CI workflow when the failure is already deterministic and localized.

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
