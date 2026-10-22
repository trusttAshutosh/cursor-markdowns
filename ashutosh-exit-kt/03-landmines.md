# 03 - Landmines

Things that look correct and still fail. Symptom, wrong fix, real fix, how to prove.

Many of these are already in `AGENTS.md`. This file is the **exit shortlist** plus anything not written there yet.

---

## Already in AGENTS.md (successor reads that, Ashutosh confirms still true)

| Landmine | Why it bites | Pointer |
| --- | --- | --- |
| TaskAlloc Flyway in the service JAR | QA already had `V000021`; HDP-8967 journey SMS never landed | TaskAlloc exception in `AGENTS.md` |
| `git merge-tree --name-only` looks clean | GitHub still `CONFLICTING` (CC PR #2513, 2026-10-15) | PR conflict rule |
| `move_agent_to_root` mid-turn | Cursor 3.21.x aborts the agent silently | orchestrator rule |
| Visit owner = `user.id` or `X-Actor-Id` | Agent list empty; seed comments often mislabel the id | BKYC hierarchy notes |
| BKYC file idempotency by file name | Same bytes, different name, still `4000027` (SHA-256 global) | AGENTS.md BKYC facts |
| UAT Superset MySQL | Same live instance as QA; UAT `ddp_superset` is stale | remote-db / Superset rules |
| Preprod vs `ddp-preprod` branch | Preprod deploys `ddp-prod` | AGENTS.md |
| QA `appuser` CREATE | MySQL 1142 on new TaskAlloc tables | AGENTS.md |
| Gateway v2 tenant header | Case-insensitive; do not ask FE to change casing | AGENTS.md |
| Continual Learning stop hook | Plugin updates re-enable it; must disable again | AGENTS.md |
| Direct feature-to-QA PR with conflicts | Close it; use `ddp-bkup-qa` after syncing env tip | AGENTS.md |

---

## Not fully written - Ashutosh must add

Each needs: symptom · wrong fix people will try · real fix · prove.

### BKYC assign

- [ ] Auto-assign skipped a lead and QA says "bug" - which cases are **by design** (cap, no office pin, ineligible corporate)?
- [ ] Reassign vs unassign vs `REASSIGNMENT_REQUESTED` - who is allowed to do which, and what FE will call by mistake
- [ ] Assign SMS sent twice / not sent - where to look (`sms_log` has no `task_id`)

### CC / KYC Engine

- [ ] `mobile_match_flag` / `filler1` blank vs Y/N - eKYC must not phone-compare when filler1 invalid
- [ ] Bank evidence packs: people will invent sample XML; he forbids that
- [ ] Current tickets in flight: DPB-2148, HDP-12325, HDP-12841, HDP-8768 - leftover landmines after merge

### Cursor / laptop

- [ ] Windows Git `BUG (fork bomb)` = missing `mingw64\bin\git.exe`, not a hook loop
- [ ] Gradle hung = stale daemon + `journal-1.lock`
- [ ] `%USERPROFILE%\.cursor\novopay-remote-db.env` is the only credential SoT - do not ask the human to paste hosts

### [FILL] newest burns

_Add the week he burned more than a day on something that is not above._
