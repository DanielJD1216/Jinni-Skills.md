# Diagnostic Runbook

Use this file as the first stop when something breaks. Keep it factual, current, and safe to share with an agent.

## Purpose

- Help agents and engineers identify the first failed layer before changing code, redeploying, or requeueing work.
- Keep local, staging, production, provider, queue, and data checks in one place.
- Prevent repeated 1-3 hour investigations caused by checking layers in the wrong order.

## Environments

| Environment | URL or entrypoint | API base | Database | Queue or worker | Deploy target | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Local | [URL or command] | [API base] | [DB name] | [Queue/worker] | N/A | [Notes] |
| Staging | [URL] | [API base] | [DB/service] | [Queue/worker] | [Platform] | [Notes] |
| Production | [URL] | [API base] | [DB/service] | [Queue/worker] | [Platform] | [Notes] |

## Health Checks

Run these before assuming the bug is in code.

| Layer | Check | Expected healthy result |
| --- | --- | --- |
| Frontend | `[command or URL]` | [Healthy signal] |
| Backend API | `[command or URL]` | [Healthy signal] |
| Auth/session | `[command or URL]` | [Healthy signal] |
| Database | `[command or query]` | [Healthy signal] |
| Queue/worker | `[command or dashboard]` | [Healthy signal] |
| External provider | `[dashboard/API/status URL]` | [Healthy signal] |
| Deploy/infrastructure | `[command/dashboard]` | [Healthy signal] |

## First-Failure Ladder

Use this order unless direct evidence points elsewhere.

1. Confirm the environment: local, staging, production, CI, or external provider.
2. Reproduce or capture the user-visible symptom.
3. Check the live API or service health before changing frontend code.
4. Check auth/session if the symptom includes 401, 403, login loops, missing data, or account-specific behavior.
5. Check database/read-model state if the API is healthy but data is wrong or missing.
6. Check workers/queues if data is stuck in "processing", "pending", "queued", or similar states.
7. Check provider delivery and credentials if the issue starts outside the app.
8. Check parser/extraction/transformation if the file or payload arrived but derived fields are wrong.
9. Check deploy/infrastructure if requests fail with 5xx, timeouts, DNS errors, or container health issues.
10. Check fixture/stale data if local or staging behavior conflicts with fresh evidence.

## Logs And Dashboards

| Source | Where to check | What to look for |
| --- | --- | --- |
| Frontend browser console | [Location] | [Errors, failed requests] |
| Backend logs | [Location] | [Exception, status, request id] |
| Worker logs | [Location] | [Job id, retry, stuck state] |
| Database | [Location] | [Rows, status values, timestamps] |
| Provider dashboard | [Location] | [Delivery, auth, quota, status] |
| Deploy platform | [Location] | [Health, release, build, env vars] |

## Safe Commands

These should be read-only by default.

```bash
[Add command]
```

```bash
[Add command]
```

## Dangerous Actions

Do not do these until the failed layer is proven and the rollback/recovery path is clear.

- Redeploying without checking current deployed health and logs.
- Requeueing jobs without checking idempotency, active workers, and stuck state.
- Editing production data manually without a backup and explicit approval.
- Rotating secrets without confirming which service is failing.
- Pasting secrets, private payloads, full customer data, source documents, or sensitive screenshots into agent context.

## External Providers

| Provider | Purpose | Required env vars or secrets | Health/status check | Common failures |
| --- | --- | --- | --- | --- |
| [Provider] | [Purpose] | [Names only, no values] | [Check] | [Failures] |

## Data And Queue Checks

| Workflow | Tables/collections | Status fields | Queue/job names | Healthy progression |
| --- | --- | --- | --- | --- |
| [Workflow] | [Tables] | [Fields] | [Jobs] | [Expected states] |

## Known Failure Modes

| Symptom | First layer to check | Evidence that proves it | Safe next action |
| --- | --- | --- | --- |
| [Symptom] | [Layer] | [Evidence] | [Action] |

## Incident Packet Template

Use this format when reporting a failure:

- Environment:
- User-visible symptom:
- First failed layer:
- Evidence:
- Unknowns:
- Two-minute check:
- Do not do yet:
- Next action:

## Open Questions

- [Operational fact still unknown]
