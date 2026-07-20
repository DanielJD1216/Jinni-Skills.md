# Understand Before Approve Contract

## Contents

1. Decision model
2. Evidence contract
3. Output contract
4. Quiz contract
5. Grading contract
6. Owner decision contract
7. Readiness contract
8. Risk scaling
9. Edge cases

## 1. Decision Model

Treat a consequential change as a chain:

`proposed action -> implementation -> dependencies -> observed evidence -> owner understanding -> owner judgment -> separate execution`

Each link answers a different question:

- **Proposed action:** What exact action could occur?
- **Implementation:** What mechanism changes behavior or state?
- **Dependencies:** What must remain present, valid, ordered, or authorized?
- **Observed evidence:** What was directly checked, where, and at which revision?
- **Owner understanding:** Can the owner accurately explain the load-bearing facts?
- **Owner judgment:** Which tradeoff or risk does the owner choose?
- **Separate execution:** Has a later explicit instruction authorized the action?

Never collapse these links. Evidence does not prove understanding. Understanding does not choose a tradeoff. A choice does not execute the action.

## 2. Evidence Contract

### Evidence priority

Prefer direct evidence closest to the claimed state:

1. observed runtime, provider, migration, or deployment state;
2. executed tests, CI, UAT, logs, or screenshots tied to a revision and environment;
3. implementation diff and relevant source;
4. source requirements and accepted product or architecture records;
5. summaries, comments, and historical notes.

Use lower-priority evidence when it is the only evidence, but label the confidence loss.

### Evidence record

For each material item, record:

| Field | Required content |
|---|---|
| Evidence | File, diff, commit, test, runtime view, source record, UAT, or log |
| Scope | Claim supported by the item |
| Context | Revision, branch, environment, user role, provider, or date when relevant |
| Status | `Confirmed fact`, `Inference`, `Unknown`, or `Stale evidence` |
| Limit | What the item does not prove |

### Evidence separation

Keep these states separate:

- local change;
- open change request;
- merged change;
- deployed artifact;
- runtime behavior;
- historical data;
- owner acceptance.

Never use one state as proof of another without a verified link.

### Evidence blockers

Return `BLOCKED BY EVIDENCE` when any missing, stale, or conflicting fact prevents an accurate model of:

- the action under consideration;
- protected state;
- irreversible or persistent effects;
- provider or permission readiness;
- migration order or recovery;
- current release or UAT target;
- a load-bearing dependency.

Name the exact artifact or observation needed to unblock the gate.

## 3. Output Contract

### Direct answer

State in one or two sentences:

- what the owner is actually being asked to decide;
- the current verdict;
- the main reason for that verdict.

Do not hide the verdict after technical detail.

### Plain-English explanation

Explain cause and effect without implementation shorthand:

- the problem before the change;
- the behavior after the change;
- the protected or untouched state;
- the main dependency;
- the largest unresolved risk.

Use simple words without removing the mechanism.

### Technical explanation

Describe the implementation path precisely. Include relevant fields, state versions, routes, identifiers, permissions, jobs, migrations, feature flags, tests, environments, and recovery behavior. Place a claim label beside every material statement.

### Dependency map

Show a compact chain such as:

`input -> stored record -> identifier or permission -> service or UI consumer -> observed validation -> owner boundary`

Add branches for asynchronous jobs, external providers, historical records, feature flags, or rollback when they change the outcome.

For a deep link, identify:

- which identifier the URL carries;
- which record lookup consumes it;
- whether the identifier or record is mutable or deletable;
- what the user sees when lookup fails;
- whether historical navigation has a tested fallback.

### Changed / Not changed

Use separate lists. Include code, data, user experience, permissions, operational state, old records, and deferred scope. State non-goals that an owner could reasonably mistake for included work.

### Proof

List checked evidence in the evidence-record format. Include negative evidence, such as a missing test, unavailable provider view, absent backfill, or unverified deployment.

### Unknowns / Blind spots

For each gap, state:

