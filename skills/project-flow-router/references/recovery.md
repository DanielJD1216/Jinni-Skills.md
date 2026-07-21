# Recovery Routing

Read this reference only when target-bound stale, conflicting, or insufficient truth can change the next owner, or when the user explicitly requests a recovery record.

## Establish recovery state

Treat recovery as an evidence condition, not a mandatory project phase. Use one or more narrow labels when supported:

- `missing-truth`: the target lacks enough current state to choose an owner;
- `stale-truth`: historical claims conflict with current higher-priority evidence;
- `broken-state`: a current build, test, install, or runtime check is known to fail;
- `scope-drift`: current implementation and accepted intent materially diverge;
- `handoff-risk`: no downstream owner could continue safely from available context; or
- `dirty-risk`: user changes exist and ownership is unclear.

Do not classify a project as Recovery merely because it lacks a formal plan or contains an old recovery file.

## Perform one owner-changing inspection

Choose one target-bound evidence check before running it. Use it only to resolve a named conflict or distinguish between plausible owners. Do not expand into general repo orientation or a second check.

If confidence remains low after that inspection, stop with one focused question or the missing evidence. If current truth already establishes the owner, route from it and treat the stale recovery record as historical context.

## Preserve the write gate

Default to read-only routing. A request to inspect, recover, or decide what runs next does not authorize broad cleanup, project setup, deletion, or rewriting.

Write `PROJECT-RECOVERY.md` from `../assets/PROJECT-RECOVERY.template.md` only when the user explicitly requests the record or an active authorized run names it as the required artifact. Before writing, record the exact written path, authorization source, and confirmed artifact scope. Use `bounded-local-write` as the boundary. Keep the record at the verified project boundary, never inside a target skill package.

When the user says `recovery only`, write or update only that record and stop. Preserve existing work and mark stale or conflicting artifacts rather than moving or deleting them.

After an authorized record, return the narrowest next owner and first stop gate. Do not execute specialist work unless separately authorized and owned.
