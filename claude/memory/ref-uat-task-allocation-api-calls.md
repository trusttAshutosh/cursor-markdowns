---
name: ref-uat-task-allocation-api-calls
description: "UAT task-allocation BKYC validation - gateway host, bank/corporate test users, bank role name ddp_maker01, entitled corporates and test tasks (verified 2026-09-15, HDP-11535)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 934764bb-50ec-484d-b1fa-7f0a798faced
  modified: 2026-09-15T15:32:00.058Z
---

Same call shape as QA ([[ref-qa-task-allocation-api-calls]]) - flat body, unique `x-stan`, pace ~3 s,
validation rejects come back HTTP 500 with a normal `responseStatus`.

- **Gateway:** `https://ddp-uat.trustt.com/api-gateway/api/v2/task-allocation/<api>`. Unlike QA, the UAT
  gateway checks usecase permissions: an unprivileged `x-user-id` (e.g. 1) gets `11017 Insufficient
  privileges` in a snake_case `response_status`.
- **Bank employee:** user `19` (login corporate 2 Tenant). UAT bank role is **`ddp_maker01`** (id 3, role
  group EMPL), not QA's `ddp_BANKMKR`; on 2026-09-15 it still held `TASK-ALLOC-BKYC-VIEW` + `ASSIGN`.
- **Entitled corporates** (`ddp_masterdata.configuration`, columns `prop_key` / `prop_value`):
  `trustt.taskallocation.bkyc.entitled.corporate.ids = 43774,31981,31985`.
- **Corporate users with ASSIGN:** 43774 -> `44462` (also 44463/44464/44468...), 31985 -> `44248`
  (44339/44340/44470), 31981 -> `32500`.
- **Test tasks:** 43774 unassigned `910009`-`910017` (910013 used for the assign cycle; agents 43777
  `GH000011` pin 515345, 43783/43784/43785 pin 500001); 31985 in-progress `11` (agent 43757), closed `6` / `7`
  (KYC_COMPLETED), reassignment-requested `9`; 31981 unassigned `2`-`5`, `8`. No agent at 15 open, so
  Seq 47 cap-15 cannot run without seeding.
- **Logs:** `python ~/.cursor/novopay-remote-ssh.py --env uat --cmd "..."` works; file
  `/apps/applogs/ddp/task-allocation-ddp.log`. DB: `novopay-remote-db-readonly.py --env uat` (its keyword
  guard refuses SQL containing `REPLACE`).