- what is unknown;
- why it matters;
- whether it blocks understanding, owner judgment, or execution;
- the smallest check or decision that resolves it.

### Recommended answers or comprehension quiz

- **Guided mode:** show concise recommended factual answers with evidence labels and consequences. Do not call them approval. Follow with confirmation or teach-back prompts.
- **Assessment mode:** ask only objective questions and keep the hidden answer key out of the initial response.

### Comprehension check

Use in Guided mode. Ask the owner to confirm, amend, dispute, or briefly teach back the load-bearing consequence. Permit an explicit adoption such as "use the recommended factual answers" when every recommendation is visible and separately labeled.

### Owner decisions

Ask only judgment questions. State the available boundary or options and the consequence of leaving each unanswered. In Guided mode, add a recommended choice with evidence, rationale, and the cost of alternatives.

### Approval readiness

Use exactly one allowed verdict and a short reason. Never create a softer synonym.

## 4. Quiz Contract

### Choose Guided or Assessment mode

Use **Guided mode** when the owner says they lack domain knowledge, cannot answer unaided, asks for recommended answers, or would otherwise be tested on specialized vocabulary rather than the real decision. Use **Assessment mode** when the owner explicitly requests a hidden-answer quiz or demonstrates sufficient grounding.

Do not treat Guided mode as weaker evidence. It replaces cold recall with transparent teaching plus explicit confirmation. It still stops before approval and execution.

### Select load-bearing concepts

Quiz a concept only when misunderstanding it could change the decision. Common concepts are:

- the user or operational problem;
- the exact mechanism changed;
- protected or unchanged state;
- dependency and blast radius;
- migration or rollout order;
- rollback versus recovery;
- evidence limitation;
- historical-data behavior;
- provider permission boundary;
- mutable-identifier or deep-link fallback.

### Write substantive questions

Prefer short-answer and scenario forms:

- "Trace the path from the saved event to the screen that displays it."
- "The application rolls back after the migration commits. What state persists, and what must happen next?"
- "The linked record was deleted. What can the deep link still guarantee, and what fallback remains?"
- "Which evidence proves preserved state, and which claim remains unproven?"

Reject these weak forms:

- "Do you understand the change?"
- "Is the migration safe?"
- "Are you comfortable approving?"
- trivia about names or syntax that does not affect the decision.

### Build the answer model

For each question, retain:

- required facts;
- acceptable equivalent wording;
- load-bearing misconception;
- evidence supporting the key;
- whether failure blocks readiness.

In Assessment mode, keep this key hidden before the owner responds and do not embed it in the question.

In Guided mode, turn the key into a short visible **Recommended answer** that includes:

- the minimum load-bearing facts;
- why those facts change the decision;
- the evidence supporting them;
- what remains unknown;
- a confirmation or teach-back prompt.

Recommended answers must simplify language without simplifying the mechanism. Do not ask the owner to guess implementation jargon.

### Keep quiz and judgment separate

An objective question has an answer fixed by evidence. An owner decision permits more than one rational answer after the facts are understood.

Move questions such as "Should old rows be backfilled?" to Owner decisions. Keep questions such as "Were old rows backfilled by this change?" in the comprehension quiz.

## 5. Grading Contract

Grade every answer as:

- `Pass`: captures every load-bearing fact, even with different wording.
- `Needs correction`: omits or contradicts a load-bearing fact.
- `Unanswered`: does not attempt the question or answers a different question.

Use those grades only in Assessment mode. In Guided mode, record each visible recommendation as:

- `Confirmed`: the owner explicitly adopts or accurately teaches back the recommended factual model.
- `Amended`: the owner changes the model and the amendment is supported by evidence.
- `Disputed`: the owner rejects a confirmed fact or proposes an unsupported amendment.
- `Pending`: the owner has not confirmed or amended the recommendation.

Use this response shape after the owner answers:

| Question | Grade | What the answer got right | Correction needed |
|---|---|---|---|

Then provide:

