---
name: incident-triage
description: Convert unclear or multi-layer bug reports, failed deploys, broken UI states, missing data, webhook failures, queue stalls, extraction failures, auth failures, 4xx/5xx errors, and "nothing is coming in" reports into a strict diagnostic packet before fixing. Use when the failed layer is unknown across local, staging, production, web app, API, worker, integration, data, provider, or deployment surfaces. Prevents premature redeploys, requeues, stale runbook shortcuts, broad edits, and project-specific guessing. Do not use for a deterministic localized defect with a known failing component or a CI-only failure with a dedicated workflow.
---

# Incident Triage

## Purpose

Turn messy failure reports into a 2-minute diagnostic packet that identifies the environment, symptom, failed layer, evidence, next check, and actions to avoid.

## Trigger Boundary

Use this skill when the failed layer is unclear, multiple layers disagree, the environment may matter, or a premature fix could hide evidence or change external state.

Do not use the full incident packet for:

- a deterministic local defect already bounded to one component, test, command, or reproducible code path;
- a CI-only failure with a dedicated CI repair workflow;
- ordinary code review, educational questions, or hypothetical incident planning;
- postmortem writing after the incident facts are already settled.

For those near misses, name the narrower workflow and stop without manufacturing incident uncertainty.

## Workflow

1. Identify the environment: local, staging, production, CI, external provider, or unknown.
2. Restate the user-visible symptom.
3. Classify the likely failed layer using the Layer Taxonomy.
4. Inspect available evidence before asking the user.
5. If the repo has a relevant runbook, read it, verify any shortcut before trusting it, and follow only the parts that still match current evidence.
6. Choose one read-only Two-Minute Check that splits the next branch.
7. Output the Required Triage Format.
8. Only fix after the failed layer is proven or safely bounded.

## Required Triage Format

Use this format unless the user explicitly asks otherwise:

### Direct Answer

One or two sentences. State the most likely layer and whether it is `Proven`, `Likely`, `Unknown`, or `Contradicted`.

### Incident Snapshot

- Environment:
- Severity:
- User-visible symptom:
- First failed layer:
- Confidence:
- Blast radius:
- Last known good:
- Current evidence:
- Evidence quality/currentness:
- Runbook freshness:
- Fix-gate status:
- Unknowns:

### Evidence Ledger

- Source checked:
- Evidence type: `Direct evidence`, `Indirect evidence`, `Missing evidence`, or `Conflicting evidence`
- Currentness marker: command output time, file content checked, provider status time, screenshot/appshot time, or `not verified`
- Conclusion supported:

### Two-Minute Check

The one command, API call, page, log, DB query, queue check, or provider check that will split the next branch.

Expected result:

- If A:
- If B:

### Do Not Do Yet

List actions that would waste time, hide evidence, duplicate work, or create risk.

### Next Action

One concrete step. During triage, execute only read-only checks. Any mutation, deploy, requeue, data repair, credential change, provider-side change, or other action that changes reality requires the Fix Gate plus explicit user approval.

## Evidence Standard

Classify evidence quality:

- `Direct evidence`: observed command output, API response, DB row, log line, test result, screenshot/appshot, current file content, health check, or provider status response.
- `Indirect evidence`: a plausible signal that points toward a layer but does not prove it.
- `Missing evidence`: a required fact is absent.
- `Conflicting evidence`: two sources disagree.

Do not present indirect evidence as proof. If direct evidence is not available, label the conclusion `Likely` or `Unknown`.

Every material conclusion must name the source checked, evidence type, and currentness marker. If currentness cannot be verified, write `not verified` and do not treat the evidence as decisive.

## Severity

Classify severity before mutation:

- `P0`: security issue, payment or wire risk, audit/auth breach risk, data loss, production outage, or irreversible user impact.
- `P1`: staging or production workflow blocked for a critical demo, UAT, live customer, or release.
- `P2`: important broken feature with workaround.
- `P3`: local-only issue, cosmetic issue, unclear report, or low-risk nuisance.

For `P0`, stop before mutation unless the user explicitly approves the recovery action.

## Layer Taxonomy

Use this fixed taxonomy:

1. Browser or local UI state
2. Frontend route, state, rendering, or API client
3. Auth, identity, permissions, or session
4. Backend API route
5. Read model, projection, cache, or dashboard view
6. Database state or migration
7. Inbound provider delivery
8. Inbound event creation or webhook receipt
9. Worker, queue, scheduler, or background job
10. File safety, archive, parser, OCR, extraction, or transformation
11. LLM, classification, state resolution, or decision logic
12. External provider outage, quota, rate limit, or credentials
13. Deployment, infrastructure, DNS, reverse proxy, container health, or secrets
14. Test fixture, synthetic data, stale local data, or stale staging data
15. CI, build, test runner, package manager, typecheck, lint, generated artifact, or asset pipeline

If the layer is unknown, say `unknown` and identify the check that will classify it.

## Local Runbook Rule

If the current repo or workspace contains diagnostic docs, use them as local context before inventing a procedure.

Look for relevant files with names like:

