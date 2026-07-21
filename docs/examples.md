# Examples

These examples show the input, useful output shape, and stopping point for every published skill. Exact wording can vary by coding assistant.

## Project Flow Router

**Prompt**

```text
Use project-flow-router. This inherited repository has no current project context, and I want accurate AGENTS.md instructions.
```

**Expected shape**

```text
Router: participated
Owner: project-start -> agent-setup
Reason: Current project truth is required before accurate repository instructions.
Preference effect: prerequisite-sequence
Boundary: route-only
First stop: Current project truth is established.
```

The router stops at the first meaningful gate. It does not claim both workflows already ran.

## Project Start

**Prompt**

```text
Use project-start on this inherited TypeScript service. Build durable context from repository evidence. Leave unknown deployment and ownership facts unresolved.
```

**Expected result**

```text
context/project-overview.md
context/architecture.md
context/ui-context.md
context/code-standards.md
context/ai-workflow-rules.md
context/progress-tracker.md
docs/guides/diagnostic-runbook.md
```

The documents distinguish verified facts, accepted decisions, and open questions. The skill does not invent production readiness.

## Agent Setup

**Prompt**

```text
Use agent-setup. The project context is accepted. Create AGENTS.md with only verified commands and explicit protected-file boundaries.
```

**Expected excerpt**

```text
Read context/project-overview.md and context/architecture.md before changing shared behavior.
Use the package scripts verified in this repository for test, lint, and build.
Do not edit deployment or migration files without explicit authorization.
Completion requires the relevant test and documentation checks to pass.
```

The exact commands must come from current repository evidence.

## Incident Triage

**Prompt**

```text
Use incident-triage. Production stopped receiving webhooks and the queue is empty. Stay read-only until the failed layer is proven.
```

**Expected shape**

```text
Symptom: Provider events do not appear in the application.
Failed layer: Not yet proven.
Evidence checked: Provider delivery, authentication, ingress, persistence, enqueueing, worker progress.
Do not do yet: Redeploy, replay events, rotate credentials, or edit production data.
Next action: Run the smallest read-only check that separates provider delivery from application ingress.
```

The skill localizes before it repairs.

## Understand Before Approve

**Prompt**

```text
Use understand-before-approve before I approve this production database migration.
```

**Expected flow**

1. Explain the change, blast radius, evidence, rollback path, and unresolved risks.
2. Ask a short comprehension check.
3. Grade the answers against the evidence.
4. Return `APPROVED`, `REVISE`, or `ESCALATE`.
5. Keep the verdict separate from permission to execute the migration.

## Fast Path Versus Guarded Path

Use the fast path when the task is localized and reversible:

```text
Fix the failing date formatter test in src/date.ts and run the focused test.
```

Use a guarded skill when the cost of guessing is high:

```text
Use incident-triage. Customer records are missing after yesterday's deploy, and the failed layer is unknown.
```

The collection is meant to reduce expensive mistakes, not add process to every edit.
