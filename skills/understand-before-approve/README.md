# Understand Before Approve

## Plain English

Use this skill when someone is about to approve an important change but should first prove they understand what will happen, why it matters, and how it can fail.

The skill explains the decision from evidence, checks the decision-maker's understanding, and returns a verdict. It never treats passing the comprehension check as permission to perform the action.

## When To Use It

- merge and release decisions;
- production deployments and migrations;
- provider permissions and integration setup;
- product or client acceptance;
- architecture decisions with meaningful recovery or security consequences.

## When Not To Use It

- ordinary education with no pending approval;
- generic code review;
- trivial or easily reversible decisions;
- execution that has already been approved and only needs implementation.

## What It Produces

- the decision being considered;
- the evidence that supports the explanation;
- a plain-English explanation of effects, risks, and recovery;
- a short comprehension check;
- grading with misunderstood areas called out;
- an approval verdict that remains separate from execution.

## Example

Before approving a production database migration, the skill explains the schema change, expected downtime, rollback path, and unresolved risks. It then checks the approver's understanding and returns `APPROVED`, `REVISE`, or `ESCALATE`. It does not run the migration.

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
