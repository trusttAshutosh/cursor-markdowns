# Ashutosh - work evidence (public)

**As of:** 2026-09-29 08:00  - **Sources:** GitHub + Jira  - **Refresh:** `python tools/personal_work_evidence_refresh.py` then `python tools/publish_work_evidence_to_mdshare.py`

> **Toggle time window:** pick a link below. (mdshare has no JS tabs - each section is the full report for that window.)

| Window | Jump |
| --- | --- |
| All time | [Open section](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) |
| Last 30 days | [Open section](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) |
| Last 7 days | [Open section](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) |
| Peer workload (7d / 30d) | [Open](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#workload) |

Org-wide cadence (always career): **#1** of 48 active members, **0.301** days/PR.

---

## Workload

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

> Peer PR volume (authored). Ashutosh line totals from this pack; peer line totals live on the team-pulse mdshare. Jira done = assignee only.

### Last 7 days

| Person | PRs created | Merged | Merged/mo (pace) | Jira done | Open |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Ashutosh** | 77 | 56 | 243.5 | 0 | 3 |
| Abhishek | 6 | 6 | 26.1 | 0 | 11 |
| Harini | 9 | 9 | 39.1 | 10 | 7 |

_Merged share: Ashutosh: 79% · Abhishek: 8% · Harini: 13% (n=71)._

Ashutosh lines in this window: **+25,859** / **-6,140** across **9** repos (460 files).

### Last 30 days

| Person | PRs created | Merged | Merged/mo (pace) | Jira done | Open |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Ashutosh** | 146 | 122 | 123.8 | 1 | 3 |
| Abhishek | 55 | 51 | 51.7 | 7 | 11 |
| Harini | 54 | 51 | 51.7 | 36 | 7 |

_Merged share: Ashutosh: 54% · Abhishek: 23% · Harini: 23% (n=224)._

Ashutosh lines in this window: **+189,036** / **-11,887** across **14** repos (3,318 files).

---

## All time

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

### 1. About Ashutosh (All time)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 48 |
| Days per PR (career) | **0.301** |
| Career merged PRs | **671** / 733 total |
| PRs in window (all time) | **733** created, **671** merged, **16** repos |
| Lines touched (window) | +538891 / -87296 |
| PR TAT (create -> merge, median / p75) | 0.4h / 1.7h (631/671 under 24h) |
| Multi-repo flow span TAT (median) | 5.7d across 25 flows (11 under 72h) |
| Avg ticket age (first commit -> Ready for QA / Closed) | **25.7d** (median 6.5d, 63 tickets; 33 under 7d) |
| Merged PRs with no Jira key in title | 62.7% (421 PRs) - Jira often missing/late/wrong |
| Jira done (window) | 35 |
| Jira open now | 3 |
| Jira comments authored | 245 on 72 issues |
| Comments helping others (not assignee) | 212 on 64 issues |
| Reporter (not assignee) | 29 |
| Reopened in window | 2 (5.7%) |
| PR rework (same ticket 2+ PRs) | 55 tickets (54 follow-up after merge, 0 retry after closed) |
| Near-duplicate PR titles (same repo) | 119 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 48 active members - 0.301 days/PR, 648 merged PRs in ~7.0 months (source: pr-cadence-top10, as of 2026-09-24). |
| Does not ship volume | **FALSE** | Career: 671 merged / 733 PRs across trusttai; all time: 733 PRs, 16 repos, +538891/-87296 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 25 multi-repo flows shipped with median span TAT 5.7d (first PR open -> last merge across repos); 11 under 72h, 14 under 7d. PR create->merge median 0.4h (p75 1.7h); 631/671 merged in under 24h. 1 reopen RCAs explicitly in cross-service bucket (gateway/header/network) - depth of diagnosis, not title touch. Caveat: 62.7% of merged PRs in window have no Jira key in title - Jira is often missing/late/wrong, so flow evidence is GitHub TAT-first, not journey labels or 'touched N repos'. |
| Recurring quality / reopen problem | **CONTEXT** | 2 issues reopened in scope (all time) (~5.7% vs 35 done). Currently reopened: 0. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. Jira reopen % understates when tickets are never filed or not updated. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 55 tickets with 2+ authored PRs in window; 54 had follow-up after a merge; 0 retry after closed-unmerged; 119 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 245 comments authored on 72 issues in window; 64 of those were not assigned to Ashutosh (212 help comments). Also reporter on 29 issues assigned to others; 141 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 5 issues with RCA Remarks authored on the ticket, 6 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-creditcard-management` | 280 |
| `trustt-platform-lib` | 116 |
| `trustt-platform-masterdata` | 65 |
| `trustt-platform-task-allocation` | 50 |
| `trustt-platform-actor` | 47 |
| `trustt-platform-banking-origination` | 45 |
| `trustt-platform-api-gateway` | 35 |
| `trustt-platform-authorization` | 21 |
| `trustt-platform-notifications` | 21 |
| `trustt-platform-consents` | 18 |
| `trustt-platform-initial-setup` | 15 |
| `trustt-platform-india-stack` | 7 |

#### Multi-repo tickets

Listed for context only - repo count alone is not proof of flow understanding. Prefer **flow span TAT** (first PR open -> last merge) below.

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-8930 | 5 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation |
| HDP-5366 | 4 | trustt-platform-consents, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-masterdata |
| HDP-8937 | 4 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-11579 | 3 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11796 | 3 | trustt-platform-actor, trustt-platform-consents, trustt-platform-lib |
| HDP-7076 | 3 | trustt-platform-creditcard-management, trustt-platform-lib, trustt-platform-notifications |
| HDP-7828 | 3 | trustt-platform-authorization, trustt-platform-creditcard-management, trustt-platform-masterdata |
| HDP-9219 | 3 | trustt-platform-agent-webapp, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11535 | 2 | trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-11729 | 2 | trustt-platform-actor, trustt-platform-task-allocation |

#### Multi-repo flow span TAT

Hours from first authored PR open to last merge for the same ticket across 2+ repos. This is speed-of-shipping a flow, not 'touched'.

| Ticket | Repos | Span | First PR | Last merge |
| --- | --- | --- | --- | --- |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 2 | 0.2h | 2026-09-23 | 2026-09-23 |
| [HDP-7853](https://novopay.atlassian.net/browse/HDP-7853) | 2 | 0.3h | 2026-07-20 | 2026-07-20 |
| [HDP-7828](https://novopay.atlassian.net/browse/HDP-7828) | 3 | 0.5h | 2026-07-28 | 2026-07-28 |
| [HDP-7725](https://novopay.atlassian.net/browse/HDP-7725) | 2 | 0.8h | 2026-07-21 | 2026-07-21 |
| [HDP-8949](https://novopay.atlassian.net/browse/HDP-8949) | 2 | 1.8h | 2026-08-11 | 2026-08-11 |
| [HDP-7377](https://novopay.atlassian.net/browse/HDP-7377) | 2 | 2.9h | 2026-06-15 | 2026-06-15 |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) | 3 | 4.4h | 2026-09-28 | 2026-09-28 |
| [HDP-8336](https://novopay.atlassian.net/browse/HDP-8336) | 2 | 18.2h | 2026-07-16 | 2026-07-17 |
| [HDP-5718](https://novopay.atlassian.net/browse/HDP-5718) | 2 | 1.1d | 2026-04-23 | 2026-04-24 |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 3 | 1.9d | 2026-09-16 | 2026-09-18 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | 2 | 2.9d | 2026-09-15 | 2026-09-18 |
| [HDP-8956](https://novopay.atlassian.net/browse/HDP-8956) | 2 | 3.7d | 2026-08-14 | 2026-08-18 |

#### Ticket age (first commit -> Ready for QA / Closed)

Start = earliest commit on authored PRs with the ticket key in the title. End = first Jira transition to Ready for QA or Closed/Done/Resolved. Window filter uses the end date.

| Ticket | Age | First commit | Ready / Closed | End status |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | 0.5h | 2026-09-17 | 2026-09-17 | Ready for QA |
| [DPB-1674](https://novopay.atlassian.net/browse/DPB-1674) | 0.6h | 2026-06-25 | 2026-06-25 | Ready for QA |
| [HDP-7316](https://novopay.atlassian.net/browse/HDP-7316) | 2.1d | 2026-06-15 | 2026-06-17 | Ready for QA |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | 3.7d | 2026-08-14 | 2026-08-18 | Done |
| [HDP-9219](https://novopay.atlassian.net/browse/HDP-9219) | 8.0d | 2026-08-12 | 2026-08-20 | Ready for QA |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 12.8d | 2026-09-04 | 2026-09-17 | Ready for QA |
| [HDP-5718](https://novopay.atlassian.net/browse/HDP-5718) | 14.6d | 2026-04-09 | 2026-04-24 | Ready for QA |
| [HDP-5366](https://novopay.atlassian.net/browse/HDP-5366) | 35.8d | 2026-04-15 | 2026-05-21 | Ready for QA |
| [HDP-7076](https://novopay.atlassian.net/browse/HDP-7076) | 72.8d | 2026-03-23 | 2026-06-04 | Ready for QA |
| [HDP-5581](https://novopay.atlassian.net/browse/HDP-5581) | 79.2d | 2026-02-04 | 2026-04-24 | Ready for QA |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | 129.9d | 2026-04-30 | 2026-09-07 | Ready for QA |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | 133.0d | 2026-02-26 | 2026-07-09 | Ready for QA |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 58 | 53 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [QA] [HDP-7350] [HDP-7351] add CC KYC Engine and BO HDF \| [QA] [HDP-7350] [HDP-7351] register CC KYC Engine APIs  \| [QA] [HDP-7350] [HDP-7351] enable CC KYC Engine path wi |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 19 | 19 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [QA] [HDP-7350] [HDP-7351] add CC KYC Engine and BO HDF \| [QA] [HDP-7350] [HDP-7351] register CC KYC Engine APIs  \| [QA] [HDP-7350] [HDP-7351] enable CC KYC Engine path wi |
| [HDP-5366](https://novopay.atlassian.net/browse/HDP-5366) | Follow-up after merge | 12 | 12 | trustt-platform-consents, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-masterdata | [QA] [HDP-5366] add portal-open IP validation trace log \| [QA] [HDP-5366] harden consent-stage customer IP resolu \| [QA] [HDP-5366] validate portal-open IP for CC/LOC cons |
| [HDP-7076](https://novopay.atlassian.net/browse/HDP-7076) | Follow-up after merge | 11 | 9 | trustt-platform-creditcard-management, trustt-platform-lib, trustt-platform-notifications | [QA] [HDP-7076] feat(loc): PE-PQ dummy jumbo restrictio \| [QA] [HDP-7076] feat(hdfc-loc): PE-PQ jumbo eligibility \| [QA] [HDP-7076] fix(loc): use no-offers message for PE- |
| [HDP-5718](https://novopay.atlassian.net/browse/HDP-5718) | Follow-up after merge | 10 | 9 | trustt-platform-actor, trustt-platform-creditcard-management | [UAT] [HDP-5718] feat(cc): wire is_cug_user on fetchCus \| [QA] [HDP-5718] feat(cc): wire is_cug_user on fetchCust \| [PROD] [HDP-5718] fix(actor-dsa): CUG permission list a |
| [HDP-7101](https://novopay.atlassian.net/browse/HDP-7101) | Follow-up after merge | 9 | 8 | trustt-platform-actor | [QA] [HDP-7101] fix(reset-mpin): suppress user_id in fo \| [QA] [HDP-7101] fix(actor): suppress user_id in pre-log \| [QA] [HDP-7101] fix(agent-login): suppress pre-otp sess |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | Follow-up after merge | 8 | 8 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation | [QA] fix: getEmployeeCorporateIdForUser for BKYC admin  \| [QA] fix: BKYC corporate file mapping, admin scope, and \| [QA] fix: seed BKYC entitled corporate config keys (HDP |
| [HDP-5581](https://novopay.atlassian.net/browse/HDP-5581) | Follow-up after merge | 7 | 6 | trustt-platform-creditcard-management, trustt-platform-masterdata | [QA] [HDP-5581] Curable Decline \| [QA] [HDP-5581] feat: add CC curable decline category c \| [UAT] [HDP-5581] feat: add CC curable decline category  |
| [HDP-7316](https://novopay.atlassian.net/browse/HDP-7316) | Follow-up after merge | 7 | 7 | trustt-platform-creditcard-management, trustt-platform-masterdata | [QA] [HDP-7316] fix(vkyc-resend): centralize retry poli \| [QA] [HDP-7316]  Create V5000135 - add DSA VKYC resend  \| [QA] [HDP-7316] fix(vkyc-resend): use VKYC-specific blo |
| [HDP-8937](https://novopay.atlassian.net/browse/HDP-8937) | Follow-up after merge | 7 | 7 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-authorization, trustt-platform-task-allocation | [QA] feat: map task-allocation APIs to granular BKYC us \| [QA] feat: TASK-BKYC permission constant (HDP-8937) \| [QA] feat: seed granular task-allocation BKYC permissio |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Follow-up after merge | 6 | 4 | trustt-platform-authorization | [UAT] fix: hide BKYC KYC List for non-entitled corporat \| [QA] fix: hide BKYC KYC List for non-entitled corporate \| [UAT] fix: hide BKYC KYC List for non-entitled corporat |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) | Follow-up after merge | 6 | 3 | trustt-platform-actor, trustt-platform-consents, trustt-platform-lib | [UAT] feat(geo-location): opt-in Firestore hardening kn \| [QA] feat(geo-location): opt-in Firestore hardening kno \| [UAT] fix(cobrowsing): retry once on Firestore timeouts |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Follow-up after merge | 5 | 4 | trustt-platform-lib | [UAT] fix: bound eKYC log masking cost and exact-case X \| [QA] fix: bound eKYC log masking cost, exact-case XML r \| [PROD] fix: mask eKYC SOAP UID/photo/prn/pan in logs an |
| [HDP-7636](https://novopay.atlassian.net/browse/HDP-7636) | Follow-up after merge | 5 | 5 | trustt-platform-lib, trustt-platform-task-allocation | [QA] feat: BKYC shared CSV reader and FlywayMigrator (H \| [QA] feat: Manipal BKYC task-allocation (HDP-7636) \| [DEVELOP] feat: Manipal BKYC task-allocation (HDP-7636) |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | Follow-up after merge | 5 | 5 | trustt-platform-actor, trustt-platform-task-allocation | [HDP-9003] feat: add ADM1 corporate getTaskList for BKY \| [QA] fix: map annexure client, product, and geo onto AD \| [QA] fix: sort ADM1 task list by tab instead of last up |
| [HDP-9219](https://novopay.atlassian.net/browse/HDP-9219) | Follow-up after merge | 5 | 3 | trustt-platform-agent-webapp, trustt-platform-creditcard-management, trustt-platform-lib | [QA] [HDP-9219] feat: send DSE browser details on LOC l \| [QA] [HDP-9219] feat: add LOC MIS device-detail constan \| [QA] [HDP-9219] feat: persist DSE and customer device d |
| [DPB-1674](https://novopay.atlassian.net/browse/DPB-1674) | Follow-up after merge | 4 | 4 | trustt-platform-creditcard-management | [QA] DPB-1674: skip CC0005 for DSA/JAN_SAMARTH/SALES li \| [PROD] fix(cc): restore DPB-1674 IP strip and stop mult \| [UAT] fix(cc): restore DPB-1674 IP strip and stop multi |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [UAT] HDP-11729: expose assignedAgentPincode on getTask \| [UAT] HDP-11729: return OFFICE pincode on getAgentsById \| [QA] HDP-11729: expose assignedAgentPincode on getTaskL |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |

#### Jira help via comments (not assignee)

Tickets owned by someone else where Ashutosh still commented (unblocks / guidance).

| Key | Assignee | My comments | Last | Snippet |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Sanooj M P | 4 | 2026-09-25 16:10:38 | PROD PR: changes are merged in qa, uat envs services: lib, banking-transaction, cc, india-stack change only in lib |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Arvind R | 6 | 2026-09-25 16:03:16 | HDP-11535 - Verified, OK to close The screenshots above show the behaviour now matches the expectation on this ticket. A |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Arvind R | 3 | 2026-09-24 13:24:42 | BKYC menu missing in admin portal - FE change needed Issue: Since 24-Sep (UAT 10:21, QA 12:27), corporate users of BKYC- |
| [HDP-11534](https://novopay.atlassian.net/browse/HDP-11534) | Thirumeni Devarajan | 1 | 2026-09-16 15:29:27 | cc: |
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

#### Reopened in this window - why

| Key | Now | Reopens | Bucket | RCA / notes |
| --- | --- | --- | --- | --- |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | On Hold | 1 | Data / env (not code) | Not a code, config, or flyway-definition defect. Pre-prod dsa_masterdata has three active duplicate CC_REPORT rows (9450, 9451, 9452) under  |
| [HDP-6421](https://novopay.atlassian.net/browse/HDP-6421) | Closed | 2 | Cross-service flow | Issue: Wrong or stale agent IP on gateway-fronted calls -> bad comparison with customer IP -> false CC0005 ("same network"). Cause: ValidateCu |

### 2. Comparative analysis (All time)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.296 | 671 | 671 | 7.1 | 35 | 2 | #1 |
| Abhishek | 0.417 | 956 | 956 | 14.5 | 83 | 1 | #2 |
| Harini | 0.864 | 656 | 656 | 19.2 | 253 | 0 | #3 |

---

## Last 30 days

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

### 1. About Ashutosh (Last 30 days)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 48 |
| Days per PR (career) | **0.301** |
| Career merged PRs | **671** / 733 total |
| PRs in window (30d) | **146** created, **122** merged, **14** repos |
| Lines touched (window) | +189036 / -11887 |
| PR TAT (create -> merge, median / p75) | 0.3h / 1.3h (122/122 under 24h) |
| Multi-repo flow span TAT (median) | 1.5d across 8 flows (6 under 72h) |
| Avg ticket age (first commit -> Ready for QA / Closed) | **14.8d** (median 3.5d, 14 tickets; 8 under 7d) |
| Merged PRs with no Jira key in title | 41.8% (51 PRs) - Jira often missing/late/wrong |
| Jira done (window) | 1 |
| Jira open now | 3 |
| Jira comments authored | 39 on 14 issues |
| Comments helping others (not assignee) | 39 on 14 issues |
| Reporter (not assignee) | 8 |
| Reopened in window | 0 (0.0%) |
| PR rework (same ticket 2+ PRs) | 23 tickets (22 follow-up after merge, 0 retry after closed) |
| Near-duplicate PR titles (same repo) | 24 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 48 active members - 0.301 days/PR, 648 merged PRs in ~7.0 months (source: pr-cadence-top10, as of 2026-09-24). |
| Does not ship volume | **FALSE** | Career: 671 merged / 733 PRs across trusttai; last 30d: 146 PRs, 14 repos, +189036/-11887 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 8 multi-repo flows shipped with median span TAT 1.5d (first PR open -> last merge across repos); 6 under 72h, 7 under 7d. PR create->merge median 0.3h (p75 1.3h); 122/122 merged in under 24h. Caveat: 41.8% of merged PRs in window have no Jira key in title - Jira is often missing/late/wrong, so flow evidence is GitHub TAT-first, not journey labels or 'touched N repos'. |
| Recurring quality / reopen problem | **CONTEXT** | 0 issues reopened in scope (last 30d) (~0.0% vs 1 done). Currently reopened: 0. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. Jira reopen % understates when tickets are never filed or not updated. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 23 tickets with 2+ authored PRs in window; 22 had follow-up after a merge; 0 retry after closed-unmerged; 24 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 39 comments authored on 14 issues in window; 14 of those were not assigned to Ashutosh (39 help comments). Also reporter on 8 issues assigned to others; 7 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 5 issues with RCA Remarks authored on the ticket, 1 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-lib` | 34 |
| `trustt-platform-task-allocation` | 28 |
| `trustt-platform-creditcard-management` | 17 |
| `trustt-platform-banking-origination` | 15 |
| `trustt-platform-actor` | 11 |
| `trustt-platform-authorization` | 11 |
| `trustt-platform-initial-setup` | 7 |
| `trustt-platform-masterdata` | 7 |
| `trustt-platform-consents` | 4 |
| `trustt-platform-india-stack` | 4 |
| `trustt-platform-api-gateway` | 3 |
| `trustt-platform-approval` | 2 |

#### Multi-repo tickets

Listed for context only - repo count alone is not proof of flow understanding. Prefer **flow span TAT** (first PR open -> last merge) below.

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-8930 | 5 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation |
| HDP-11579 | 3 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11796 | 3 | trustt-platform-actor, trustt-platform-consents, trustt-platform-lib |
| HDP-11535 | 2 | trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-11729 | 2 | trustt-platform-actor, trustt-platform-task-allocation |
| HDP-8961 | 2 | trustt-platform-actor, trustt-platform-task-allocation |

#### Multi-repo flow span TAT

Hours from first authored PR open to last merge for the same ticket across 2+ repos. This is speed-of-shipping a flow, not 'touched'.

| Ticket | Repos | Span | First PR | Last merge |
| --- | --- | --- | --- | --- |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 2 | 0.2h | 2026-09-23 | 2026-09-23 |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) | 3 | 4.4h | 2026-09-28 | 2026-09-28 |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | 5 | 23.6h | 2026-09-22 | 2026-09-23 |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | 5 | 1.2d | 2026-09-22 | 2026-09-23 |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 3 | 1.9d | 2026-09-16 | 2026-09-18 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | 2 | 2.9d | 2026-09-15 | 2026-09-18 |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | 5 | 5.7d | 2026-09-02 | 2026-09-08 |
| [HDP-8961](https://novopay.atlassian.net/browse/HDP-8961) | 2 | 7.1d | 2026-09-01 | 2026-09-08 |

#### Ticket age (first commit -> Ready for QA / Closed)

Start = earliest commit on authored PRs with the ticket key in the title. End = first Jira transition to Ready for QA or Closed/Done/Resolved. Window filter uses the end date.

| Ticket | Age | First commit | Ready / Closed | End status |
| --- | --- | --- | --- | --- |
| [HDP-9423](https://novopay.atlassian.net/browse/HDP-9423) | 0.2h | 2026-09-18 | 2026-09-18 | Ready for QA |
| [HDP-11725](https://novopay.atlassian.net/browse/HDP-11725) | 0.5h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | 0.5h | 2026-09-17 | 2026-09-17 | Ready for QA |
| [HDP-11762](https://novopay.atlassian.net/browse/HDP-11762) | 1.1h | 2026-09-25 | 2026-09-25 | Ready for QA |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | 1.6h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11477](https://novopay.atlassian.net/browse/HDP-11477) | 5.0h | 2026-09-15 | 2026-09-15 | Ready for QA |
| [HDP-11792](https://novopay.atlassian.net/browse/HDP-11792) | 1.2d | 2026-09-23 | 2026-09-24 | Ready for QA |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | 5.9d | 2026-09-18 | 2026-09-24 | Ready for QA |
| [HDP-11397](https://novopay.atlassian.net/browse/HDP-11397) | 8.5d | 2026-09-16 | 2026-09-25 | Ready for QA |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | 9.9d | 2026-09-15 | 2026-09-25 | Ready for QA |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 12.8d | 2026-09-04 | 2026-09-17 | Ready for QA |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 14.1d | 2026-09-09 | 2026-09-24 | Ready for QA |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 10 | 8 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | Follow-up after merge | 8 | 8 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation | [QA] fix: getEmployeeCorporateIdForUser for BKYC admin  \| [QA] fix: BKYC corporate file mapping, admin scope, and \| [QA] fix: seed BKYC entitled corporate config keys (HDP |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Follow-up after merge | 6 | 4 | trustt-platform-authorization | [UAT] fix: hide BKYC KYC List for non-entitled corporat \| [QA] fix: hide BKYC KYC List for non-entitled corporate \| [UAT] fix: hide BKYC KYC List for non-entitled corporat |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) | Follow-up after merge | 6 | 3 | trustt-platform-actor, trustt-platform-consents, trustt-platform-lib | [UAT] feat(geo-location): opt-in Firestore hardening kn \| [QA] feat(geo-location): opt-in Firestore hardening kno \| [UAT] fix(cobrowsing): retry once on Firestore timeouts |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Follow-up after merge | 5 | 4 | trustt-platform-lib | [UAT] fix: bound eKYC log masking cost and exact-case X \| [QA] fix: bound eKYC log masking cost, exact-case XML r \| [PROD] fix: mask eKYC SOAP UID/photo/prn/pan in logs an |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 5 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [UAT] HDP-11729: expose assignedAgentPincode on getTask \| [UAT] HDP-11729: return OFFICE pincode on getAgentsById \| [QA] HDP-11729: expose assignedAgentPincode on getTaskL |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | Follow-up after merge | 3 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [PROD] fix: keep time on Excel Timestamp columns (HDP-1 \| [UAT] fix: keep time on Excel Timestamp columns (HDP-10 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Follow-up after merge | 3 | 3 | trustt-platform-authorization, trustt-platform-task-allocation | [UAT] fix: restrict BKYC assign / re-assign / unassign  \| [QA] fix: restrict BKYC assign / re-assign / unassign t \| [QA] fix(uam): split BKYC Management feature by role gr |
| [HDP-11792](https://novopay.atlassian.net/browse/HDP-11792) | Follow-up after merge | 3 | 3 | trustt-platform-creditcard-management | [PROD] fix(HDP-11792): stop KYC Engine callback apply f \| [QA] fix(HDP-11792): stop KYC Engine callback apply fro \| [UAT] fix(HDP-11792): stop KYC Engine callback apply fr |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time \| [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [QA] fix(infra-platform): map missing request part/valu \| [QA] fix(infra-platform): map missing request part/valu |
| (title match) | Near-duplicate title | 2 | 0 | trustt-platform-creditcard-management | [UAT] fix: migrate KYC Engine Jackson 2 ObjectMapper to \| [QA] fix: migrate KYC Engine Jackson 2 ObjectMapper to  |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [QA] fix(addon-card): tight CDATA wrapping for requestX \| [UAT] fix(addon-card): tight CDATA wrapping for request |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: log eKYC responses whole after masking inste \| [QA] fix: log eKYC responses whole after masking instea |

#### Jira help via comments (not assignee)

Tickets owned by someone else where Ashutosh still commented (unblocks / guidance).

| Key | Assignee | My comments | Last | Snippet |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Sanooj M P | 4 | 2026-09-25 16:10:38 | PROD PR: changes are merged in qa, uat envs services: lib, banking-transaction, cc, india-stack change only in lib |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Arvind R | 6 | 2026-09-25 16:03:16 | HDP-11535 - Verified, OK to close The screenshots above show the behaviour now matches the expectation on this ticket. A |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Arvind R | 3 | 2026-09-24 13:24:42 | BKYC menu missing in admin portal - FE change needed Issue: Since 24-Sep (UAT 10:21, QA 12:27), corporate users of BKYC- |
| [HDP-11534](https://novopay.atlassian.net/browse/HDP-11534) | Thirumeni Devarajan | 1 | 2026-09-16 15:29:27 | cc: |
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

#### Open / blocked now (current)

| Key | Type | Status | Summary | Updated |
| --- | --- | --- | --- | --- |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) | Task | Dev In Progress | Firestore client cannot detect a dead connection - co-browsing secure channel hangs 60s and returns 503 (UAT incident 24 Sep) | 2026-09-28 |
| [HDP-11011](https://novopay.atlassian.net/browse/HDP-11011) | Story | On Hold | PROD New Requirement - Tenant-wise FD Report with Dynamic Filters | 2026-09-17 |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | Bug | On Hold | DSA Admin - Agent Lead Report dropdown displays CC Report entries instead of Agent Lead Report options | 2026-09-02 |

### 2. Comparative analysis (Last 30 days)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.296 | 122 | 671 | 7.1 | 1 | 0 | #1 |
| Abhishek | 0.417 | 51 | 956 | 14.5 | 7 | 1 | #2 |
| Harini | 0.864 | 51 | 656 | 19.2 | 36 | 0 | #3 |

---

## Last 7 days

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

### 1. About Ashutosh (Last 7 days)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 48 |
| Days per PR (career) | **0.301** |
| Career merged PRs | **671** / 733 total |
| PRs in window (7d) | **77** created, **56** merged, **9** repos |
| Lines touched (window) | +25859 / -6140 |
| PR TAT (create -> merge, median / p75) | 0.2h / 2.9h (56/56 under 24h) |
| Multi-repo flow span TAT (median) | 14.0h across 4 flows (4 under 72h) |
| Avg ticket age (first commit -> Ready for QA / Closed) | **3.6d** (median 15.1h, 6 tickets; 5 under 7d) |
| Merged PRs with no Jira key in title | 35.7% (20 PRs) - Jira often missing/late/wrong |
| Jira done (window) | 0 |
| Jira open now | 3 |
| Jira comments authored | 8 on 3 issues |
| Comments helping others (not assignee) | 8 on 3 issues |
| Reporter (not assignee) | 2 |
| Reopened in window | 0 (0.0%) |
| PR rework (same ticket 2+ PRs) | 11 tickets (10 follow-up after merge, 0 retry after closed) |
| Near-duplicate PR titles (same repo) | 17 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 48 active members - 0.301 days/PR, 648 merged PRs in ~7.0 months (source: pr-cadence-top10, as of 2026-09-24). |
| Does not ship volume | **FALSE** | Career: 671 merged / 733 PRs across trusttai; last 7d: 77 PRs, 9 repos, +25859/-6140 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 4 multi-repo flows shipped with median span TAT 14.0h (first PR open -> last merge across repos); 4 under 72h, 4 under 7d. PR create->merge median 0.2h (p75 2.9h); 56/56 merged in under 24h. Caveat: 35.7% of merged PRs in window have no Jira key in title - Jira is often missing/late/wrong, so flow evidence is GitHub TAT-first, not journey labels or 'touched N repos'. |
| Recurring quality / reopen problem | **CONTEXT** | 0 issues reopened in scope (last 7d) (~0.0% vs 0 done). Currently reopened: 0. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. Jira reopen % understates when tickets are never filed or not updated. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 11 tickets with 2+ authored PRs in window; 10 had follow-up after a merge; 0 retry after closed-unmerged; 17 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 8 comments authored on 3 issues in window; 3 of those were not assigned to Ashutosh (8 help comments). Also reporter on 2 issues assigned to others; 3 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 5 issues with RCA Remarks authored on the ticket, 0 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-lib` | 24 |
| `trustt-platform-creditcard-management` | 13 |
| `trustt-platform-banking-origination` | 12 |
| `trustt-platform-task-allocation` | 9 |
| `trustt-platform-authorization` | 9 |
| `trustt-platform-actor` | 4 |
| `trustt-platform-initial-setup` | 3 |
| `trustt-platform-consents` | 2 |
| `trustt-platform-masterdata` | 1 |

#### Multi-repo tickets

Listed for context only - repo count alone is not proof of flow understanding. Prefer **flow span TAT** (first PR open -> last merge) below.

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-11796 | 3 | trustt-platform-actor, trustt-platform-consents, trustt-platform-lib |
| HDP-11729 | 2 | trustt-platform-actor, trustt-platform-task-allocation |

#### Multi-repo flow span TAT

Hours from first authored PR open to last merge for the same ticket across 2+ repos. This is speed-of-shipping a flow, not 'touched'.

| Ticket | Repos | Span | First PR | Last merge |
| --- | --- | --- | --- | --- |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 2 | 0.2h | 2026-09-23 | 2026-09-23 |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) | 3 | 4.4h | 2026-09-28 | 2026-09-28 |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | 5 | 23.6h | 2026-09-22 | 2026-09-23 |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | 5 | 1.2d | 2026-09-22 | 2026-09-23 |

#### Ticket age (first commit -> Ready for QA / Closed)

Start = earliest commit on authored PRs with the ticket key in the title. End = first Jira transition to Ready for QA or Closed/Done/Resolved. Window filter uses the end date.

| Ticket | Age | First commit | Ready / Closed | End status |
| --- | --- | --- | --- | --- |
| [HDP-11725](https://novopay.atlassian.net/browse/HDP-11725) | 0.5h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11762](https://novopay.atlassian.net/browse/HDP-11762) | 1.1h | 2026-09-25 | 2026-09-25 | Ready for QA |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | 1.6h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11792](https://novopay.atlassian.net/browse/HDP-11792) | 1.2d | 2026-09-23 | 2026-09-24 | Ready for QA |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | 5.9d | 2026-09-18 | 2026-09-24 | Ready for QA |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 14.1d | 2026-09-09 | 2026-09-24 | Ready for QA |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 10 | 8 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Follow-up after merge | 6 | 4 | trustt-platform-authorization | [UAT] fix: hide BKYC KYC List for non-entitled corporat \| [QA] fix: hide BKYC KYC List for non-entitled corporate \| [UAT] fix: hide BKYC KYC List for non-entitled corporat |
| [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) | Follow-up after merge | 6 | 3 | trustt-platform-actor, trustt-platform-consents, trustt-platform-lib | [UAT] feat(geo-location): opt-in Firestore hardening kn \| [QA] feat(geo-location): opt-in Firestore hardening kno \| [UAT] fix(cobrowsing): retry once on Firestore timeouts |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Follow-up after merge | 5 | 4 | trustt-platform-lib | [UAT] fix: bound eKYC log masking cost and exact-case X \| [QA] fix: bound eKYC log masking cost, exact-case XML r \| [PROD] fix: mask eKYC SOAP UID/photo/prn/pan in logs an |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 5 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [UAT] HDP-11729: expose assignedAgentPincode on getTask \| [UAT] HDP-11729: return OFFICE pincode on getAgentsById \| [QA] HDP-11729: expose assignedAgentPincode on getTaskL |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | Follow-up after merge | 3 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [PROD] fix: keep time on Excel Timestamp columns (HDP-1 \| [UAT] fix: keep time on Excel Timestamp columns (HDP-10 |
| [HDP-11792](https://novopay.atlassian.net/browse/HDP-11792) | Follow-up after merge | 3 | 3 | trustt-platform-creditcard-management | [PROD] fix(HDP-11792): stop KYC Engine callback apply f \| [QA] fix(HDP-11792): stop KYC Engine callback apply fro \| [UAT] fix(HDP-11792): stop KYC Engine callback apply fr |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time \| [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time |
| (title match) | Near-duplicate title | 2 | 0 | trustt-platform-creditcard-management | [UAT] fix: migrate KYC Engine Jackson 2 ObjectMapper to \| [QA] fix: migrate KYC Engine Jackson 2 ObjectMapper to  |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: log eKYC responses whole after masking inste \| [QA] fix: log eKYC responses whole after masking instea |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-banking-origination | [UAT] fix: poll CC KYC status with DS reference after f \| [QA] fix: poll CC KYC status with DS reference after fa |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-creditcard-management | [QA] fix: migrate KYC Engine Jackson 2 ObjectMapper to  \| [PROD] fix: migrate KYC Engine Jackson 2 ObjectMapper t |
| (title match) | Near-duplicate title | 2 | 0 | trustt-platform-banking-origination | [UAT] fix: add RBG kyc_detail CREATE (V9000006) before  \| [QA] fix: add RBG kyc_detail CREATE (V9000006) before E |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-creditcard-management | [UAT] fix: show real field names in CC0006/CC0007 error \| [QA] fix: show real field names in CC0006/CC0007 error  |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: mask aadhaar_number in logs like other Aadha \| [QA] fix: mask aadhaar_number in logs like other Aadhaa |

#### Jira help via comments (not assignee)

Tickets owned by someone else where Ashutosh still commented (unblocks / guidance).

| Key | Assignee | My comments | Last | Snippet |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Sanooj M P | 3 | 2026-09-25 16:10:38 | PROD PR: changes are merged in qa, uat envs services: lib, banking-transaction, cc, india-stack change only in lib |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Arvind R | 2 | 2026-09-25 16:03:16 | HDP-11535 - Verified, OK to close The screenshots above show the behaviour now matches the expectation on this ticket. A |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Arvind R | 3 | 2026-09-24 13:24:42 | BKYC menu missing in admin portal - FE change needed Issue: Since 24-Sep (UAT 10:21, QA 12:27), corporate users of BKYC- |

### 2. Comparative analysis (Last 7 days)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.296 | 56 | 671 | 7.1 | 0 | 0 | #1 |
| Abhishek | 0.417 | 6 | 956 | 14.5 | 0 | 1 | #3 |
| Harini | 0.864 | 9 | 656 | 19.2 | 10 | 0 | #2 |

---

_Generated 2026-09-29 08:00. Peers: trusttAshutosh, trustt-abhishek, Harini-Trustt._
