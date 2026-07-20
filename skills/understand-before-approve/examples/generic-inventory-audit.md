# Worked Example: Fictional Inventory Audit Gate

This scenario is fictional. Its names, values, fields, and workflows are sample data created only to demonstrate the skill.

## Contents

1. Initial gate
2. Second-turn owner response
3. Second-turn grading response

## 1. Initial Gate

## Decision Context

The owner is deciding whether a fictional inventory-adjustment audit fix is understood well enough for a merge decision. This example stops before approval or merge.

## Direct answer

The change repairs audit traceability for newly recorded adjustment approvals, but it does not repair old audit rows and cannot guarantee an exact historical deep link after the linked proposal disappears. Verdict: `NOT READY`, because comprehension answers and owner choices about historical behavior are still pending.

## Plain-English explanation

Adjustment approvals were being saved, but Item History could not find them because their audit metadata did not identify the item. The fix adds that missing connection and makes the audit entry readable: who acted, the old threshold, the chosen threshold, and the reason.

The link can now open the exact Change Review dialog while the referenced proposal still exists. The link depends on that proposal record. If the proposal later disappears, no confirmed historical fallback exists.

A fictional UAT run kept the reorder threshold at `40 units` and the item stayed at revision `r12`. That supports the claim that this tested path improved audit visibility without changing inventory settings or advancing item revision.

## Technical explanation

- `Confirmed fact`: Adjustment approvals were saved before the fix, but their audit metadata omitted `item_id`, so Item History could not include them.
- `Confirmed fact`: The fix adds `item_id`, `attribute_path`, and `prior_revision` to the audit metadata.
- `Confirmed fact`: The History UI categorizes the event as `Approvals` and displays actor, prior value, chosen value, and reason.
- `Confirmed fact`: The deep link uses the audit resource ID as `proposalId` and opens the exact Change Review dialog.
- `Confirmed fact`: Exact deep-link behavior depends on the referenced proposal still existing.
- `Unknown`: Historical fallback behavior after the proposal no longer exists is unresolved.
- `Confirmed fact`: The fictional UAT run kept the reorder threshold at `40 units` and item revision stayed `r12`.
- `Confirmed fact`: Old pre-fix audit rows were not backfilled.
- `Unknown`: Production deployment state is not established by this scenario.

## Dependency map

`saved adjustment approval -> audit metadata with item_id -> Item History query -> Approvals category -> actor/prior/chosen/reason display`

`audit resource ID -> proposalId -> proposal lookup -> exact Change Review dialog`

The second chain is conditional. If the proposal no longer exists, exact navigation cannot be guaranteed because the historical fallback is unresolved.

## Changed / Not changed

### Changed

- Added `item_id`, `attribute_path`, and `prior_revision` to new adjustment-approval audit metadata.
- Included the event in Item History through `item_id`.
- Categorized the UI event as `Approvals`.
- Displayed actor, prior value, chosen value, and reason.
- Used the audit resource ID as `proposalId` to open the exact Change Review dialog.

### Not changed

- The reorder threshold remained `40 units` in the fictional UAT run.
- Item revision remained `r12` in the fictional UAT run.
- Old pre-fix audit rows were not backfilled.
- Historical fallback after proposal removal was not resolved.
- Production deployment was not proved by the UAT result.

## Proof

| Evidence | Claim supported | Status | Limit |
|---|---|---|---|
| Adjustment-audit implementation | New metadata includes `item_id`, `attribute_path`, and `prior_revision` | Confirmed fact | Does not backfill old rows |
| History UI implementation | Event appears as `Approvals` with actor, prior/chosen values, and reason | Confirmed fact | Does not prove every role or environment |
| Deep-link implementation | Audit resource ID is passed as `proposalId` to the exact dialog | Confirmed fact | Depends on proposal existence |
| Fictional UAT record | Reorder threshold stayed `40 units`; revision stayed `r12` | Confirmed fact | Does not prove deployment, old-row repair, or fallback behavior |
| Historical-row check | Pre-fix rows were not backfilled | Confirmed fact | Does not decide whether a backfill should be added |

## Unknowns / Blind spots

- **Missing historical fallback:** The deep link has no confirmed behavior for a deleted or missing proposal. This matters because audit records can outlive mutable operational records.
- **No historical backfill:** Old rows still lack the metadata needed for Item History. This is known excluded scope, but whether that limitation is acceptable remains an owner decision.
- **Environment boundary:** The scenario gives UAT evidence, not current production deployment evidence.
- **Coverage boundary:** The test covers one role and one scenario. Other roles, failure states, and missing-proposal behavior are not established here.

