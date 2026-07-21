# Project Start Methodology Reference

## Purpose

Project Start uses the Six-File Context Methodology to give an AI coding agent durable project memory. It captures what the product is, how it is built, what rules matter, and where development currently stands.

Use it before and during implementation. Pair the six context files with an operational diagnostic runbook so future incidents start from known environments, health checks, logs, queues, providers, and safe recovery rules. Use docs audit later to verify repository documentation for humans.

## Phase Map

| Phase | Use Project Start For | Main Files |
| --- | --- | --- |
| Idea | Clarify product, user, scope, and success | `project-overview.md` |
| Pre-build | Lock architecture, UI direction, and code rules | `architecture.md`, `ui-context.md`, `code-standards.md` |
| Build | Keep agent work scoped and verifiable | `ai-workflow-rules.md`, `progress-tracker.md` |
| Feature planning | Break work into ordered units | `context/specs/00-build-plan.md` |
| Implementation | Execute one unit at a time | Unit spec plus all six context files |
| Operations and debugging | Make failures diagnosable without guessing | `docs/guides/diagnostic-runbook.md` |
| Resume | Restore state quickly | `progress-tracker.md` |
| Handoff | Prepare for another person or agent | Six files plus docs audit outputs |

## File Responsibilities

### `project-overview.md`

Define product intent: overview, goals, primary user, core flow, features, in scope, out of scope, and success criteria.

### `architecture.md`

Define system truth: stack, folder boundaries, storage model, auth/access model, background jobs, AI flows, external services, and invariants.

### `ui-context.md`

Define visual truth: theme, semantic color tokens, typography, spacing, radius, component library, layout patterns, icons, and responsive rules.

### `code-standards.md`

Define implementation truth: language rules, framework conventions, module boundaries, API/data patterns, validation rules, testing expectations, and file organization.

### `ai-workflow-rules.md`

Define agent execution rules: one unit at a time, when to split work, how to handle missing requirements, protected files, documentation sync, and verification before moving on.

### `progress-tracker.md`

Define current state: phase, current goal, completed work, in-progress work, next steps, open questions, architecture decisions, and session notes.

### `docs/guides/diagnostic-runbook.md`

Define first-debug truth: environments, health checks, logs, dashboards, DB checks, queue checks, external providers, deployment checks, safe commands, dangerous actions, known failure modes, and open operational questions.

This file is not one of the six context files. It is an operational companion used when a build, staging environment, production environment, integration, queue, or provider workflow fails.

## Entrypoint Pattern

Use `AGENTS.md` for Codex and `CLAUDE.md` for Claude Code. For GitHub Copilot and other assistants, preserve the repository's documented convention and verify current official guidance before claiming automatic instruction discovery.

The entrypoint should tell the agent which context files to read before implementation, when to update them, and where to look first during incidents. Keep detailed project facts in the six files and diagnostic runbook, not duplicated in the entrypoint.

## Spec-Driven Build Pattern

For larger builds, add `context/specs/`.

Recommended files:

- `00-build-plan.md`: ordered list of units.
- `NN-feature-name.md`: one buildable unit.

Each unit spec should include:

- Goal: concrete output of this unit.
- Design: layout and interaction details specific to this unit.
- Implementation: component, API, data, or workflow steps.
- Dependencies: packages or services needed for this unit only.
- Verification checklist: exact conditions that prove the unit is done.

## Guardrails

- Do not use blank templates as final documentation.
- Do not duplicate large blocks between `AGENTS.md` and context files.
- Do not let `progress-tracker.md` become a changelog. Keep it focused on current state and resume context.
- Do not let `diagnostic-runbook.md` become a vague troubleshooting essay. Keep it focused on concrete checks, layers, commands, dashboards, and safe recovery boundaries.
- Do not document architecture as implemented unless repo evidence supports it.
- Put unresolved decisions in open questions.
