---
name: ref-bob-task-allocation-local
description: "Running bob validate-ticket against a locally running trustt-platform-task-allocation: port, Actor/Notifications WireMock stubs, DB seed gaps, audit columns, and the 290-scenario status-matrix ticket"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d9860180-f87c-4b3a-a68c-c9b7d3aecca0
  modified: 2026-09-03T21:24:05.936Z
---

Verified 2026-09-03 with ticket `docs/tdd-runs/HDP-7636-status-matrix` (290 scenarios, ~38 min, all PASS on
independent verification). Regenerate the spec with `generate_spec.py` in that folder (dates are relative to
today because appointments must be inside the 3-day window, else 4000008).

**How to run:** `cd trustt-platform-task-allocation && python ..\bob-the-builder\bob.py validate-ticket <id>`
(bob detects the host from cwd). Launch detached (PowerShell `Start-Process` with redirected stdout) - a run of
hundreds of scenarios outlasts the 10-min tool timeout. Export
`JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Users/ashutosh.kumar/tmpnio` first or WireMock's JVM hits the
loopback bug ([[ref-machine-commands]]). `tasklist` returns nothing inside the sandbox - detect completion from
`docs/tdd-runs/<id>/run-summary.json`, not from the pid.

**Gotchas (all bit us once):**
- Local TaskAlloc runs on **8022** (`application.properties`), not the 8020 in `deploy/tdd` / `service_master`.
  `local/user.env` `TASK_ALLOCATION_BASE` now says 8022; bob's user.env overwrites `os.environ`, so an env var on the
  command line does not win.
- Every agent API first resolves the agent id via Actor `getFieldAgentCorporateIdForUser` (HDP-8930). `service_master`
  routes ACTOR and NOTIFICATIONS to `http://localhost:9090/stub/...`; the ticket must ship
  `stubs/mappings/actor-corporate-id-*.json` returning `{responseStatus, corporateId}` (corporateId is used as the
  agent id). WireMock `bodyPatterns.equalToJson {"userId": N}` gives per-agent answers.
- The local `ddp_task_allocation` was hand-seeded: only 7 of 17 BKYC statuses and no `task_bkyc_document` table
  (needed by the async 8_647 closure after CUSTOMER_DECLINED). The ticket's `sql/seed_status_matrix.sql` adds both
  idempotently. A failing statement anywhere in `pre_sql` aborts the whole seed silently ("Task not found").
- bob's DB check reads only `audit.columns` from `deploy/tdd/env-local-task-allocation.yaml`; a column missing there
  shows as `got=None`. Added `appointment_on` and `decline_reason_code` (uncommitted) so the PASS gate is real.
- Business errors come back HTTP 400 with `{responseStatus:{code}}`, so `expect_http_error: true` works.
- Per-step `api_expect` reads the same `{sid}-{api_id}-last.json`, so one scenario per (from,to) pair - do not
  bundle several transitions with the same api_id in one scenario.
- Catalog `updateTaskStatus` defaults carry `appointmentOn: 2026-12-31`; always override it (`""` to send none).
- Seed tasks with fixed ids and `DELETE`-then-`INSERT`; each scenario's `{CRN}` goes into `task.external_ref`
  and bob looks the row up by it (latest `updated_on`). Only one row per scenario may carry the CRN.
- **DB expect for a NULL column must be the literal `NULL`** (bob string-compares mysql --batch output);
  `''` fails with `want= got=NULL`.
- **Masterdata keys are read from Redis first** (`{env}_{tenant}_config_TASK-ALLOCATION_<key>`, tenant db index
  from `tenant_master`, ddp = 0). bob primes them per scenario from ticket / per-scenario `masterdata:` (JDK-serialized
  via redis-cli), so per-scenario overrides work without the masterdata service - but only if `TENANT=ddp` in
  `local/user.env` (it was `dsa`, which primes db 2 that the service never reads). Verified 2026-09-04 with the
  loop-limit keys (ticket `HDP-7636-loop-guard`).
- `BKYC_AUTO_ASSIGN_REFILL` via `triggerWorkflow` resolves corporates from masterdata (entitled list = 90031 locally)
  and **ignores `context.corporate_id`**; seed pool leads under 90031. Eligible-agent stubs can be keyed per pincode
  with WireMock `bodyPatterns.equalToJson {"pincode": ...}`.

Related: [[proj-task-allocation]], [[ref-workspace-tools]], [[ref-machine-commands]].