## Comprehension quiz

1. Adjustment approvals were already saved. Why were they absent from Item History, and which new field creates the missing connection?
2. Trace the user-visible path from the new audit metadata to the `Approvals` entry and its displayed details.
3. What did the fictional UAT prove about the reorder threshold and revision `r12`, and what did it not prove?
4. The deep link opens the exact dialog today. What record must still exist for that to work, and what happens to the guarantee if that record is missing?
5. An old pre-fix audit row does not appear in Item History. Is that evidence that the adjustment approval was never saved? Explain the safe conclusion.

## Owner decisions

- **Decision:** Accept forward-only audit visibility or require historical backfill. **Boundary:** The current fix does not backfill old rows. **Status:** Pending.
- **Decision:** Accept unresolved missing-proposal navigation or require a historical fallback before merge. **Boundary:** Exact navigation depends on proposal existence. **Status:** Pending.
- **Decision:** Define any additional role, failure-path, or environment evidence required before the merge decision. **Boundary:** Current UAT covers one role and scenario only. **Status:** Pending.

## Approval readiness

`NOT READY`

The owner has not answered the load-bearing comprehension questions or made the historical backfill and deep-link fallback decisions. Passing later would mean `READY FOR OWNER DECISION`, not automatic approval.

## 2. Second-Turn Owner Response

The owner replies:

> 1. The approval event existed, but `item_id` was missing, so Item History could not select it. Adding `item_id` creates that connection.
>
> 2. `attribute_path` makes the event appear in Item History, and the fix changes the reorder threshold before showing the new value.
>
> 3. No answer yet.
>
> 4. The proposal must still exist. If it is deleted, the exact dialog is no longer guaranteed because there is no confirmed fallback.
>
> 5. If an old row is absent from Item History, the adjustment approval was never saved.
>
> Owner decision A: Accept forward-only visibility. Do not add a historical backfill to this merge.
>
> Owner decision B: I have not decided whether missing-proposal fallback is required.
>
> Owner decision C: The tested role is enough for this merge; no additional role coverage is required.

This response contains two correct answers, two attempted but incorrect answers, one unanswered item, two explicit owner decisions, and one pending owner decision.

## 3. Second-Turn Grading Response

### Direct answer

Two load-bearing concepts passed, two need correction, and one remains unanswered. One owner decision is still pending, so the recomputed verdict remains `NOT READY`.

### Grading

| Question | Grade | What the answer got right | Correction needed |
|---|---|---|---|
| 1 | `Pass` | Correctly identified missing `item_id` as the reason Item History could not select the saved event | None |
| 2 | `Needs correction` | Recognized that metadata feeds Item History | `item_id`, not `attribute_path`, connects the event to the item query; the fix displays prior and chosen values but does not change the reorder threshold |
| 3 | `Unanswered` | No answer was attempted | Keep the answer key hidden and leave the item pending |
| 4 | `Pass` | Correctly identified proposal existence as the exact-link dependency and the missing fallback | None |
| 5 | `Needs correction` | Recognized that old rows can remain absent from Item History | Absence does not prove the approval was never saved; old saved rows can remain invisible because they were not backfilled with `item_id` |

### Plain-English corrections

- **Question 2:** The item identifier gets the event into the correct item history. The other fields explain the decision once it is there. The screen shows the old and chosen values; it does not apply a new reorder threshold.
- **Question 5:** An old event can exist and still be missing from this item view. The current fix changes new audit metadata, not old rows.

No correction is given for Question 3 because the owner did not attempt it. Its hidden answer remains unrevealed.

### Focused re-quiz

1. A new audit row has `attribute_path` and `prior_revision` but no `item_id`. Will Item History include it, and why?
2. An old adjustment approval was saved before the fix but does not appear in Item History. What two facts must remain separate when interpreting that absence?

Questions 1 and 4 from the initial quiz are not repeated because they passed. Question 3 remains a pending original item rather than receiving a disclosed answer.

### Pending comprehension item

- Answer original Question 3: What did the fictional UAT prove about the reorder threshold and revision `r12`, and what did it not prove?

### Owner decisions status

- **Historical backfill:** Explicit. Keep this merge forward-only.
- **Missing-proposal fallback:** Pending. The owner has not accepted the limitation or required a fallback.
- **Additional role coverage:** Explicit. No additional role coverage is required for this merge decision.

### Approval readiness

`NOT READY`

Two attempted load-bearing concepts require a focused re-quiz, one load-bearing item remains unanswered, and the missing-proposal fallback decision remains pending. Even after these pass, the next state can only be `READY FOR OWNER DECISION`; no approval or merge follows automatically.
