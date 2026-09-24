# Ashutosh - work evidence (public)

**As of:** 2026-09-23 13:45  - **Sources:** GitHub (`trusttai` / `trusttAshutosh`) + Jira Cloud  - **Refresh:** `python tools/personal_work_evidence_refresh.py`

> Cursor canvas is for Ashutosh only. This mdshare page is the copy anyone can open without Cursor Premium.

---

## 1. About Ashutosh

### Headline

| Metric | Value |
| --- | --- |
| Org PR cadence rank | **#1** of 47 active members |
| Days per PR (career) | **0.314** |
| Career merged PRs | **629** / 677 total |
| Last 120d PRs | **465** created, **439** merged, **16** repos |
| Lines touched (window) | +348551 / -64556 |
| Jira done (assignee history) | 35 |
| Jira open now | 5 |
| Tickets with RCA Remarks | 6 |
| Ever reopened vs done | 3 (8.6%) |

### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 47 active members - 0.314 days/PR, 624 merged PRs in ~6.9 months (source: pr-cadence-top10, as of 2026-09-22). |
| Does not ship volume | **FALSE** | Career: 629 merged / 677 PRs across trusttai; last 120d: 465 PRs, 16 repos, +348551/-64556 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 20 tickets in the window touched 2+ repos in PR titles (e.g. HDP-7350, HDP-7351, HDP-8930, HDP-5366, HDP-8937). Jira journeys covered: ReKyc (15), Credit Card (6), BKYC (2), Loan On Card (2), All (Common) (1). Reopen RCA samples show gateway/header, log-mask, and data-dup root causes - not surface patches. |
| Recurring quality / reopen problem | **CONTEXT** | 3 issues ever reopened while assignee (~8.6% vs 35 done). Currently reopened: 1. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 6 issues with RCA Remarks authored on the ticket, 6 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

### Where work lands (repos, window)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-creditcard-management` | 136 |
| `trustt-platform-lib` | 81 |
| `trustt-platform-task-allocation` | 46 |
| `trustt-platform-masterdata` | 44 |
| `trustt-platform-actor` | 34 |
| `trustt-platform-banking-origination` | 33 |
| `trustt-platform-api-gateway` | 27 |
| `trustt-platform-notifications` | 19 |
| `trustt-platform-initial-setup` | 13 |
| `trustt-platform-authorization` | 12 |
| `trustt-platform-india-stack` | 7 |
| `trustt-platform-consents` | 6 |

### Multi-repo tickets (flow ownership)

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-8930 | 5 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation |
| HDP-5366 | 4 | trustt-platform-consents, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-masterdata |
| HDP-8937 | 4 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-11579 | 3 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-7076 | 3 | trustt-platform-creditcard-management, trustt-platform-lib, trustt-platform-notifications |
| HDP-7828 | 3 | trustt-platform-authorization, trustt-platform-creditcard-management, trustt-platform-masterdata |
| HDP-9219 | 3 | trustt-platform-agent-webapp, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11535 | 2 | trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-5581 | 2 | trustt-platform-creditcard-management, trustt-platform-masterdata |
| HDP-7316 | 2 | trustt-platform-creditcard-management, trustt-platform-masterdata |
| HDP-7377 | 2 | trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-7636 | 2 | trustt-platform-lib, trustt-platform-task-allocation |
| HDP-7725 | 2 | trustt-platform-creditcard-management, trustt-platform-lib |

### Open / blocked now

