---
name: proj-hdp-7636-deferred-qa-tests
description: "HDP-7636 QA checks deferred for lack of DB write access on QA - T17 (name-match outage) and PACK-114 (assign SMS held outside hours), with exact runbooks"
metadata: 
  node_type: memory
  type: project
  originSessionId: d9860180-f87c-4b3a-a68c-c9b7d3aecca0
  modified: 2026-09-07T08:10:00.000Z
---

Two HDP-7636 QA regression checks are **deferred for access, not for product reasons**. As of
2026-09-05 Ashutosh has **neither INSERT nor UPDATE** on `ddp_masterdata.configuration`, and the
sanctioned DB tool (`~/.cursor/novopay-remote-db-readonly.py`) hard-refuses anything but `SELECT`.
The Redis flush also needs the **tomcat** account — `redis-cli` from the normal SSH user gets
`Connection refused` on 127.0.0.1:6379. Run both once access is granted. See [[proj-hdp-7636-bkyc]].

**Shared Redis flush procedure** (Ashutosh's steps, QA app server):
`sudo -u tomcat -i` → `sh redis-cli.sh` → `select 1` → find the key with
`--scan --pattern "*<propKey fragment>*"` (do not guess the prefix) → `DEL <key>` → `exit`.

## T17 — bank name-match service unavailable

Prove that when the bank's name-match service fails, the customer does **not** lose an attempt
(`score()` throws before the counter is incremented).

QA BKYC name matching does **not** go through the local simulator: there is no
`hdfc.soa.name.match.service.url` row for service `TASK-ALLOCATION`, so it falls back to the
compiled default, the live HDFC UAT endpoint. `BANKING-ORIGINATION` (row 87) and `ACTOR` (row 152)
both already point at the QA simulator `https://172.31.2.132:8686/simulate/soap/nameMatch`.

1. Pick a lead with `task_bkyc.name_match_attempt_count = 0` on an agent whose login user is known
   (agent 26 = user 89, agent 166602 = user 133154).
2. `INSERT` the key for service `TASK-ALLOCATION` with a dead value, e.g. `https://127.0.0.1:9/dead`.
3. Flush `...hdfc.soa.name.match.service.url`.
4. One `checkNameMatch`. Expect a failure **and an unchanged attempt counter**.
5. `UPDATE` the row to its final value, flush again, verify with a healthy call.

**Final value (Ashutosh):** the **same as ACTOR and BANKING-ORIGINATION** — the simulator URL, not
the HDFC UAT default. **Raise at that point:** the simulator's canned response
(`novopay_simulator.simulator_response` id 82) returns a **fixed `namePercentage` of 100**, so once
TASK-ALLOCATION points there the mismatch scenarios (T14/T15) become untestable unless the canned
response is made input-sensitive.

## PACK-114 — assign SMS is held outside 07:00–22:00

The quiet-hours window is **configuration, not the system clock** — four live rows in
`ddp_masterdata.configuration` for service `TASK-ALLOCATION`:
`trustt.taskallocation.bkyc.sms.assign.window.start` / `.end` and
`trustt.taskallocation.bkyc.sms.journey.window.start` / `.end`, currently `07:00` / `22:00`.
So this needs **one UPDATE to an existing row**, no clock control.

1. `UPDATE ddp_masterdata.configuration SET prop_value='07:30' WHERE prop_key=
   'trustt.taskallocation.bkyc.sms.assign.window.end' AND service='TASK-ALLOCATION';`
   (window becomes 07:00–07:30, so "now" is outside it).
2. Flush `...sms.assign.window.end`.
3. Trigger the flush job:
   `GET https://localhost:8022/task-allocation/api/v2/internal/workflow/trigger-scheduled?workflowCode=BKYC_ASSIGN_SMS_FLUSH`
   with headers `X-Tenant-Code`, `X-User-Id`, `X-Batch-Id`, `X-Batch-Run-Id`.
4. Expect the outside-window signature **`skipped = pending, sent = 0, failed = 0`** plus the log
   line `Assign SMS flush skipped outside window` (`AssignSmsService:72`). This is distinguishable
   from the current in-window failure mode (`failed = pending`), so the test works even while SMS
   delivery is broken — it proves messages are *held*, not attempted and lost.
5. Revert `prop_value` to `22:00` and flush again.

**Caution:** while narrowed, assign SMS is held for the **whole ddp tenant**, not just test leads.
Keep the window short and revert in the same session.

## Related live finding

No SMS is being delivered on QA at all — every flush run since at least 2026-09-02 reports
`sent=0`. **Root cause found 2026-09-07:** `NotificationsSmsClient` (task-allocation) posts a flat
`{user_story_code, locale}` body to Notifications v1 `getNotificationMessageByNotificationCode`, which
requires the `{request:{...},headers:{...}}` envelope; Notifications answers `13007 Missing required
JSON section 'headers'`. Every upload re-tries the whole pending backlog (44 on 2026-09-07). Fixed
locally 2026-09-07 (uncommitted on `ddp-fea-bkyc`): `NotificationsSmsClient.v1Envelope` wraps the body. Separate defect (`SMS-DELIVERY`), not a blocker above.

**QA DB access (2026-09-07):** the `mugesh` credentials in `~/.cursor/novopay-remote-db.env` were rejected (`ERROR 1045`) once in the morning but worked again from 12:20 IST the same day via the read-only tool, so treat a 1045 as transient and retry before falling back to `getTaskLeadUploadList` / `getTaskList` as read proxies. No `mysql` client exists on the QA app box. Full upload-API check: `docs/tdd-runs/HDP-7636/regression-2026-09-prep/UPLOAD_API_QA_CHECK_2026-09-07.md`. Server-log access: [[ref-qa-server-access]].

Full results: `docs/tdd-runs/HDP-7636/regression-2026-09-prep/ARTIFACT_BKYC_QA_RESULTS.csv`.
