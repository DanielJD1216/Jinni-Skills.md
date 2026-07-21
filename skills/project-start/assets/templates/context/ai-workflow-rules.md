# AI Workflow Rules

## Approach

[Describe the development approach. Example: build incrementally using spec-driven units. Context files define what to build, how to build it, and what state the project is in.]

## Scoping Rules

- Work on one feature unit at a time.
- Prefer small, verifiable increments over broad speculative changes.
- Do not combine unrelated system boundaries in a single implementation step.

## When to Split Work

Split an implementation step if it combines:

- [Concern one]
- [Concern two]
- [Concern three]

If a change cannot be verified end to end quickly, the scope is too broad.

## Handling Missing Requirements

- Do not invent product behavior not defined in the context files or current task.
- If a requirement is ambiguous, resolve it in the relevant context file before implementing when risk is meaningful.
- If a requirement is missing and work can safely continue, add it as an open question in `progress-tracker.md`.

## Protected Files

Do not modify the following unless explicitly instructed:

- [Protected path or file]
- [Protected path or file]

## Keeping Docs in Sync

Update the relevant context file whenever implementation changes:

- System architecture or boundaries
- Storage model decisions
- Code conventions or standards
- Feature scope
- UI tokens or component conventions

## Before Moving to the Next Unit

1. The current unit works end to end within its defined scope.
2. No invariant defined in `architecture.md` was violated.
3. `progress-tracker.md` reflects the completed work.
4. Required verification commands pass, or the blocker is documented.