| Key | Type | Status | Summary | Updated |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Bug | Reopened | fetchEkycDetails Response - Pht and Prn Values Returned as XML Tags Instead of BASE64 | 2026-09-22 |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Bug | Open | BKYC KYC List Accessible for Non-Enabled Corporate | 2026-09-22 |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Bug | Open | BKYC Admin Portal - Newly Assigned Agent Pincode Not Updated in View | 2026-09-22 |
| [HDP-11011](https://novopay.atlassian.net/browse/HDP-11011) | Story | On Hold | PROD New Requirement - Tenant-wise FD Report with Dynamic Filters | 2026-09-17 |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | Bug | On Hold | DSA Admin - Agent Lead Report dropdown displays CC Report entries instead of Agent Lead Report options | 2026-09-02 |

### Ever reopened - why

| Key | Now | Reopens | Bucket | RCA / notes |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Reopened | 1 | Log/masking (product OK) | QA/UAT infra-logging JSON masks for photo/auth_ref_code used ( +), which in JSON has almost no <, so they greedily ate sibling fields (poi.photo / poi.prn) in a |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | On Hold | 1 | Data / env (not code) | Not a code, config, or flyway-definition defect. Pre-prod dsa_masterdata has three active duplicate CC_REPORT rows (9450, 9451, 9452) under REPORT_TYPE/DDP, so  |
| [HDP-6421](https://novopay.atlassian.net/browse/HDP-6421) | Closed | 2 | Cross-service flow | Issue: Wrong or stale agent IP on gateway-fronted calls -> bad comparison with customer IP -> false CC0005 (“same network”). Cause: ValidateCustomerIPAddressProce |

### Recently completed Jira

| Key | Type | Status | Summary | Resolved |
| --- | --- | --- | --- | --- |
| [DPB-1997](https://novopay.atlassian.net/browse/DPB-1997) | Production Bug | Not An Issue | DSA \| Date format issue in DSA | 2026-09-02 |
| [HDP-8967](https://novopay.atlassian.net/browse/HDP-8967) | Sub-task | Done | ST-BE-41: Java - Journey SMS appointment / KYC success / fail | 2026-08-26 |
| [HDP-10752](https://novopay.atlassian.net/browse/HDP-10752) | Bug | Closed | LOC : MIS : Column order needs to be changed for loanType and journeyType | 2026-08-25 |
| [HDP-8954](https://novopay.atlassian.net/browse/HDP-8954) | Sub-task | Done | ST-BE-22: Intake response CSV to DMS (WRITE_INTAKE_RESPONSE workflow step) | 2026-08-20 |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | Sub-task | Done | ST-BE-35: ADM1 corporate getTaskList (Unassigned/In Progress/Closed) | 2026-08-18 |
| [HDP-9551](https://novopay.atlassian.net/browse/HDP-9551) | Sub-task | Done | ST-BE-59: ADM6 corporate getTaskActivityLog (status + assignment audit) | 2026-08-18 |
| [HDP-9004](https://novopay.atlassian.net/browse/HDP-9004) | Sub-task | Done | ST-BE-36: ADM2 eligible agents PINCODE/DISTANCE/HYBRID + cap 15 | 2026-08-18 |
| [HDP-9005](https://novopay.atlassian.net/browse/HDP-9005) | Sub-task | Done | ST-BE-37: ADM3 Assign / Reassign / Unassign | 2026-08-18 |
| [HDP-8957](https://novopay.atlassian.net/browse/HDP-8957) | Sub-task | Done | ST-BE-25: Manual assign SMS - now if in window else pending | 2026-08-18 |
| [HDP-8956](https://novopay.atlassian.net/browse/HDP-8956) | Sub-task | Done | ST-BE-24: Assign SMS flush (schedule/Run now); window 07:00-22:00 | 2026-08-18 |
| [HDP-8953](https://novopay.atlassian.net/browse/HDP-8953) | Sub-task | Done | ST-BE-21: Auto-assign FIFO + water-fill (pincode, cap 10, all unassigned) | 2026-08-14 |
| [HDP-8952](https://novopay.atlassian.net/browse/HDP-8952) | Sub-task | Done | ST-BE-20: Open-task caps 10/15 on Actor candidate set | 2026-08-14 |

---

## 2. Comparative analysis - Ashutosh vs Abhishek vs Harini

Lower **days/PR** and higher **merged/month** = faster cadence. Career span differs (tenure), so prefer pace metrics over raw merged totals. Window = last **120** days for all three.

| Person | Days/PR | Merged/mo | Career merged | Span (mo) | Window merged (120d) | Jira done | Jira open | Ever reopened | Reopen % | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.314 | 89.9 | 629 | 7.0 | 439 | 35 | 5 | 3 | 8.6% | #1 |
| Abhishek | 0.412 | 66.4 | 950 | 14.3 | 259 | 83 | 12 | 0 | 0.0% | #2 |
| Harini | 0.86 | 34.2 | 650 | 19.0 | 158 | 245 | 9 | 1 | 0.4% | #3 |

### How to read this in a meeting

- **Pace (days/PR, merged/month, window merged):** Ashutosh leads this 3-person set.
- **Raw career merged / Jira done:** Abhishek and Harini have longer tenure / different assignee patterns - do not use raw totals alone.
- **AI dependency** cannot be proven from GitHub/Jira; judge RCA depth and multi-repo delivery in section 1.

---

_Generated 2026-09-23 13:45. GitHub: `trusttAshutosh`, `trustt-abhishek`, `Harini-Trustt`. Jira assignee history for Ashutosh Kumar, Abhishek Puranik, Harini Prakash._
