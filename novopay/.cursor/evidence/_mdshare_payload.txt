<a id="top"></a>

# Ashutosh - work evidence (public)

**As of:** 2026-09-23 14:20  - **Sources:** GitHub + Jira  - **Refresh:** `python tools/personal_work_evidence_refresh.py` then `python tools/publish_work_evidence_to_mdshare.py`

> **Toggle time window:** pick a link below. (mdshare has no JS tabs - each section is the full report for that window.)

| Window | Jump |
| --- | --- |
| All time | [Open section](#all-time) |
| Last 30 days | [Open section](#last-30-days) |
| Last 7 days | [Open section](#last-7-days) |

Org-wide cadence (always career): **#1** of 47 active members, **0.314** days/PR.

---

<a id="all-time"></a>

## All time

[All time](#all-time) · [Last 30 days](#last-30-days) · [Last 7 days](#last-7-days) · [Back to top](#top)

### 1. About Ashutosh (All time)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 47 |
| Days per PR (career) | **0.314** |
| Career merged PRs | **629** / 677 total |
| PRs in window (all time) | **677** created, **629** merged, **16** repos |
| Lines touched (window) | +527766 / -85285 |
| Jira done (window) | 35 |
| Jira open now | 5 |
| Jira comments authored | 236 on 70 issues |
| Comments helping others (not assignee) | 203 on 62 issues |
| Reporter (not assignee) | 28 |
| Reopened in window | 3 (8.6%) |
| PR rework (same ticket 2+ PRs) | 49 tickets (48 follow-up after merge, 0 retry after closed) |
| Near-duplicate PR titles (same repo) | 102 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 47 active members - 0.314 days/PR, 624 merged PRs in ~6.9 months (source: pr-cadence-top10, as of 2026-09-22). |
| Does not ship volume | **FALSE** | Career: 629 merged / 677 PRs across trusttai; all time: 677 PRs, 16 repos, +527766/-85285 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 20 tickets in the window touched 2+ repos in PR titles (e.g. HDP-7350, HDP-7351, HDP-8930, HDP-5366, HDP-8937). Jira journeys covered: ReKyc (15), Credit Card (6), BKYC (2), Loan On Card (2), All (Common) (1). Reopen RCA samples show gateway/header, log-mask, and data-dup root causes - not surface patches. |
| Recurring quality / reopen problem | **CONTEXT** | 3 issues reopened in scope (all time) (~8.6% vs 35 done). Currently reopened: 1. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 49 tickets with 2+ authored PRs in window; 48 had follow-up after a merge; 0 retry after closed-unmerged; 102 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 236 comments authored on 70 issues in window; 62 of those were not assigned to Ashutosh (203 help comments). Also reporter on 28 issues assigned to others; 136 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 6 issues with RCA Remarks authored on the ticket, 6 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-creditcard-management` | 270 |
| `trustt-platform-lib` | 98 |
| `trustt-platform-masterdata` | 65 |
| `trustt-platform-task-allocation` | 46 |
| `trustt-platform-actor` | 43 |
| `trustt-platform-banking-origination` | 36 |
| `trustt-platform-api-gateway` | 35 |
| `trustt-platform-notifications` | 21 |
| `trustt-platform-consents` | 16 |
| `trustt-platform-initial-setup` | 15 |
| `trustt-platform-authorization` | 12 |
| `trustt-platform-india-stack` | 7 |

#### Multi-repo tickets

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
| HDP-5718 | 2 | trustt-platform-actor, trustt-platform-creditcard-management |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 58 | 50 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [QA] [HDP-7350] [HDP-7351] add CC KYC Engine and BO HDF \| [QA] [HDP-7350] [HDP-7351] register CC KYC Engine APIs  \| [QA] [HDP-7350] [HDP-7351] enable CC KYC Engine path wi |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 19 | 19 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [QA] [HDP-7350] [HDP-7351] add CC KYC Engine and BO HDF \| [QA] [HDP-7350] [HDP-7351] register CC KYC Engine APIs  \| [QA] [HDP-7350] [HDP-7351] enable CC KYC Engine path wi |
| [HDP-5366](https://novopay.atlassian.net/browse/HDP-5366) | Follow-up after merge | 12 | 12 | trustt-platform-consents, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-masterdata | [QA] [HDP-5366] add portal-open IP validation trace log \| [QA] [HDP-5366] harden consent-stage customer IP resolu \| [QA] [HDP-5366] validate portal-open IP for CC/LOC cons |
| [HDP-7076](https://novopay.atlassian.net/browse/HDP-7076) | Follow-up after merge | 11 | 9 | trustt-platform-creditcard-management, trustt-platform-lib, trustt-platform-notifications | [QA] [HDP-7076] feat(loc): PE-PQ dummy jumbo restrictio \| [QA] [HDP-7076] feat(hdfc-loc): PE-PQ jumbo eligibility \| [QA] [HDP-7076] fix(loc): use no-offers message for PE- |
| [HDP-5718](https://novopay.atlassian.net/browse/HDP-5718) | Follow-up after merge | 10 | 9 | trustt-platform-actor, trustt-platform-creditcard-management | [UAT] [HDP-5718] feat(cc): wire is_cug_user on fetchCus \| [QA] [HDP-5718] feat(cc): wire is_cug_user on fetchCust \| [PROD] [HDP-5718] fix(actor-dsa): CUG permission list a |
| [HDP-7101](https://novopay.atlassian.net/browse/HDP-7101) | Follow-up after merge | 9 | 8 | trustt-platform-actor | [QA] [HDP-7101] fix(reset-mpin): suppress user_id in fo \| [QA] [HDP-7101] fix(actor): suppress user_id in pre-log \| [QA] [HDP-7101] fix(agent-login): suppress pre-otp sess |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | Follow-up after merge | 8 | 8 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation | [QA] fix: getEmployeeCorporateIdForUser for BKYC admin  \| [QA] fix: BKYC corporate file mapping, admin scope, and \| [QA] fix: seed BKYC entitled corporate config keys (HDP |
| [HDP-5581](https://novopay.atlassian.net/browse/HDP-5581) | Follow-up after merge | 7 | 6 | trustt-platform-creditcard-management, trustt-platform-masterdata | [QA] [HDP-5581] Curable Decline \| [QA] [HDP-5581] feat: add CC curable decline category c \| [UAT] [HDP-5581] feat: add CC curable decline category  |
| [HDP-7316](https://novopay.atlassian.net/browse/HDP-7316) | Follow-up after merge | 7 | 7 | trustt-platform-creditcard-management, trustt-platform-masterdata | [QA] [HDP-7316] fix(vkyc-resend): centralize retry poli \| [QA] [HDP-7316]  Create V5000135 - add DSA VKYC resend  \| [QA] [HDP-7316] fix(vkyc-resend): use VKYC-specific blo |
| [HDP-8937](https://novopay.atlassian.net/browse/HDP-8937) | Follow-up after merge | 7 | 7 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-authorization, trustt-platform-task-allocation | [QA] feat: map task-allocation APIs to granular BKYC us \| [QA] feat: TASK-BKYC permission constant (HDP-8937) \| [QA] feat: seed granular task-allocation BKYC permissio |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-7636](https://novopay.atlassian.net/browse/HDP-7636) | Follow-up after merge | 5 | 5 | trustt-platform-lib, trustt-platform-task-allocation | [QA] feat: BKYC shared CSV reader and FlywayMigrator (H \| [QA] feat: Manipal BKYC task-allocation (HDP-7636) \| [DEVELOP] feat: Manipal BKYC task-allocation (HDP-7636) |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | Follow-up after merge | 5 | 5 | trustt-platform-actor, trustt-platform-task-allocation | [HDP-9003] feat: add ADM1 corporate getTaskList for BKY \| [QA] fix: map annexure client, product, and geo onto AD \| [QA] fix: sort ADM1 task list by tab instead of last up |
| [HDP-9219](https://novopay.atlassian.net/browse/HDP-9219) | Follow-up after merge | 5 | 3 | trustt-platform-agent-webapp, trustt-platform-creditcard-management, trustt-platform-lib | [QA] [HDP-9219] feat: send DSE browser details on LOC l \| [QA] [HDP-9219] feat: add LOC MIS device-detail constan \| [QA] [HDP-9219] feat: persist DSE and customer device d |
| [DPB-1674](https://novopay.atlassian.net/browse/DPB-1674) | Follow-up after merge | 4 | 4 | trustt-platform-creditcard-management | [QA] DPB-1674: skip CC0005 for DSA/JAN_SAMARTH/SALES li \| [PROD] fix(cc): restore DPB-1674 IP strip and stop mult \| [UAT] fix(cc): restore DPB-1674 IP strip and stop multi |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [DPB-1461](https://novopay.atlassian.net/browse/DPB-1461) | Follow-up after merge | 3 | 3 | trustt-platform-approval | [QA] [DPB-1461] [DPB-1593]: scope DSA corporate join an \| [UAT] [DPB-1461] [DPB-1593]: scope DSA corporate join a \| [PROD] [DPB-1461] [DPB-1593]: scope DSA corporate join  |
| [DPB-1593](https://novopay.atlassian.net/browse/DPB-1593) | Follow-up after merge | 3 | 3 | trustt-platform-approval | [QA] [DPB-1461] [DPB-1593]: scope DSA corporate join an \| [UAT] [DPB-1461] [DPB-1593]: scope DSA corporate join a \| [PROD] [DPB-1461] [DPB-1593]: scope DSA corporate join  |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | Follow-up after merge | 3 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [PROD] fix: keep time on Excel Timestamp columns (HDP-1 \| [UAT] fix: keep time on Excel Timestamp columns (HDP-10 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Follow-up after merge | 3 | 3 | trustt-platform-authorization, trustt-platform-task-allocation | [UAT] fix: restrict BKYC assign / re-assign / unassign  \| [QA] fix: restrict BKYC assign / re-assign / unassign t \| [QA] fix(uam): split BKYC Management feature by role gr |

#### Jira help via comments (not assignee)

Tickets owned by someone else where Ashutosh still commented (unblocks / guidance).

| Key | Assignee | My comments | Last | Snippet |
| --- | --- | --- | --- | --- |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Salini PD | 4 | 2026-09-18 16:05:44 | HDP-11535 - FE change needed for BKYC menu Context Bank logins were seeing Assign / Re-assign, and permission clean-ups  |
| [HDP-11534](https://novopay.atlassian.net/browse/HDP-11534) | Salini PD | 1 | 2026-09-16 15:29:27 | cc: |
| [HDP-11082](https://novopay.atlassian.net/browse/HDP-11082) | Arvind R | 3 | 2026-09-09 16:24:09 | - thanks, the screenshots pinned it exactly. You were right that something was still wrong, and it is not the search. Th |
| [DEVOPS-22139](https://novopay.atlassian.net/browse/DEVOPS-22139) | Arnold Smith E | 1 | 2026-09-08 19:27:34 | plz do the task-allocation service setup in UAT as well cc: |
| [HDP-11241](https://novopay.atlassian.net/browse/HDP-11241) | Thirumeni Devarajan | 4 | 2026-09-08 14:58:06 | Not a defect - AUTO_ASSIGN behaved to spec. Raising a design gap the run exposed. Report: ARN2026090126 (plus ARN2026090 |
| [HDP-11035](https://novopay.atlassian.net/browse/HDP-11035) | Arvind R | 2 | 2026-09-07 14:18:28 | confirmed the APK fix and the backend fix are both live on QA. getAgentTaskDetails on task 910373 (ARNBKYC20260908, agen |
| [HDP-10981](https://novopay.atlassian.net/browse/HDP-10981) | Samyuktha S | 1 | 2026-09-07 12:00:27 | please recheck this on the latest BKYC build and let me know . The symptom here (map opens on Bangalore instead of the c |
| [HDP-11080](https://novopay.atlassian.net/browse/HDP-11080) | Samyuktha S | 1 | 2026-09-04 13:46:40 | Clarification: current build vs Figma (BKYC Final), side by side Root cause first. The catalogs in the build were frozen |
| [HDP-9036](https://novopay.atlassian.net/browse/HDP-9036) | Thirumeni Devarajan | 2 | 2026-09-04 12:11:01 | BKYC status loops: every cycle, how it is bounded, and the masterdata keys Follow-up to the tab-split comment. This list |
| [DPB-1984](https://novopay.atlassian.net/browse/DPB-1984) | Sanooj M P | 6 | 2026-09-03 19:09:10 | ddp-fea-dpb-1984-hdp-8530-ekyc-fail reverted from india-stack in qa, uat HDP-8530 changes reverted from prod for now. Wi |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | Arvind R | 8 | 2026-09-01 21:22:07 | FE work needed - BKYC corporate mapping (concluded on HDP-8930) SoT: 401415 (access + upload/assign scope) and 401531 (f |
| [HDP-10974](https://novopay.atlassian.net/browse/HDP-10974) | Arvind R | 1 | 2026-09-01 13:54:41 | Update - file format + error message BKYC KYC File Upload accepts CSV only , per HDP-9694 (requirement lock 2026-08-04 / |
| [HDP-9006](https://novopay.atlassian.net/browse/HDP-9006) | Salini PD | 7 | 2026-08-28 11:43:03 | Delta - BCFI has no Task Management menu (2026-08-28) Supersedes comment 400737 S.No. 3. S.No. Rule 1 BKYC reports stay  |
| [HDP-9031](https://novopay.atlassian.net/browse/HDP-9031) | Thirumeni Devarajan | 4 | 2026-08-28 11:42:56 | Delta - BCFI is a BKYC field agent, not corporate (2026-08-28) Supersedes comment 400734 and the BCFI Assignment row in  |
| [HDP-10649](https://novopay.atlassian.net/browse/HDP-10649) | Samyuktha S | 1 | 2026-08-28 09:57:51 | Requirement update vs this ticket This ticket asked: eKYC: Final DAP FILLER5 = GetKycStatus filler2 as-is CKYC: FILLER5  |

#### Reopened in this window - why

| Key | Now | Reopens | Bucket | RCA / notes |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Reopened | 1 | Log/masking (product OK) | QA/UAT infra-logging JSON masks for photo/auth_ref_code used ( +), which in JSON has almost no <, so they greedily ate sibling fields (poi.p |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | On Hold | 1 | Data / env (not code) | Not a code, config, or flyway-definition defect. Pre-prod dsa_masterdata has three active duplicate CC_REPORT rows (9450, 9451, 9452) under  |
| [HDP-6421](https://novopay.atlassian.net/browse/HDP-6421) | Closed | 2 | Cross-service flow | Issue: Wrong or stale agent IP on gateway-fronted calls -> bad comparison with customer IP -> false CC0005 ("same network"). Cause: ValidateCu |

### 2. Comparative analysis (All time)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.314 | 629 | 629 | 7.0 | 35 | 3 | #1 |
| Abhishek | 0.412 | 950 | 950 | 14.3 | 83 | 0 | #2 |
| Harini | 0.86 | 651 | 651 | 19.0 | 245 | 1 | #3 |

---

<a id="last-30-days"></a>

## Last 30 days

[All time](#all-time) · [Last 30 days](#last-30-days) · [Last 7 days](#last-7-days) · [Back to top](#top)

### 1. About Ashutosh (Last 30 days)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 47 |
| Days per PR (career) | **0.314** |
| Career merged PRs | **629** / 677 total |
| PRs in window (30d) | **126** created, **114** merged, **14** repos |
| Lines touched (window) | +190186 / -14851 |
| Jira done (window) | 3 |
| Jira open now | 5 |
| Jira comments authored | 45 on 18 issues |
| Comments helping others (not assignee) | 38 on 15 issues |
| Reporter (not assignee) | 7 |
| Reopened in window | 1 (33.3%) |
| PR rework (same ticket 2+ PRs) | 20 tickets (18 follow-up after merge, 0 retry after closed) |
| Near-duplicate PR titles (same repo) | 15 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 47 active members - 0.314 days/PR, 624 merged PRs in ~6.9 months (source: pr-cadence-top10, as of 2026-09-22). |
| Does not ship volume | **FALSE** | Career: 629 merged / 677 PRs across trusttai; last 30d: 126 PRs, 14 repos, +190186/-14851 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 8 tickets in the window touched 2+ repos in PR titles (e.g. HDP-7350, HDP-7351, HDP-8930, HDP-11579, HDP-11535). Jira journeys covered: ReKyc (15), Credit Card (6), BKYC (2), Loan On Card (2), All (Common) (1). Reopen RCA samples show gateway/header, log-mask, and data-dup root causes - not surface patches. |
| Recurring quality / reopen problem | **CONTEXT** | 1 issues reopened in scope (last 30d) (~33.3% vs 3 done). Currently reopened: 1. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 20 tickets with 2+ authored PRs in window; 18 had follow-up after a merge; 0 retry after closed-unmerged; 15 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 45 comments authored on 18 issues in window; 15 of those were not assigned to Ashutosh (38 help comments). Also reporter on 7 issues assigned to others; 9 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 6 issues with RCA Remarks authored on the ticket, 2 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-task-allocation` | 32 |
| `trustt-platform-lib` | 23 |
| `trustt-platform-creditcard-management` | 18 |
| `trustt-platform-actor` | 9 |
| `trustt-platform-banking-origination` | 8 |
| `trustt-platform-initial-setup` | 8 |
| `trustt-platform-masterdata` | 8 |
| `trustt-platform-authorization` | 5 |
| `trustt-platform-api-gateway` | 4 |
| `trustt-platform-india-stack` | 4 |
| `trustt-platform-approval` | 2 |
| `trustt-platform-consents` | 2 |

#### Multi-repo tickets

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-8930 | 5 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation |
| HDP-11579 | 3 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11535 | 2 | trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-8937 | 2 | trustt-platform-actor, trustt-platform-authorization |
| HDP-8961 | 2 | trustt-platform-actor, trustt-platform-task-allocation |
| HDP-9003 | 2 | trustt-platform-actor, trustt-platform-task-allocation |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 14 | 7 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | fix(kyc-engine): promote ddp-bkup-qa to ddp-qa - KYC En \| fix(kyc-engine): promote ddp-bkup-qa to ddp-qa - KYC En \| fix(kyc-engine): map KYC Engine status filler2 to Final |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | Follow-up after merge | 8 | 8 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation | [QA] fix: getEmployeeCorporateIdForUser for BKYC admin  \| [QA] fix: BKYC corporate file mapping, admin scope, and \| [QA] fix: seed BKYC entitled corporate config keys (HDP |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 5 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [QA] fix: map annexure client, product, and geo onto AD \| [QA] fix: sort ADM1 task list by tab instead of last up \| [QA] fix: fill assigned agent code/name and ADM1 area c |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | Follow-up after merge | 3 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [PROD] fix: keep time on Excel Timestamp columns (HDP-1 \| [UAT] fix: keep time on Excel Timestamp columns (HDP-10 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Follow-up after merge | 3 | 3 | trustt-platform-authorization, trustt-platform-task-allocation | [UAT] fix: restrict BKYC assign / re-assign / unassign  \| [QA] fix: restrict BKYC assign / re-assign / unassign t \| [QA] fix(uam): split BKYC Management feature by role gr |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [QA] fix(infra-platform): map missing request part/valu \| [QA] fix(infra-platform): map missing request part/valu |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [QA] fix(addon-card): tight CDATA wrapping for requestX \| [UAT] fix(addon-card): tight CDATA wrapping for request |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-creditcard-management | [QA] fix: persist KYC Engine initiate and poll in trans \| [UAT] fix: persist KYC Engine initiate and poll in tran |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-approval | [UAT] fix: hide closed applications from Pending Action \| [QA] fix: hide closed applications from Pending Actions |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [PROD] fix(addon-card): tight CDATA wrapping for reques \| [QA] fix(addon-card): tight CDATA wrapping for requestX |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-banking-origination | [QA] fix: expose CC getKycStatus filler2 for Final DAP  \| [UAT] fix: expose CC getKycStatus filler2 for Final DAP |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: stop JSON log masks from swallowing photo an \| [QA] fix: stop JSON log masks from swallowing photo and |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-creditcard-management | [UAT] refactor: align LOC MIS SQL select order with Exc \| [QA] refactor: align LOC MIS SQL select order with Exce |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-india-stack | [UAT] fix: stop painting eKYC auth failures as SUCCESS  \| [QA] fix: stop painting eKYC auth failures as SUCCESS  |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-creditcard-management | [UAT] fix: stop LOC MIS download SQL syntax error \| [QA] fix: stop LOC MIS download SQL syntax error  |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [QA] fix: keep time on Excel Timestamp columns |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-creditcard-management | [UAT] fix: put loanType third on LOC MIS export  \| [QA] fix: put loanType third on LOC MIS export  |

#### Jira help via comments (not assignee)

Tickets owned by someone else where Ashutosh still commented (unblocks / guidance).

| Key | Assignee | My comments | Last | Snippet |
| --- | --- | --- | --- | --- |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Salini PD | 4 | 2026-09-18 16:05:44 | HDP-11535 - FE change needed for BKYC menu Context Bank logins were seeing Assign / Re-assign, and permission clean-ups  |
| [HDP-11534](https://novopay.atlassian.net/browse/HDP-11534) | Salini PD | 1 | 2026-09-16 15:29:27 | cc: |
| [HDP-11082](https://novopay.atlassian.net/browse/HDP-11082) | Arvind R | 3 | 2026-09-09 16:24:09 | - thanks, the screenshots pinned it exactly. You were right that something was still wrong, and it is not the search. Th |
| [DEVOPS-22139](https://novopay.atlassian.net/browse/DEVOPS-22139) | Arnold Smith E | 1 | 2026-09-08 19:27:34 | plz do the task-allocation service setup in UAT as well cc: |
| [HDP-11241](https://novopay.atlassian.net/browse/HDP-11241) | Thirumeni Devarajan | 4 | 2026-09-08 14:58:06 | Not a defect - AUTO_ASSIGN behaved to spec. Raising a design gap the run exposed. Report: ARN2026090126 (plus ARN2026090 |
| [HDP-11035](https://novopay.atlassian.net/browse/HDP-11035) | Arvind R | 2 | 2026-09-07 14:18:28 | confirmed the APK fix and the backend fix are both live on QA. getAgentTaskDetails on task 910373 (ARNBKYC20260908, agen |
| [HDP-10981](https://novopay.atlassian.net/browse/HDP-10981) | Samyuktha S | 1 | 2026-09-07 12:00:27 | please recheck this on the latest BKYC build and let me know . The symptom here (map opens on Bangalore instead of the c |
| [HDP-11080](https://novopay.atlassian.net/browse/HDP-11080) | Samyuktha S | 1 | 2026-09-04 13:46:40 | Clarification: current build vs Figma (BKYC Final), side by side Root cause first. The catalogs in the build were frozen |
| [HDP-9036](https://novopay.atlassian.net/browse/HDP-9036) | Thirumeni Devarajan | 2 | 2026-09-04 12:11:01 | BKYC status loops: every cycle, how it is bounded, and the masterdata keys Follow-up to the tab-split comment. This list |
| [DPB-1984](https://novopay.atlassian.net/browse/DPB-1984) | Sanooj M P | 6 | 2026-09-03 19:09:10 | ddp-fea-dpb-1984-hdp-8530-ekyc-fail reverted from india-stack in qa, uat HDP-8530 changes reverted from prod for now. Wi |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | Arvind R | 4 | 2026-09-01 21:22:07 | FE work needed - BKYC corporate mapping (concluded on HDP-8930) SoT: 401415 (access + upload/assign scope) and 401531 (f |
| [HDP-10974](https://novopay.atlassian.net/browse/HDP-10974) | Arvind R | 1 | 2026-09-01 13:54:41 | Update - file format + error message BKYC KYC File Upload accepts CSV only , per HDP-9694 (requirement lock 2026-08-04 / |
| [HDP-9006](https://novopay.atlassian.net/browse/HDP-9006) | Salini PD | 3 | 2026-08-28 11:43:03 | Delta - BCFI has no Task Management menu (2026-08-28) Supersedes comment 400737 S.No. 3. S.No. Rule 1 BKYC reports stay  |
| [HDP-9031](https://novopay.atlassian.net/browse/HDP-9031) | Thirumeni Devarajan | 4 | 2026-08-28 11:42:56 | Delta - BCFI is a BKYC field agent, not corporate (2026-08-28) Supersedes comment 400734 and the BCFI Assignment row in  |
| [HDP-10649](https://novopay.atlassian.net/browse/HDP-10649) | Samyuktha S | 1 | 2026-08-28 09:57:51 | Requirement update vs this ticket This ticket asked: eKYC: Final DAP FILLER5 = GetKycStatus filler2 as-is CKYC: FILLER5  |

#### Open / blocked now (current)

| Key | Type | Status | Summary | Updated |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Bug | Reopened | fetchEkycDetails Response - Pht and Prn Values Returned as XML Tags Instead of BASE64 | 2026-09-22 |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Bug | Open | BKYC KYC List Accessible for Non-Enabled Corporate | 2026-09-22 |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Bug | Open | BKYC Admin Portal - Newly Assigned Agent Pincode Not Updated in View | 2026-09-22 |
| [HDP-11011](https://novopay.atlassian.net/browse/HDP-11011) | Story | On Hold | PROD New Requirement - Tenant-wise FD Report with Dynamic Filters | 2026-09-17 |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | Bug | On Hold | DSA Admin - Agent Lead Report dropdown displays CC Report entries instead of Agent Lead Report options | 2026-09-02 |

#### Reopened in this window - why

| Key | Now | Reopens | Bucket | RCA / notes |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Reopened | 1 | Log/masking (product OK) | QA/UAT infra-logging JSON masks for photo/auth_ref_code used ( +), which in JSON has almost no <, so they greedily ate sibling fields (poi.p |

### 2. Comparative analysis (Last 30 days)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.314 | 115 | 629 | 7.0 | 3 | 1 | #1 |
| Abhishek | 0.412 | 53 | 950 | 14.3 | 7 | 0 | #2 |
| Harini | 0.86 | 53 | 651 | 19.0 | 32 | 1 | #3 |

---

<a id="last-7-days"></a>

## Last 7 days

[All time](#all-time) · [Last 30 days](#last-30-days) · [Last 7 days](#last-7-days) · [Back to top](#top)

### 1. About Ashutosh (Last 7 days)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 47 |
| Days per PR (career) | **0.314** |
| Career merged PRs | **629** / 677 total |
| PRs in window (7d) | **34** created, **25** merged, **7** repos |
| Lines touched (window) | +116818 / -6164 |
| Jira done (window) | 0 |
| Jira open now | 5 |
| Jira comments authored | 3 on 2 issues |
| Comments helping others (not assignee) | 3 on 2 issues |
| Reporter (not assignee) | 3 |
| Reopened in window | 1 (0.0%) |
| PR rework (same ticket 2+ PRs) | 8 tickets (7 follow-up after merge, 0 retry after closed) |
| Near-duplicate PR titles (same repo) | 1 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 47 active members - 0.314 days/PR, 624 merged PRs in ~6.9 months (source: pr-cadence-top10, as of 2026-09-22). |
| Does not ship volume | **FALSE** | Career: 629 merged / 677 PRs across trusttai; last 7d: 34 PRs, 7 repos, +116818/-6164 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 3 tickets in the window touched 2+ repos in PR titles (e.g. HDP-7350, HDP-7351, HDP-11579). Jira journeys covered: ReKyc (15), Credit Card (6), BKYC (2), Loan On Card (2), All (Common) (1). Reopen RCA samples show gateway/header, log-mask, and data-dup root causes - not surface patches. |
| Recurring quality / reopen problem | **CONTEXT** | 1 issues reopened in scope (last 7d) (~0.0% vs 0 done). Currently reopened: 1. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 8 tickets with 2+ authored PRs in window; 7 had follow-up after a merge; 0 retry after closed-unmerged; 1 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 3 comments authored on 2 issues in window; 2 of those were not assigned to Ashutosh (3 help comments). Also reporter on 3 issues assigned to others; 1 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 6 issues with RCA Remarks authored on the ticket, 0 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-lib` | 9 |
| `trustt-platform-task-allocation` | 7 |
| `trustt-platform-banking-origination` | 6 |
| `trustt-platform-creditcard-management` | 5 |
| `trustt-platform-initial-setup` | 3 |
| `trustt-platform-masterdata` | 3 |
| `trustt-platform-authorization` | 1 |

#### Multi-repo tickets

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-11579 | 3 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 10 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 5 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | Follow-up after merge | 3 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [PROD] fix: keep time on Excel Timestamp columns (HDP-1 \| [UAT] fix: keep time on Excel Timestamp columns (HDP-10 |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: stop JSON log masks from swallowing photo an \| [QA] fix: stop JSON log masks from swallowing photo and |
| [HDP-10752](https://novopay.atlassian.net/browse/HDP-10752) | Multi-PR same ticket | 2 | 1 | trustt-platform-creditcard-management | [PROD] LOC MIS column order journeyName -> journeyType -> \| [PROD] LOC MIS column order (HDP-10752) + device column |
| [HDP-11397](https://novopay.atlassian.net/browse/HDP-11397) | Follow-up after merge | 2 | 2 | trustt-platform-task-allocation | [QA] fix: stamp who acted on the ADM6 activity log (HDP \| [UAT] fix: stamp who acted on the ADM6 activity log (HD |
| [HDP-9423](https://novopay.atlassian.net/browse/HDP-9423) | Follow-up after merge | 2 | 2 | trustt-platform-masterdata | [UAT] HDP-9423: update DSA CKYC GetKycStatus URL to Pro \| [QA] HDP-9423: update DSA CKYC GetKycStatus URL to Prox |

#### Jira help via comments (not assignee)

Tickets owned by someone else where Ashutosh still commented (unblocks / guidance).

| Key | Assignee | My comments | Last | Snippet |
| --- | --- | --- | --- | --- |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Salini PD | 2 | 2026-09-18 16:05:44 | HDP-11535 - FE change needed for BKYC menu Context Bank logins were seeing Assign / Re-assign, and permission clean-ups  |
| [HDP-11534](https://novopay.atlassian.net/browse/HDP-11534) | Salini PD | 1 | 2026-09-16 15:29:27 | cc: |

#### Reopened in this window - why

| Key | Now | Reopens | Bucket | RCA / notes |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Reopened | 1 | Log/masking (product OK) | QA/UAT infra-logging JSON masks for photo/auth_ref_code used ( +), which in JSON has almost no <, so they greedily ate sibling fields (poi.p |

### 2. Comparative analysis (Last 7 days)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.314 | 25 | 629 | 7.0 | 0 | 1 | #1 |
| Abhishek | 0.412 | 10 | 950 | 14.3 | 0 | 0 | #3 |
| Harini | 0.86 | 11 | 651 | 19.0 | 5 | 1 | #2 |

---

_Generated 2026-09-23 14:20. Peers: trusttAshutosh, trustt-abhishek, Harini-Trustt._
