---
name: feedback-bank-uat-bkyc-testdata
description: "Bank UAT BKYC test data: build only from the SELECT output Ashutosh pastes (no DB access there); always ask which corporate code has BKYC enabled, default CORP0007"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e9713e78-cfa3-4da6-9912-2ca1a7303e9f
  modified: 2026-09-16T12:41:36.291Z
---

For **bank UAT**, BKYC test data must be built from the **SELECT query output Ashutosh pastes in**, not
from my own queries. I have no DB, SSH or gateway access to bank UAT. It is a **different environment**
from the trustt/ddp UAT at `172.31.2.22` that I can read.

**In bank UAT, BKYC is currently enabled for one corporate only.** Default to **`CORP0007`**, and
**always ask which bank UAT corporate code has BKYC enabled** before building, in case it has changed.
If Ashutosh does not specify, proceed with `CORP0007`.

**Why:** bank UAT has its own corporate ids, agent ids, pincodes and logins. Nothing carries over from
the environments I can query. On ddp UAT the code `CORP0007` happens to resolve to corporate **43606
"Pavan Solutions"** (17 agents, not entitled for BKYC there) - that is a **different corporate** and its
ids must never be reused for bank UAT.

**How to apply:**
1. Ask for the bank UAT corporate code (default `CORP0007`).
2. Ask for the output of `qa-bkyc-lead-files/BKYC-NEW-ENV-DISCOVERY.sql` (Q1 to Q16, corp-code driven).
   Minimum needed to produce files: Q1, Q2, Q6, Q9, Q11.
3. Build the CSVs and run sheet only from that output: eligible agents and their pincodes from Q6,
   negatives from Q7, starting open counts from Q9, a free ARN prefix from Q11, logins from Q13/Q14.
4. Never invent pincodes, agent ids or logins for bank UAT, and never carry over QA or ddp UAT values.
   [[pref-qa-bkyc-file-pincodes]] is a QA-only rule; for bank UAT the pincodes come from that
   environment's own Q6/Q7 rows.
5. Emit any required writes as SQL for someone else to run; assume I cannot execute them there.

## Confirmed bank UAT facts (2026-09-16 round, re-verify the drifting ones)

Stable:
- **`CORP0007` = corporate `625` "Motwanihero"**, ACTIVE, the **only** entitled id
  (`trustt.taskallocation.bkyc.entitled.corporate.ids = 625`). Tenant root is corporate `2`.
- Schemas are the `ddp_` set, same as QA and ddp UAT.
- Caps: auto **10**, manual **15**. `BKYC_OPS` steps 10-50 active.
- **The only role carrying `PRDCT-TASKREQUEST-BKYC` is `QA_BKYC_TASK` (role 337)**, so eligibility there
  means "holds role 337". 34 agents held it as of this round, all with ACTIVE employees, so the
  DORMANT-employee defect is not reproducible on bank UAT.
- Logins: bank corp 2 users **443** (also 442, 1746, 1748, 1780, 1787) can upload and view but **cannot
  assign**; corp 625 users **1260, 1673, 1794** can view and assign but **cannot upload**.
- DB account `supersetreadonly` is **SELECT only** - all writes go to someone else.
- Status master matches ddp UAT (18 rows, `CASE_CLOSED`, `REASSIGNMENT_REQUESTED` in its own bucket).

Drifts, always re-read: agent list and pincodes (Q6), existing tasks and their pincodes (Q10/Q11),
ARN prefixes used (Q11b), open counts (Q9).

Still unknown: agent app login handles (`user_handle` type 6 - Q14 not run; the `agent_mobile` column is
not a reliable substitute), the upload route, the log path, and the deployed branch.

Related: [[ref-uat-task-allocation-api-calls]] (ddp UAT, not bank UAT), [[proj-task-allocation]],
[[proj-hdp-7636-bkyc]].
