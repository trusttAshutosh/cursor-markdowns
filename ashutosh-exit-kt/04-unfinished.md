# 04 - Unfinished

If it is not here, treat it as gone. Do not reconstruct from open PR lists.

| Item | Status | Waiting on | Note |
| --- | --- | --- | --- |
| [DPB-2148](https://novopay.atlassian.net/browse/DPB-2148) DIY collision | Fix on QA (#2484, #2488). Draft prod #2515. **Not** UAT/prod | QA checks 10-16 (414213); then UAT PR; bank remap 2 ARNs + close 3 in-flight; **remove leaked log attachment + rotate HDFC creds** ([HDP-12335](https://novopay.atlassian.net/browse/HDP-12335)) | Resume: `docs/tdd-runs/DPB-2148/TICKET_RESUME.md`. No FE PR. |
| [HDP-8768](https://novopay.atlassian.net/browse/HDP-8768) Blostem status | QA PRs merged + CC proven. Gateway skip-list on the **box** still missing | Ops edit QA (and later UAT/prod) gateway `application.properties` + restart. Bank **mapping sign-off** | Without skip-list, gateway 401 10017 |
| [HDP-12387](https://novopay.atlassian.net/browse/HDP-12387) ETB overwrite | QA PRs via bkup (lib #6909 then CC #2496). Prod PR not opened | Publish lib first | 5 ARNs listed in resume |
| [HDP-12841](https://novopay.atlassian.net/browse/HDP-12841) CC masters loader | Plan locked. Feature branch local, **dev not started** | Merge masters-mgmt [PR #28](https://github.com/trusttai/trustt-platform-masters-mgmt/pull/28); confirm Masters Mgmt deployed on `dsa` | SoT `origin/ddp-qa`. Maker-checker still commented out |
| [HDP-12874](https://novopay.atlassian.net/browse/HDP-12874) encrypted PAN | **Not a code bug.** Open on him because he diagnosed it | DBA / `rprabhakar` - old UAT rows stay ciphertext | Do not "fix" actor |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) Agent Lead Report dropdown | On Hold | Data cleanup of duplicate `CC_REPORT` rows on preprod | Not a code ticket |
| [HDP-12027](https://novopay.atlassian.net/browse/HDP-12027) UAM reports for all users | Queries drafted/posted; **not applied on prod DSA Superset** | Someone with prod Superset write (he has none) | SQL not in git |
| [HDP-11496](https://novopay.atlassian.net/browse/HDP-11496) Grafana / ECS JSON logs | Phase 1 moved to **Dineshkumar A B**, still To Do | Confirm Ashutosh is **not** coding it (avoid dup) | Deepankar epic |
| [HDP-12325](https://novopay.atlassian.net/browse/HDP-12325) add-on CASE-NBR | Gowtham's. Local evidence under `docs/tdd-runs/HDP-12325/` | Gowtham / bank on cust-id | He diagnosed; not assignee |
| LOC consent web customer IP audit | Uncommitted in CC working tree | Decide if part of [HDP-5366](https://novopay.atlassian.net/browse/HDP-5366) follow-up | `LocPersistConsentWebCustomerIpAuditProcessor` |
| Entitled-by-**code** rollout | Designed/committed on `ddp-fea-bkyc` | Actor **before** TaskAlloc on each env; set `...entitled.corporate.codes`; flush TaskAlloc cache | Fails closed if codes set and Actor old |
| Abhishek leaving | Ingest / ADM7 / close file / Superset | Get **his** KT this week | Ashutosh is not the ingest owner |
| BKYC Google Chat | Stopped on purpose | Do not resume | |
| Developer-clone of Deepankar | Recurring, often stale | `TASKS.md` | Coding-standards memory |

Laptop-only (ask him before last day):

- Worktrees `Desktop/novopay/.wt-*` that are still the source of truth
- `Downloads\LOC APIs mapping v 0.1 (2).xlsx`
- Bank UAT SELECT pastes / Chat DMs
- DPB-2148 leaked attachment still on Jira
