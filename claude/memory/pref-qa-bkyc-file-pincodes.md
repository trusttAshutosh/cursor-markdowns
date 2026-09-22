---
name: pref-qa-bkyc-file-pincodes
description: "Any file generated for Ashutosh (BKYC lead CSVs, fixtures, sample data) must use only the QA agent office pincodes of Manipal 10 and RISL 166512"
metadata:
  node_type: memory
  type: feedback
---

**Whenever generating or sharing a data file** (BKYC lead upload CSV, test fixture, sample rows),
use **only** these QA agent office pincodes. Never invent a pincode, and never reuse the old
placeholders `999999` / `5600`.

**Manipal, corporate `10`:** `111111` (agents 25/26/36), `518301` (166597), `518302` (166598),
`560005` (147), `560009` (145), `560036` (166602).

**RISL Corporate, corporate `166512`:** `560035` (166498), `560102` (166571),
`560103` (166556/166570/166583 - three agents, good multi-result case), `580001` (166494),
`801503` (166517).

**Why:** a lead whose pincode matches no agent office pincode can never auto-assign or appear in the
ADM2 pincode search, so files built with arbitrary pincodes silently produce zero-result tests. QA
corporate `10` already carries a large backlog of unmatchable leads from exactly this mistake.

**How to apply:** pick the pincode from the corporate the file is being uploaded for - Manipal leads
get Manipal pincodes, RISL leads get RISL pincodes. Cross-corporate pincodes never match, because the
eligible-agent search filters on `corporate.parent_id`.

**Known gaps (verified 2026-09-07 18:15 IST):** agent `166494` at `580001` has **no**
`PRDCT-TASKREQUEST-BKYC`, so it is filtered out of eligible search. Agent `36` at `111111` has an
ACTIVE login user but a **DORMANT employee row**. Everything else under both corporates is active end
to end. Ashutosh activated agents 145/147 (mobiles `9100000009` / `9100000005`) and the two RISL
corporate users on 2026-09-07, so any older note calling `560005` / `560009` unusable is stale.
Re-verify before a big run; agents get added and deactivated on QA.

**One agent per pincode — auto-assign spread tests need a shared pincode.** Under Manipal `10`
each of `518301` / `518302` / `560036` is served by exactly **one** agent (`166597` / `166598` /
`166602`), verified against every AUTO assignment ever written for QA file 68 (2026-09-03). Agents are
therefore **not interchangeable**: 10 leads on `518301` can only ever go to `166597`, capped at
`assign.auto.max.open.tasks` (QA value **10**, set 2026-08-18). A file built to test "N leads spread
across M agents" must put all those leads on **one** pincode that M agents share - RISL `560103`
(`166556`/`166570`/`166583`) is the only such pincode. `560012` matches **no** agent at all; leads on it
never auto-assign. Also zero the agents' open tasks first: the cap counts **existing non-terminal**
tasks, so an agent already holding 5 takes only 5 more. Both mistakes together produced the invalid
bug [HDP-11075](https://novopay.atlassian.net/browse/HDP-11075) ("only 5 records per agent") - the
system was behaving exactly to spec.

**What actually fills the cap (verified 2026-09-08).** `KYC_FAILED`, `REASSIGNMENT_REQUESTED`,
`CUSTOMER_UNREACHABLE`, `CALLBACK_REQUESTED`, `APPOINTMENT_RESCHEDULED` are all `is_terminal=0` in
`task_status_master`, so a "failed" or bounced-back visit **keeps holding an auto-cap slot forever**.
Only `KYC_COMPLETED` / `CASE_SUBMITTED` / `REJECTED` / `CUSTOMER_DECLINED` / `DUPLICATE` /
`CLOSED_BY_BANK` / `REQUEST_EXPIRED` free one. On 2026-09-08 all four Manipal pincode agents
(`36`, `166597`, `166598`, `166602`) sat at exactly **10/10**, so every fresh Manipal lead — 2334 of
them — landed in `AWAITING_AGENT_ASSIGNMENT` with note "No pincode-eligible agent under auto cap".
**APK tab names differ from the API's.** The agent app renders **New / Follow Up / Scheduled /
Closed**; the wire protocol and `AgentTaskBucket` call the fourth one **`DONE`** (the app's own
request body sends `"listType":"DONE"` for the Closed chip). `CLOSED` on the wire is the *admin*
ADM1 list type, not the APK's. So a `KYC_FAILED` lead shows under **Closed** to the agent while
still holding an auto-cap slot - that is the whole reason "agent has 10 tasks" looks wrong in the
app. Before any auto-assign test, check
`SELECT ta.agent_id, COUNT(*) ... task_assignment ta JOIN task t JOIN task_status_master sm
WHERE ta.is_active=1 AND sm.is_terminal=0 AND t.task_type_code='BKYC' AND t.corporate_id=<corp>
GROUP BY ta.agent_id` — not just "is there an agent on this pincode".

Related: [[proj-hdp-7636-bkyc]], [[proj-hdp-7636-deferred-qa-tests]].

**Cap value and data state changed on 2026-09-09.** `assign.auto.max.open.tasks` is now **20** and
`assign.manual.max.open.tasks` **30**, both set at 15:17 by `QA_SETUP`; the earlier note of 10 from
2026-08-18 is stale. The same reset wiped the BKYC tasks: 35 fresh `AWAITING_CONTACT` leads under
corporate 10 (ids 912871 to 912905), and task 912575 with all its `KYC_FAILED` rows is gone. Agents
now hold 166598 = 15 on `518302`, 147 = 10 on `560005`, 145 = 10 on `560009`, 166597 = 0 on `518301`.

**The KYC_FAILED cap leak was reproduced end to end on QA on 2026-09-09** (HDP-11241 comment 403349):
166598 filled to 20 of 20, three of those leads driven to `KYC_FAILED` through three failing
`checkNameMatch` calls each, cap-scope count still returned **20** with only **17** workable, and the
next lead on `518302` parked in `AWAITING_AGENT_ASSIGNMENT` with note "No pincode-eligible agent under
auto cap". The three failed leads sat on the agent's Closed tab with `allowedNextStatuses` null.