1. `Plain-English corrections` for failed concepts only.
2. `Focused re-quiz` for failed load-bearing concepts only.
3. `Owner decisions status` as explicit, pending, or conflicting.
4. `Approval readiness` with one allowed verdict.

Correct the mechanism, not merely the wording. Explain why the mistake changes risk. Do not re-quiz passed concepts. Do not grade owner judgment as correct or incorrect.

For Guided mode, explain only disputed or unsupported amendments, then ask one focused confirmation. Do not make the owner repeat facts already confirmed.

## 6. Owner Decision Contract

Express each decision as:

- **Decision:** the choice the owner must make;
- **Options or boundary:** the realistic choices supported by evidence;
- **Consequence:** what each choice changes or accepts;
- **Status:** explicit, pending, delegated, or conflicting.

Examples include:

- merge now or wait for missing evidence;
- backfill historical rows or keep scope forward-only;
- accept no historical deep-link fallback or require one;
- choose a provider permission and target resource;
- select rollout timing and rollback threshold;
- accept a known limitation or expand scope.

In Guided mode, present a recommended choice before confirmation when evidence supports one. Label it as analysis, show the alternative and tradeoff, and require the owner to adopt or change it explicitly. In Assessment mode, wait until comprehension passes before recommending a choice. Neither mode converts a recommendation into approval.

## 7. Readiness Contract

Use only these verdicts:

### READY FOR OWNER DECISION

Use when:

- all load-bearing quiz items pass;
- or, in Guided mode, all load-bearing recommended factual answers are confirmed or supported amendments are recorded;
- every owner decision is explicit;
- evidence is sufficient and current for the decision;
- no unresolved conflict prevents a reliable choice.

Meaning: the owner can now choose. It does not mean approved, safe, merged, deployed, accepted, or signed off.

### NOT READY

Use when:

- quiz answers are pending;
- an owner decision is pending;
- a load-bearing misunderstanding remains;
- a focused re-quiz remains.

Meaning: continue the gate. Do not recommend or execute the action.

### BLOCKED BY EVIDENCE

Use when:

- required evidence is missing, conflicting, stale, or tied to the wrong revision or environment;
- the proposed action cannot be described reliably;
- a load-bearing dependency or recovery claim cannot be verified.

Meaning: obtain or reconcile evidence before continuing the decision gate.

## 8. Risk Scaling

| Risk | Evidence depth | Quiz depth | Typical examples |
|---|---|---|---|
| Low | Diff and relevant check | 1 to 2 concepts | Reversible presentation change |
| Moderate | Diff, tests, dependencies, rollback, UAT when relevant | 3 to 5 concepts | Workflow, integration, configuration |
| High | Revision-bound implementation, runtime or deploy state, recovery, permissions, UAT, approval lineage | 5 to 8 concepts | Migration, auth, money, deletion, production, client acceptance |

Raise rigor for broad reach, persistent data, external providers, privilege, legal effect, costly recovery, or uncertain evidence.

## 9. Edge Cases

### Mutable deep-link target

If a deep link uses a record identifier and that record can be deleted, merged, regenerated, or renumbered, distinguish two guarantees:

- current navigation works while the target exists and lookup remains compatible;
- historical navigation requires a fallback when the target no longer exists.

Do not claim exact historical navigation without evidence for the fallback. Quiz this dependency because an owner may otherwise approve a current-state link while assuming permanent audit navigation.

### Migration without symmetric rollback

Distinguish application rollback from data rollback. A reverted application may leave schema or transformed data in place. Require a recovery plan that matches the actual persistence boundary.

### Provider permission mismatch

Do not treat one provider permission as proof of another. Verify the exact scope, account, tenant, target resource, and consent state.

### UAT proves only its path

State the user role, environment, revision, data state, and path covered. Do not generalize one successful UAT path to production deployment, all roles, old records, or failure recovery.

### Evidence arrives after grading

Reclassify affected claims, explain why the label changed, update only dependent quiz items, and recompute the verdict.
