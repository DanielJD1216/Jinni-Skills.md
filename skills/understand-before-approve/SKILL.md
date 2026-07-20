---
name: understand-before-approve
description: >
  Creates evidence-backed understanding gates before consequential approvals, merges, deployments, sign-offs, migrations, provider setup, product decisions, or release gates. Teaches non-experts with recommended answers or runs a hidden-answer assessment when requested. Use for "what am I approving?", "explain this before I approve", "show me the recommended answers", "quiz me before merge", blind-spot checks, and ship or sign-off readiness. Do not use for ordinary education, generic code review, or trivial questions without a pending decision.
---

# Understand Before Approve

## Purpose

Prevent consequential approval by reflex. Build an accurate model of the proposed change, teach or test the owner's understanding of load-bearing facts at the right level, collect owner judgment separately, and report whether the decision can now be made.

Treat understanding, approval, and execution as three separate states. Passing the comprehension gate never approves, merges, deploys, signs off, or accepts anything.

## Trigger Boundary

Use this skill when a real decision is pending, including:

- code merge or release approval;
- product or client acceptance;
- architecture or migration approval;
- provider access or integration setup;
- production deployment or operational sign-off;
- implicit go/no-go readiness, such as whether a consequential change is ready to ship or proceed;
- data, permission, legal-state, or money-impacting change.

Do not use it for:

- ordinary education without a pending decision;
- generic code review that asks for defects but not approval understanding;
- trivial factual or copy questions;
- hypothetical comparisons with no current owner decision.

## Core Rules

1. Inspect evidence before explaining.
2. Lead with the direct answer and plain English, then provide technical detail.
3. Separate confirmed facts, inferences, unknowns, and stale evidence.
4. Separate objective comprehension questions from owner judgment questions.
5. Default to **Guided mode** when the owner lacks domain knowledge, asks for recommended answers, cannot answer unaided, or specialized language would make a cold quiz performative rather than useful.
6. Use **Assessment mode** only when the owner explicitly wants a hidden-answer quiz or already has enough domain grounding for one.
7. In Guided mode, show recommended factual answers and recommended owner choices with evidence and tradeoffs before asking for confirmation or teach-back. In Assessment mode, keep the answer key hidden until the owner responds.
8. Re-check only failed, disputed, or unconfirmed load-bearing concepts.
9. Never convert guided confirmation or a passing assessment into automatic approval or execution.

## Workflow

### 1. Define the Decision

State the exact proposed action, decision owner, target system or product surface, environment, and consequence. Ask one focused question if the decision boundary is unclear. Hold the gate until the object of approval is specific.

### 2. Set Risk Rigor

Scale the evidence and quiz to the consequence:

- **Low risk:** reversible presentation or copy change with no data, permission, workflow, or external-state effect. Ask 1 to 2 load-bearing questions.
- **Moderate risk:** behavior, workflow, configuration, integration, or user-impact change. Ask 3 to 5 load-bearing questions.
- **High risk:** migration, authentication, provider permission, legal state, money, deletion, production release, client acceptance, or difficult recovery. Ask 5 to 8 load-bearing questions and require direct recovery evidence.

Increase rigor when uncertainty, irreversibility, reach, privilege, or financial impact increases. Do not reduce rigor merely because the change is small in line count.

### 2A. Choose the Comprehension Mode

Choose one mode from the owner's wording and demonstrated familiarity:

- **Guided mode, default for non-experts:** explain each load-bearing fact, show a concise recommended answer, and ask the owner to confirm, amend, or teach it back. Also show a recommended owner choice with its rationale and alternatives. Label recommendations as analysis, never approval.
- **Assessment mode:** ask substantive questions with a hidden evidence-backed key, then grade and correct after the response.

Switch from Assessment to Guided mode immediately when the owner says they cannot answer because of missing domain knowledge. Do not treat unfamiliarity as failure.

### 3. Inspect Evidence

Inspect the strongest available evidence before forming conclusions:

- diffs, changed files, commits, and relevant source;
- tests, CI, runtime state, migration state, and deployment state;
- source requirements, architecture records, provider configuration, and approval lineage;
- UAT notes, screenshots, logs, and acceptance evidence;
- rollback instructions, recovery tests, backups, feature flags, and monitoring.

Record the artifact, environment, freshness, and claim each item supports. If the user supplied a summary, treat it as a claim until supported by direct evidence. Never infer current deployment, provider readiness, sign-off, test success, or rollback viability from nearby facts.

### 4. Classify Claims

Apply one label to every material claim:

- `Confirmed fact`: directly supported by checked evidence.
- `Inference`: follows from confirmed facts but was not directly observed.
- `Unknown`: available evidence does not answer it.
- `Stale evidence`: evidence exists, but its time, environment, revision, or authority may no longer match the decision.

Keep proposed code, merged code, deployed code, runtime state, historical state, and owner acceptance separate. Surface conflicts instead of choosing the convenient version.

### 5. Build the Change Model

Explain:

- what changed and why;
- what did not change, including protected state, old records, and deferred scope;
- dependencies from input through stored state and user-visible behavior;
- affected users, data, permissions, providers, and environments;
- blast radius under success, partial failure, and rollback;
- rollback or recovery steps and any state that rollback cannot undo;
- limitations, evidence gaps, stale facts, and unresolved decisions.

For exact deep links, identify every mutable identifier. Explain the fallback when the target record no longer exists. If no fallback exists, mark exact historical navigation as unresolved and quiz that dependency.

