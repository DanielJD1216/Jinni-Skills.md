# Worked Decision Examples

Use these examples for output shape, not as a static owner catalog. Resolve real owners from a valid live catalog. Stop before specialist execution.

## Contents

- [Clear named owner bypasses router activation](#clear-named-owner-bypasses-router-activation)
- [Router package is a target, not the operating owner](#router-package-is-a-target-not-the-operating-owner)
- [Unlisted inferred owner stops for confirmation](#unlisted-inferred-owner-stops-for-confirmation)
- [Factual Fabled owner-fit question](#factual-fabled-owner-fit-question)
- [Concrete outer lifecycle handoff](#concrete-outer-lifecycle-handoff)
- [Generic active run is not Fabled](#generic-active-run-is-not-fabled)
- [Missing accepted pointer stops before routing](#missing-accepted-pointer-stops-before-routing)
- [Bare invocation does not recover delegation context](#bare-invocation-does-not-recover-delegation-context)
- [Standalone project terminology selects domain modeling](#standalone-project-terminology-selects-domain-modeling)
- [Explicit operational router request with a known owner](#explicit-operational-router-request-with-a-known-owner)
- [Authorized external route remains route-only](#authorized-external-route-remains-route-only)
- [Explicit denial overrides hypothetical authorization](#explicit-denial-overrides-hypothetical-authorization)
- [Active Fabled conditional owner uses its profile tier](#active-fabled-conditional-owner-uses-its-profile-tier)
- [Active Fabled automatic owner uses its profile tier](#active-fabled-automatic-owner-uses-its-profile-tier)
- [Active Fabled recorded unlisted owner uses explicit confirmation](#active-fabled-recorded-unlisted-owner-uses-explicit-confirmation)
- [Failed-quiz explanation is not a live approval gate](#failed-quiz-explanation-is-not-a-live-approval-gate)
- [Consequential quiz routes to comprehension](#consequential-quiz-routes-to-comprehension)
- [Current goal-state routing](#current-goal-state-routing)
- [Browser owner selection is not router inspection](#browser-owner-selection-is-not-router-inspection)
- [Unknown authenticated browser location stops before selection](#unknown-authenticated-browser-location-stops-before-selection)
- [Planning denial stops before issue slicing](#planning-denial-stops-before-issue-slicing)
- [First-owner prerequisite keeps sequence semantics](#first-owner-prerequisite-keeps-sequence-semantics)
- [Blocked profile owner stops](#blocked-profile-owner-stops)
- [Unresolved duplicate family stops](#unresolved-duplicate-family-stops)
- [Missing profile fails closed](#missing-profile-fails-closed)
- [Invalid profile fails closed](#invalid-profile-fails-closed)
- [Profile preference cannot prove availability](#profile-preference-cannot-prove-availability)
- [Next-gate continuation recovers accepted state first](#next-gate-continuation-recovers-accepted-state-first)
- [Inspect-only reason remains prospective](#inspect-only-reason-remains-prospective)
- [Active Fabled with unclear downstream ownership](#active-fabled-with-unclear-downstream-ownership)
- [Invalid catalog fails closed](#invalid-catalog-fails-closed)
- [Unavailable named owner fails closed](#unavailable-named-owner-fails-closed)
- [One target-bound inspection](#one-target-bound-inspection)
- [Authorized bounded local route-record write](#authorized-bounded-local-route-record-write)

## Clear named owner bypasses router activation

**Input:** `Run $domain-modeling on ./checkout to settle Booking versus Order. The valid live catalog exposes domain-modeling.`

```text
Expected host behavior: Load domain-modeling directly and perform its scoped work. Do not load project-flow-router or emit router decision fields.
```

## Router package is a target, not the operating owner

**Input:** `Run $skill-forge on [$project-flow-router](../SKILL.md) to harden its existing package. The valid live catalog exposes skill-forge.`

```text
Router: bypassed
Owner: skill-forge
Reason: The explicit operating owner is skill-forge; the router package is only its named target.
Profile state: valid
Preference effect: explicit-owner
Catalog state: valid-current
Boundary: direct-bypass
Actions: none.
```

## Unlisted inferred owner stops for confirmation

**Input:** `Use $project-flow-router to choose who reviews a proprietary seam in ./app. The valid live catalog exposes only custom-seam-review as a plausible specialist. The active routing profile does not list it.`

```text
Router: participated
Owner: custom-seam-review
Reason: The sole plausible live owner is unlisted and therefore requires explicit confirmation.
Catalog state: valid-current
Profile state: valid
Preference effect: explicit-only-confirm
Boundary: stop-and-confirm
Question: Do you want to invoke custom-seam-review for this target?
Actions: none.
```

## Factual Fabled owner-fit question

**Input:** `A skill lifecycle would create, test on a real target, evaluate outputs, and refine. Is Fabled the correct owner?`

```text
Router: bypassed
Owner: direct-action
Reason: The request is a factual fit question without operational lifecycle authorization.
Profile state: not-required
Preference effect: not-applied
Catalog state: not-consulted
Boundary: direct-bypass
Actions: none.
```

## Concrete outer lifecycle handoff

**Input:** `Build a browser-verification skill, test it on ./sandbox-a and ./sandbox-b, evaluate the outputs, refine it, retest it, and package the stable version. Start the work now.`

```text
Router: bypassed
Owner: fabled
Reason: The authorized creation, real-target testing, evaluation, refinement, retesting, and packaging form a concrete outer lifecycle.
Profile state: valid
Preference effect: not-applied
Catalog state: valid-current
Boundary: compact-handoff
Handoff: Build and stabilize the browser-verification skill against ./sandbox-a and ./sandbox-b; preserve the supplied test and packaging constraints.
Actions: none.
```

The compact handoff does not change the participation decision. An operational outer
Fabled lifecycle always reports `Router: bypassed`.

## Generic active run is not Fabled

**Input:** `The target is accepted in an active run. Use $project-flow-router to inspect the exact accepted-state pointer ./run/_state.md#accepted_gate once. The prompt does not identify Fabled, a Fabled session pin, or Fabled-owned run metadata.`

```text
Router: participated
Owner: project-flow-router
Reason: The exact accepted-state pointer may establish the current gate; generic active-run wording alone cannot establish a lifecycle container.
Profile state: not-required
Preference effect: not-applied
Catalog state: not-consulted
Boundary: inspect-only
Actions: inspected ./run/_state.md#accepted_gate once.
```

## Missing accepted pointer stops before routing

**Input:** `Use $project-flow-router and proceed with the next gate for ./ledger. The target is verified, but no accepted gate or exact authoritative accepted-state pointer is supplied.`

```text
Router: participated
Owner: project-flow-router
Reason: The verified target lacks the one accepted gate or exact pointer required to establish downstream ownership.
Profile state: not-required
Preference effect: not-applied
Catalog state: not-consulted
Boundary: stop-and-confirm
Question: What accepted gate or exact authoritative pointer governs ./ledger?
Actions: none.
```

## Bare invocation does not recover delegation context

**Input:** `A delegation wrapper contains a source task identifier, but the current input is only $project-flow-router.`

```text
Router: participated
Owner: project-flow-router
Reason: No current target or desired routing outcome is supplied.
Profile state: not-required
Preference effect: not-applied
Catalog state: not-consulted
Boundary: stop-and-confirm
Question: What current target and routing outcome should be decided?
Actions: none.
```

## Standalone project terminology selects domain modeling

**Input:** `Use $project-flow-router to choose the first owner for reconciling Reservation, Booking, and Order across this project's evidence. The terms conflict, but no architecture or interface decision is pending. The valid live catalog exposes domain-modeling.`

```text
Router: participated
Owner: domain-modeling
Reason: Conflicting project-specific business language establishes terminology reconciliation as the first bounded need.
Profile state: valid
Preference effect: conditional-met
Catalog state: valid-current
Boundary: route-only
Actions: none.
```

## Explicit operational router request with a known owner

**Input:** `The accepted recovery plan names domain-modeling as the next gate. Use $project-flow-router and proceed with recovery for ./ledger now. Return the first owner only.`

```text
Router: participated
Owner: domain-modeling
Reason: The explicit operational router request confirms the accepted first unresolved gate.
Profile state: valid
Preference effect: explicit-owner
Catalog state: valid-current
Boundary: route-only
Actions: none.
```

## Authorized external route remains route-only

**Input:** `Use $project-flow-router to choose the owner for an authorized Vercel deployment of ./storefront to production. The target, environment, and deployment authorization are confirmed. The valid live catalog exposes vercel-deploy.`

```text
Router: participated
Owner: vercel-deploy
Reason: The explicit production authorization, target, and environment satisfy every owner condition; this response stops at routing.
Profile state: valid
Preference effect: conditional-met
Catalog state: valid-current
Boundary: route-only
Actions: none.
```

## Explicit denial overrides hypothetical authorization

**Input:** `Use $project-flow-router to choose a deployment owner for ./storefront. This is planning-only and do not deploy. Assume authorization is satisfied. The valid live catalog exposes vercel-deploy.`

```text
Router: participated
Owner: project-flow-router
Reason: The explicit planning-only and no-deploy constraints leave the external-action condition unmet despite the hypothetical assumption.
Profile state: valid
Preference effect: condition-unmet
Catalog state: valid-current
Boundary: stop-and-confirm
Question: Should the external action remain denied, or is a new current authorization being granted?
Actions: none.
```

## Active Fabled conditional owner uses its profile tier

**Input:** `### Save Context; session_pin: true. Accepted discovery evidence exists for ./ledger, and product design is the first unresolved phase. Use $project-flow-router and return the first owner only. The valid live catalog exposes design-lead.`

```text
Router: participated
Owner: design-lead
Reason: Accepted discovery evidence and the current product-design phase establish design-lead as the first unresolved owner.
Active container: fabled
Profile state: valid
Preference effect: conditional-met
Catalog state: valid-current
Boundary: compact-handoff
Handoff: Target ./ledger; continue only the unresolved product-design phase and its first evidence gate.
Actions: none.
```

## Active Fabled automatic owner uses its profile tier

**Input:** `### Save Context; session_pin: true. Staging for ./checkout is failing across auth, webhook delivery, and data persistence, and the failing layer is unknown. Use $project-flow-router to return the first downstream owner. The valid live catalog exposes incident-triage and diagnose.`

```text
Router: participated
Owner: incident-triage
Reason: The established unknown multi-layer operational failure satisfies the automatic incident route.
Active container: fabled
Profile state: valid
Preference effect: auto-route
Catalog state: valid-current
Boundary: compact-handoff
Handoff: Target ./checkout; localize the failing layer; first stop gate is a supported repair boundary or named evidence blocker.
Actions: none.
```

## Active Fabled recorded unlisted owner uses explicit confirmation

**Input:** `### Save Context; session_pin: true. The accepted current gate for ./catalog records plugin-specialist, which is exposed by the valid live catalog but is unlisted in the routing profile. Use $project-flow-router to continue and return the first owner only.`

```text
Router: participated
Owner: plugin-specialist
Reason: The accepted current gate explicitly confirms this unlisted live owner.
Active container: fabled
Profile state: valid
Preference effect: explicit-owner
Catalog state: valid-current
Boundary: compact-handoff
Handoff: Target ./catalog; continue only the accepted plugin-specialist gate.
Actions: none.
```

## Failed-quiz explanation is not a live approval gate

**Input:** `I could not answer the quiz. What happens if I failed it?`

```text
Router: bypassed
Owner: direct-action
Reason: This asks for an explanation of the failed result and does not request approval, merge, release, deployment, acceptance, or sign-off.
Profile state: not-required
Preference effect: not-applied
Catalog state: not-consulted
Boundary: direct-bypass
Actions: none.
```

## Consequential quiz routes to comprehension

**Input:** `Explain the release evidence, quiz me, and do not approve deployment until I pass. The valid live catalog exposes understand-before-approve.`

```text
Router: bypassed
Owner: understand-before-approve
Reason: Consequential deployment approval requires the comprehension gate before any release owner.
Profile state: valid
Preference effect: auto-route
Catalog state: valid-current
Boundary: stop-and-confirm
Actions: none.
```

## Current goal-state routing

**Input:** `Use $project-flow-router. We need to revisit the current goal. Where are we now? The valid live catalog exposes project-start for auditing or refreshing project context.`

```text
Router: participated
Owner: project-start
Reason: The requested output is refreshed current project and goal state.
Catalog state: valid-current
Profile state: valid
Preference effect: auto-route
Boundary: route-only
Actions: none.
```

## Browser owner selection is not router inspection

**Input:** `The logged-in session is confirmed in the in-app browser. Use $project-flow-router to choose who inspects the checkout. The valid live catalog exposes browser:control-in-app-browser.`

```text
Router: participated
Owner: browser:control-in-app-browser
Reason: The supplied session location establishes the narrow browser owner; later UI inspection belongs to that owner.
Catalog state: valid-current
Profile state: valid
Preference effect: conditional-met
Boundary: route-only
Actions: none.
```

## Unknown authenticated browser location stops before selection

**Input:** `An existing authenticated payroll session is open, but the prompt does not identify whether it is in the in-app Browser or Chrome. Choose the read-only inspection workflow and stop before browser action. The valid live catalog exposes both browser owners.`

```text
Router: participated
Owner: project-flow-router
Reason: The existing authenticated session location is required to distinguish the live browser owner.
Profile state: valid
Preference effect: condition-unmet
Catalog state: valid-current
Boundary: stop-and-confirm
Question: Is the authenticated session in the in-app Browser or Chrome?
Actions: none.
```

## Planning denial stops before issue slicing

**Input:** `Use $project-flow-router to create implementation issues for ./app. No accepted plan, PRD, or spec exists, and do not create a planning artifact. The valid live catalog exposes to-prd and to-issues.`

```text
Router: participated
Owner: project-flow-router
Reason: Issue slicing requires an accepted planning input, and the request denies the required upstream artifact.
Profile state: valid
Preference effect: condition-unmet
Catalog state: valid-current
Boundary: stop-and-confirm
Question: Provide an accepted plan, PRD, or spec, or authorize the required planning step.
Actions: none.
```

## First-owner prerequisite keeps sequence semantics

**Input:** `Accepted product requirements exist and executable issues are requested, but no accepted PRD, plan, or spec exists. Decide which workflow must happen first, return only that owner, and create nothing. The valid live catalog exposes to-prd and to-issues.`

```text
Router: participated
Owner: to-prd
Reason: Executable issue slicing lacks its required accepted planning input, so the planning workflow is first.
Profile state: valid
Preference effect: prerequisite-sequence
Catalog state: valid-current
Boundary: route-only
Actions: none.
```

## Blocked profile owner stops

**Input:** `Use $project-flow-router to choose the owner for a request that names legacy-project-router. The valid live catalog exposes legacy-project-router. The active profile records legacy-project-router as blocked.`

```text
Router: participated
Owner: project-flow-router
Reason: The requested candidate is blocked by the recorded profile policy, so no alternative owner can be selected without a user decision.
Catalog state: valid-current
Profile state: valid
Preference effect: blocked
Boundary: stop-and-confirm
Question: Do you want to override the recorded block for this request?
Actions: none.
```

## Unresolved duplicate family stops

**Input:** `Use $project-flow-router to choose the CI-only failure owner. The valid live catalog exposes gh-fix-ci and github:gh-fix-ci, and the active profile keeps that duplicate family unresolved.`

```text
Router: participated
Owner: project-flow-router
Reason: The two live CI owners remain an unresolved duplicate family, so neither can be selected silently.
Profile state: valid
Preference effect: unresolved-conflict
Catalog state: valid-current
Boundary: stop-and-confirm
Question: Which CI owner do you want to invoke for this target?
Actions: none.
```

## Missing profile fails closed

**Input:** `Use $project-flow-router to infer who owns the current audit. The live catalog is valid, but references/routing-profile.yaml is missing.`

```text
Router: participated
Owner: project-flow-router
Reason: Inferred selection requires the user-owned preference profile.
Catalog state: valid-current
Profile state: missing
Preference effect: profile-stop
Boundary: stop-and-confirm
Question: Can the active routing profile be restored or explicitly name the operating owner?
Actions: none.
```

## Invalid profile fails closed

**Input:** `Use $project-flow-router to infer the current owner. The live catalog is valid, but the active profile repeats one owner in auto_route and conditional.`

```text
Router: participated
Owner: project-flow-router
Reason: Duplicate profile membership makes preference selection invalid.
Catalog state: valid-current
Profile state: invalid
Profile evidence: duplicate owner membership
Preference effect: profile-stop
Boundary: stop-and-confirm
Question: Can the profile be corrected or explicitly name the operating owner?
Actions: none.
```

## Profile preference cannot prove availability

**Input:** `Use $project-flow-router to route a repository documentation-drift audit. The active profile lists docs-audit, but the valid live catalog does not expose it.`

```text
Router: participated
Owner: unavailable:docs-audit
Reason: Profile preference cannot establish live host availability.
Catalog state: valid-owner-absent
Profile state: valid
Preference effect: auto-route
Boundary: stop-and-confirm
Actions: none.
```

## Next-gate continuation recovers accepted state first

**Input:** `Use $project-flow-router and proceed with the next gate for verified target ./app. I also have several new feature ideas. The accepted gate is not supplied; ./app/TASKS.md is the exact authoritative accepted-state pointer.`

```text
Router: participated
Owner: project-flow-router
Reason: The exact accepted-state pointer may establish the current gate before new initiatives can establish downstream ownership.
Profile state: not-required
Preference effect: not-applied
Catalog state: not-consulted
Boundary: inspect-only
Actions: inspected ./app/TASKS.md once.
```

## Inspect-only reason remains prospective

**Input:** `Use $project-flow-router to audit the current gate for verified target ./refund-engine. Inspect only the exact authoritative pointer ./refund-engine/.project/accepted-state.json once before selecting any downstream owner.`

```text
Router: participated
Owner: project-flow-router
Reason: The exact authoritative pointer may establish the current accepted gate before downstream owner selection.
Profile state: not-required
Preference effect: not-applied
Catalog state: not-consulted
Boundary: inspect-only
Actions: inspected ./refund-engine/.project/accepted-state.json once.
```

For `inspect-only`, keep activity narration out of `Reason`. Put the exact inspection in
`Actions`. Apply the entrypoint's decision-only reason rule without copying action or
completion words from supplied evidence.

## Active Fabled with unclear downstream ownership

**Input:** `### Save Context; session_pin: true. Target: ./checkout. Booking versus Order must be settled before interface design. The valid live catalog exposes domain-modeling and codebase-design. Use $project-flow-router to select the downstream order.`

```text
Router: participated
Owner: domain-modeling
Reason: Accepted terminology is the first unresolved downstream gate.
Active container: fabled
Catalog state: valid-current
Profile state: valid
Preference effect: conditional-met
Boundary: compact-handoff
Handoff: Target ./checkout; first stop gate is accepted terminology.
Actions: none.
```

## Invalid catalog fails closed

**Input:** `Use $project-flow-router on ./app. The live-catalog API returned HTTP 503. Skill source folders exist on disk.`

```text
Router: participated
Owner: project-flow-router
Reason: No authoritative current catalog is available.
Profile state: valid
Preference effect: not-applied
Catalog state: invalid
Catalog evidence: refresh failed, HTTP 503
Boundary: stop-and-confirm
Question: Can the host provide a current successful catalog response?
Actions: none.
```

## Unavailable named owner fails closed

**Input:** `Run $module-architect on ./app. The valid live catalog does not expose module-architect, although its source folder exists.`

```text
Router: bypassed
Owner: unavailable:module-architect
Reason: The named owner is absent from the valid live catalog.
Profile state: valid
Preference effect: explicit-owner
Catalog state: valid-owner-absent
Boundary: stop-and-confirm
Actions: none.
```

The unavailable-owner stop does not change the participation decision. A direct named
owner absent from an otherwise valid catalog always reports `Router: bypassed`.

## One target-bound inspection

**Input:** `Use $project-flow-router on ./app. Its recovery record describes an unknown multi-layer incident, but ./app/test-results.json may localize the failure. Inspect that exact pointer once before owner selection. Do not perform downstream work.`

```text
Router: participated
Owner: project-flow-router
Reason: The exact test-results pointer may distinguish a deterministic local defect from a multi-layer incident.
Catalog state: not-consulted
Profile state: not-required
Preference effect: not-applied
Boundary: inspect-only
Actions: inspected ./app/test-results.json once.
```

## Authorized bounded local route-record write

**Input:** `Use $project-flow-router on ./app. Requirements are accepted, but no PRD or issues exist. The valid live catalog exposes to-prd and to-issues. I authorize creating or updating only ./app/artifacts/ROUTE-DECISION.md. Do not run specialists.`

```text
Router: participated
Owner: to-prd -> to-issues
Reason: The prerequisite order is to-prd then to-issues, and the permitted local artifact is limited to the exact route-record path.
Catalog state: valid-current
Profile state: valid
Preference effect: prerequisite-sequence
Boundary: bounded-local-write
Written path: ./app/artifacts/ROUTE-DECISION.md
Authorization source: current user request
Confirmed scope: create or update only the route record
Actions: wrote ./app/artifacts/ROUTE-DECISION.md within the confirmed local scope.
```