- `AGENTS.md`
- `README.md`
- `docs/**/runbook*.md`
- `docs/**/diagnostic*.md`
- `docs/**/operations*.md`
- `docs/**/incident*.md`
- `docs/**/architecture*.md`
- `docs/**/troubleshoot*.md`

Use only the sections relevant to the current incident. Do not let a project-specific runbook override the universal evidence, freshness, and fix-gate rules in this skill.

## Runbook Freshness Gate

Project runbooks are local context, not guaranteed truth.

Before following a runbook shortcut, verify that the referenced command, script, file, service, route, queue, provider, env var, deployment target, or data source still exists in the current repo or runtime.

Classify runbook freshness:

- `Fresh`: the referenced shortcut matches current repo or runtime evidence.
- `Possibly stale`: the referenced shortcut cannot be verified yet.
- `Stale`: direct evidence shows the referenced shortcut no longer matches the system.
- `Not applicable`: no relevant runbook shortcut was used.

If a shortcut is `Possibly stale`, do not use it as authority. Label it as `Possibly stale runbook evidence` and choose a direct evidence check instead.

If a shortcut is `Stale`, say so explicitly, do not follow it, and add a docs-update task or patch the runbook before closing the incident when docs edits are in scope.

Freshness checks should be quick and read-only. Examples:

- Confirm a referenced script exists in `package.json`, `Makefile`, `justfile`, or repo scripts.
- Confirm a referenced service exists in compose, deployment config, process state, or provider config.
- Confirm a referenced route exists in the current API route files or router.
- Confirm a referenced queue, worker, scheduler, or webhook handler exists in current code or runtime state.
- Confirm a referenced env var exists in config, `.env.example`, deployment secrets references, or docs.
- Compare a claimed architecture path against current folders, deployment files, and recent migrations.

## Scope Change Drift Triggers

Treat diagnostic docs as drift-prone when recent work changed any of these:

- `AGENTS.md`, `README.md`, or `docs/**`
- `package.json` scripts, task runners, or build commands
- Docker, deployment, CI, reverse proxy, DNS, or secrets config
- API route structure, auth/session code, or permission model
- Webhook, provider, queue, worker, scheduler, or background job code
- Database migrations, read models, projections, cache, or dashboard data paths
- Parser, OCR, extraction, file safety, archive, or transformation code
- Env var examples, provider credentials, or integration setup

When a drift trigger appears relevant, verify the runbook shortcut against direct evidence before using it.

## Safety Rules

- Start read-only.
- Do not redeploy before health and deployed-state checks.
- Do not requeue before checking active workers, stuck state, and idempotency.
- Do not perform irreversible, production, destructive, paid, credential-changing, deployment, migration, requeue, data-write, or provider-side actions without explicit user approval, even if the failed layer looks obvious.
- Do not blame local Docker, local cache, or local cleanup for staging or production without evidence.
- Do not assume the frontend is wrong just because the UI shows the symptom.
- Do not assume a provider received something because a user sent it.
- Do not paste secrets, tokens, full payloads, private documents, raw AI responses with private data, screenshots with sensitive values, or payment/wire/banking values.
- Safe evidence includes IDs, timestamps, counts, short status values, safe filenames, redacted error classes, and non-sensitive logs.

## Fix Gate

Do not implement a fix until all four are true:

1. Environment is known or safely irrelevant.
2. Failed layer is `Proven` or tightly `Likely`.
3. The next edit targets that layer only.
4. The verification command or observable success condition is known.

If any item is missing, continue triage instead of editing.

## Missing Information

If information is missing but discoverable, inspect tools, repo docs, logs, DB, screenshot/appshot, runtime state, health checks, or provider status.

If information is missing and not discoverable, ask one question only. Ask the question that unlocks the next branch.

## Fixing

If the user asks to fix the issue, triage first. Fix only after the failed layer is proven or bounded enough that the edit is safe.

When fixing:

1. Make the smallest change that targets the failed layer.
2. Run the known verification check.
3. Report the result using failure-reporting shape if it does not pass.
4. If the fix reveals a different failed layer, stop broad editing and re-triage.
5. If the incident proves a runbook shortcut stale, patch the runbook or create a docs-update task before closing when docs edits are in scope.

## Retrospective Mode

If the user asks why an investigation took too long, use:

### Direct Answer

### Where Time Was Lost

### What We Should Have Checked First

### The New Rule

### Concrete Prevention

## Completion Check

Before ending a triage response, verify:

- The environment is named or explicitly `unknown`.
- The severity and blast radius are named.
- The first failed layer is named or explicitly `unknown`.
- The confidence label is present.
- Runbook freshness is named as `Fresh`, `Possibly stale`, `Stale`, or `Not applicable`.
- Current evidence, unknowns, evidence quality/currentness, and fix-gate status are present.
- The Two-Minute Check is one branch-splitting check.
- The Two-Minute Check includes expected A/B branch results.
- The Do Not Do Yet section prevents at least one likely wasteful or risky action.
- The Next Action is executable.

## Bundled Resources

- Keep `agents/openai.yaml` as optional Codex discovery metadata.
- Use `evals/evals.json` for behavioral checks covering unknown-layer incidents, stale runbooks, near misses, and fix pressure.
- Use `evals/trigger-evals.json` to test trigger precision.