### 6. Explain in Two Layers

Start with the direct answer: state what the owner is actually deciding and the current gate verdict.

Then explain in plain English using concrete cause and effect. Name the user-visible result, protected state, largest dependency, and largest blind spot.

Only then give technical detail. Include field names, state transitions, routes, permissions, versions, migrations, flags, tests, environments, and recovery behavior when relevant.

### 7. Teach or Test, Then Ask for Judgment

In Guided mode, create **Recommended answers** from evidence-backed facts. Pair each answer with a short confirmation or teach-back prompt that tests the consequence, not jargon recall. Permit the owner to adopt the recommended factual model explicitly or amend any item.

In Assessment mode, create a **Comprehension quiz** from facts with objectively correct answers. Use substantive short-answer or scenario questions. Test mechanism, boundary, consequence, dependency, rollback, or evidence limitation. Keep the answer key hidden before the response.

Create **Owner decisions** from choices that have no single technical answer. Ask the owner to choose scope, risk tolerance, timing, provider permission, target environment, historical backfill, fallback behavior, waiver, or acceptance boundary. Do not grade these choices as technically right or wrong.

In Guided mode, add **Recommended owner choices** with evidence, rationale, and the cost of the alternative. The owner must still explicitly adopt or change each choice.

Read `references/contract.md` before composing or grading a gate. Follow its detailed output, quiz, grading, and verdict contract.

### 8. Hold the Gate

End the initial gate with one verdict:

- `NOT READY` when guided confirmations, assessment answers, or owner decisions are pending, or when a load-bearing misunderstanding remains.
- `BLOCKED BY EVIDENCE` when missing, conflicting, or stale evidence prevents a reliable explanation or decision.
- `READY FOR OWNER DECISION` only when load-bearing comprehension passes, owner decisions are explicit, and evidence is sufficient for the owner to choose.

Do not recommend approval, merge, deployment, sign-off, or acceptance while the verdict is `NOT READY` or `BLOCKED BY EVIDENCE`.

### 9. Grade and Correct

After the owner responds:

1. In Assessment mode, grade each answer `Pass`, `Needs correction`, or `Unanswered` against the hidden evidence-backed key.
2. In Guided mode, record each recommended factual answer as `Confirmed`, `Amended`, `Disputed`, or `Pending`; verify amendments against evidence instead of grading domain vocabulary.
3. Explain each failed, disputed, or corrected concept in plain English, including why it changes risk.
4. Re-check only failed, disputed, or unconfirmed load-bearing concepts.
5. Record owner decisions as explicit, pending, delegated, or conflicting with evidence.
6. Recompute the verdict.

In Assessment mode, do not reveal answers to unanswered quiz items unless correcting them after a genuine attempt or the owner explicitly switches to Guided mode. Do not re-check concepts already passed or confirmed.

### 10. Stop at Readiness

When the verdict becomes `READY FOR OWNER DECISION`, state that the owner may now decide. Do not say the change is approved or should be approved. Require a separate explicit instruction before performing any consequential action, and obey all external approval and execution controls.

## Required Output Order

Use these headings in this order:

1. `Direct answer`
2. `Plain-English explanation`
3. `Technical explanation`
4. `Dependency map`
5. `Changed / Not changed`
6. `Proof`
7. `Unknowns / Blind spots`
8. `Recommended answers` in Guided mode, or `Comprehension quiz` in Assessment mode
9. `Comprehension check` in Guided mode only
10. `Owner decisions`
11. `Recommended owner choices` in Guided mode only
12. `Approval readiness`

Adapt depth to risk, but preserve every applicable section for the selected mode. Use `references/contract.md` for section content and grading format.

## Failure Handling

- **No direct evidence:** explain only the proposed behavior, mark material claims unknown, list the artifacts needed, and return `BLOCKED BY EVIDENCE`.
- **Conflicting evidence:** preserve both claims, identify the deciding artifact or owner, and return `BLOCKED BY EVIDENCE`.
- **Stale evidence:** name the stale dimension and verify it when practical; otherwise return `BLOCKED BY EVIDENCE` if freshness is load-bearing.
- **Action already occurred:** explain the actual state without backdating approval. Treat sign-off as a separate current decision.
- **Historical records differ:** separate current behavior from pre-change rows. Treat backfill and historical fallback as separate owner decisions.
- **User asks to skip the quiz:** reduce question count only when the actual risk is low. Do not waive load-bearing comprehension for a consequential decision.
- **Owner lacks domain knowledge or asks for answers:** switch to Guided mode, show the recommended factual model and owner choices, then ask for explicit confirmation or amendment. Do not score unfamiliarity as a failed quiz.
- **Partial answers:** grade what was answered, correct failures, keep missing items pending, and return `NOT READY`.

## Bundled Resources

- Read `references/contract.md` for the detailed output, quiz, grading, and verdict contract.
- Read `examples/generic-inventory-audit.md` for a fictional worked gate with an exact-link dependency and unresolved historical fallback.
- Use `evals/evals.json` to test the fictional inventory gate, its mixed-answer grading turn, a database migration gate, a guided queue-recovery gate, and a near-miss educational prompt.
- Use `evals/trigger-evals.json` to test trigger precision against strong approval language and adjacent non-trigger requests.
- Keep `agents/openai.yaml` as the Codex discovery metadata for this skill.
