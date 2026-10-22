# 04 - Unfinished

If it is not here, treat it as gone. Do not reconstruct from open PR lists.

| Item | Status | Waiting on | Note |
| --- | --- | --- | --- |
| [DPB-2148](https://novopay.atlassian.net/browse/DPB-2148) DIY collision | Fix on QA (#2484, #2488). Draft prod #2515. **Not** UAT/prod | QA checks 10-16 (414213); then UAT PR; bank remap 2 ARNs + close 3 in-flight; **remove leaked log attachment + rotate HDFC creds** ([HDP-12335](https://novopay.atlassian.net/browse/HDP-12335)) | Resume: `docs/tdd-runs/DPB-2148/TICKET_RESUME.md`. No FE PR. |
| [HDP-8768](https://novopay.atlassian.net/browse/HDP-8768) Blostem status | QA PRs merged + CC proven. Gateway skip-list on the **box** still missing | Ops edit QA (and later UAT/prod) gateway `application.properties` + restart. Bank **mapping sign-off** | Without skip-list, gateway 401 10017 |
| [HDP-12387](https://novopay.atlassian.net/browse/HDP-12387) ETB overwrite | QA PRs via bkup (lib #6909 then CC #2496). Prod PR not opened | Publish lib first | 5 ARNs listed in resume |
| [HDP-12841](https://novopay.atlassian.net/browse/HDP-12841) CC masters loader | Jira **Ready for QA**, assignee Samyuktha (21-22 Oct moved). Masters Jenkins still missing | [DEVOPS-23427](https://novopay.atlassian.net/browse/DEVOPS-23427); confirm `dsa` deploy | SoT still `origin/ddp-qa` |
| [HDP-12874](https://novopay.atlassian.net/browse/HDP-12874) encrypted PAN | **Not a code bug.** Open on him because he diagnosed it | DBA / `rprabhakar` - old UAT rows stay ciphertext | Do not "fix" actor |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) Agent Lead Report dropdown | On Hold | Data cleanup of duplicate `CC_REPORT` rows on preprod | Not a code ticket |
| [HDP-12027](https://novopay.atlassian.net/browse/HDP-12027) UAM reports for all users | Queries drafted/posted; **not applied on prod DSA Superset** | Someone with prod Superset write (he has none) | SQL not in git |
| [HDP-11496](https://novopay.atlassian.net/browse/HDP-11496) Grafana / ECS JSON logs | Phase 1 moved to **Dineshkumar A B**, still To Do | Confirm Ashutosh is **not** coding it (avoid dup) | Deepankar epic |
| [HDP-12325](https://novopay.atlassian.net/browse/HDP-12325) add-on CASE-NBR + Novopay vs Net-banking | Ready for QA, Gowtham. Local evidence `docs/tdd-runs/HDP-12325/` | Gowtham / bank | [DPB-2154](https://novopay.atlassian.net/browse/DPB-2154) is Not An Issue. Blank CASE-NBR = missing cust id |
| LOC consent web customer IP audit | Uncommitted in CC working tree | Decide if part of [HDP-5366](https://novopay.atlassian.net/browse/HDP-5366) follow-up | `LocPersistConsentWebCustomerIpAuditProcessor` |
| Entitled-by-**code** rollout | Designed/committed on `ddp-fea-bkyc` | Actor **before** TaskAlloc on each env; set `...entitled.corporate.codes`; flush TaskAlloc cache | Fails closed if codes set and Actor old |
| Abhishek leaving | Ingest / ADM7 / close file / Superset | Get **his** KT this week | Ashutosh is not the ingest owner |
| BKYC Google Chat | Stopped on purpose | Do not resume | |
| Developer-clone of Deepankar | Recurring, often stale | `TASKS.md` | Coding-standards memory |
| [HDP-12870](https://novopay.atlassian.net/browse/HDP-12870) Aadhaar-mobile fail as N | Open, **unassigned**, reported today | Approval then CC-only fix (~3h) | In prod since 7 May 2026 |
| [HDP-12335](https://novopay.atlassian.net/browse/HDP-12335) mask Authorization in HTTP logs | Ready for QA, Deepankar | Pair with DPB-2148 attachment removal + cred rotate | He reported it |
| [HDP-12140](https://novopay.atlassian.net/browse/HDP-12140) BKYC upload PROCESSING 0 | Open, unassigned | FE poll + download original vs response file | Preprod user 19 / corp 76 |
| [HDP-12386](https://novopay.atlassian.net/browse/HDP-12386) missing x-run-mode | RCA + interceptor in worktree, **uncommitted** | Commit/PR webapp to `ddp-qa` when asked | QA-only until Training promoted |
| [HDP-12080](https://novopay.atlassian.net/browse/HDP-12080) duplicate kyc_detail | Ready for QA Samyuktha. Prod PR [BO #5396](https://github.com/trusttai/trustt-platform-banking-origination/pull/5396) open | Unique key follow-up after prod count | |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) Firestore hang | Bank UAT, Sanooj. Actor flag still default off | Soak then enable actor; DevOps network/alert separate | Worktrees `.wt-11796*` |
| [HDP-11386](https://novopay.atlassian.net/browse/HDP-11386) first-time reactivation 220000 | Open, Kavya | Kavya | He reported |
| [HDP-11970](https://novopay.atlassian.net/browse/HDP-11970) UAT eKYC Invalid OTP | Env config, not code | Compare UAT vs preprod ekyc OTP URLs | |
| BKYC **prod** draft pack | Open: notifications [#5339](https://github.com/trusttai/trustt-platform-notifications/pull/5339), actor [#18591](https://github.com/trusttai/trustt-platform-actor/pull/18591), masterdata [#8458](https://github.com/trusttai/trustt-platform-masterdata/pull/8458), TA [#120](https://github.com/trusttai/trustt-platform-task-allocation/pull/120) | Decide gateway **V4000032 rename** before marking ready. Order: MD 8458 -> actor 18591 -> TA 120 -> set codes key -> notifications 5339 | Comment 399957 on HDP-7636 |
| [HDP-8997](https://novopay.atlassian.net/browse/HDP-8997) doc-upload retry | Batch merged; TA/initial-setup PRs were still open as of 5 Oct | QA FlywayMigrator `enableRepair=true` for V000036/37. UAT batch `bkycAutoAssignRefill` stuck STARTED since 21 Sep | SMS flush batches 121/122 were never triggered before this |
| Remarketing SMS pack | [HDP-7059](https://novopay.atlassian.net/browse/HDP-7059)-[HDP-7062](https://novopay.atlassian.net/browse/HDP-7062) still **To Do**, unassigned | Kill or hand | He created 28 May; no owner |
| DSA delete / 60-day lead freshness | [HDP-6868](https://novopay.atlassian.net/browse/HDP-6868), [HDP-6866](https://novopay.atlassian.net/browse/HDP-6866) To Do, Gowtham | Gowtham | He wrote the stories |
| [HDP-7839](https://novopay.atlassian.net/browse/HDP-7839) BO kyc_detail Flyway not on UAT | Deferred, Deepankar | Deepankar / DBA | DSA KYC Engine |
| [HDP-5288](https://novopay.atlassian.net/browse/HDP-5288) report generation perf | On Hold, Arvind | Arvind | He reported Mar 2026 |
| T17 + PACK-114 BKYC QA | Deferred for **QA DB write** + tomcat Redis | Write grant on `configuration` | Not a product skip |

Laptop-only (ask him before last day):

- Worktrees `Desktop/novopay/.wt-*` that are still the source of truth
- `Downloads\LOC APIs mapping v 0.1 (2).xlsx`
- Bank UAT SELECT pastes / Chat DMs
- DPB-2148 leaked attachment still on Jira
