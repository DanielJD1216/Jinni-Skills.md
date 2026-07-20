# Understand Before Approve

`understand-before-approve` creates an evidence-backed understanding gate before a consequential decision. It separates evidence, comprehension, owner judgment, approval, and execution so that a successful explanation or quiz never performs the action being considered.

## Use It For

- merge and release decisions;
- production deployments and migrations;
- provider permissions and integration setup;
- product or client acceptance;
- architecture decisions with meaningful recovery or security consequences.

Do not use it for ordinary education, generic code review, or trivial questions without a pending decision.

## Install

Place this folder in the skill directory used by your coding assistant.

- Codex: `~/.codex/skills/understand-before-approve/`
- Claude Code: `~/.claude/skills/understand-before-approve/`
- Other Agent Skills compatible tools: use that tool's documented user or project skill directory.

Keep the directory name and the `name` field in `SKILL.md` as `understand-before-approve`.

## Contents

- `SKILL.md`: trigger boundary and workflow
- `references/contract.md`: output, evidence, quiz, grading, and verdict contract
- `examples/generic-inventory-audit.md`: fictional worked example
- `evals/evals.json`: behavioral evaluations using fictional or generic scenarios
- `evals/trigger-evals.json`: trigger precision tests
- `agents/openai.yaml`: optional Codex discovery metadata

## Privacy

This distribution contains fictional examples and no required project-specific context. Before redistributing a modified copy, scan it for client names, personal names, internal product terms, URLs, email addresses, local paths, credentials, production identifiers, financial details, and copied logs.

Keep private project examples outside the public skill directory. Other assistants can ignore `agents/openai.yaml` when they do not use Codex metadata.
