# Ashutosh - work evidence (public)

**As of:** 2026-09-24 02:07  - **Sources:** GitHub + Jira  - **Refresh:** `python tools/personal_work_evidence_refresh.py` then `python tools/publish_work_evidence_to_mdshare.py`

> **Toggle time window:** pick a link below. (mdshare has no JS tabs - each section is the full report for that window.)

| Window | Jump |
| --- | --- |
| All time | [Open section](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) |
| Last 30 days | [Open section](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) |
| Last 7 days | [Open section](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) |
| Peer workload (7d / 30d) | [Open](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#workload) |

Org-wide cadence (always career): **#1** of 47 active members, **0.314** days/PR.

---

## Workload

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

> Peer PR volume (authored). Ashutosh line totals from this pack; peer line totals live on the team-pulse mdshare. Jira done = assignee only.

### Last 7 days

| Person | PRs created | Merged | Merged/mo (pace) | Jira done | Open |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Ashutosh** | 57 | 38 | 165.2 | 0 | 4 |
| Abhishek | 14 | 13 | 56.5 | 0 | 9 |
| Harini | 15 | 14 | 60.9 | 5 | 8 |

_Merged share: Ashutosh: 58% · Abhishek: 20% · Harini: 22% (n=65)._

Ashutosh lines in this window: **+123,049** / **-7,047** across **8** repos (1,518 files).

### Last 30 days

| Person | PRs created | Merged | Merged/mo (pace) | Jira done | Open |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Ashutosh** | 149 | 128 | 129.9 | 3 | 4 |
| Abhishek | 63 | 56 | 56.8 | 7 | 9 |
| Harini | 60 | 56 | 56.8 | 33 | 8 |

_Merged share: Ashutosh: 53% · Abhishek: 23% · Harini: 23% (n=240)._

Ashutosh lines in this window: **+196,417** / **-15,734** across **14** repos (3,600 files).

---

## All time

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

### 1. About Ashutosh (All time)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 47 |
| Days per PR (career) | **0.314** |
| Career merged PRs | **642** / 700 total |
| PRs in window (all time) | **700** created, **642** merged, **16** repos |
| Lines touched (window) | +533997 / -86168 |
| PR TAT (create -> merge, median / p75) | 0.4h / 1.7h (602/642 under 24h) |
| Multi-repo flow span TAT (median) | 6.3d across 24 flows (10 under 72h) |
| Avg ticket age (first commit -> Ready for QA / Closed) | **28.0d** (median 6.8d, 57 tickets; 29 under 7d) |
| Merged PRs with no Jira key in title | 63.6% (408 PRs) - Jira often missing/late/wrong |
| Jira done (window) | 35 |
| Jira open now | 4 |
| Jira comments authored | 236 on 70 issues |
| Comments helping others (not assignee) | 203 on 62 issues |
| Reporter (not assignee) | 28 |
| Reopened in window | 3 (8.6%) |
| PR rework (same ticket 2+ PRs) | 51 tickets (49 follow-up after merge, 1 retry after closed) |
| Near-duplicate PR titles (same repo) | 112 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 47 active members - 0.314 days/PR, 624 merged PRs in ~6.9 months (source: pr-cadence-top10, as of 2026-09-22). |
| Does not ship volume | **FALSE** | Career: 642 merged / 700 PRs across trusttai; all time: 700 PRs, 16 repos, +533997/-86168 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 24 multi-repo flows shipped with median span TAT 6.3d (first PR open -> last merge across repos); 10 under 72h, 13 under 7d. PR create->merge median 0.4h (p75 1.7h); 602/642 merged in under 24h. 1 reopen RCAs explicitly in cross-service bucket (gateway/header/network) - depth of diagnosis, not title touch. Caveat: 63.6% of merged PRs in window have no Jira key in title - Jira is often missing/late/wrong, so flow evidence is GitHub TAT-first, not journey labels or 'touched N repos'. |
| Recurring quality / reopen problem | **CONTEXT** | 3 issues reopened in scope (all time) (~8.6% vs 35 done). Currently reopened: 1. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. Jira reopen % understates when tickets are never filed or not updated. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 51 tickets with 2+ authored PRs in window; 49 had follow-up after a merge; 1 retry after closed-unmerged; 112 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 236 comments authored on 70 issues in window; 62 of those were not assigned to Ashutosh (203 help comments). Also reporter on 28 issues assigned to others; 137 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 6 issues with RCA Remarks authored on the ticket, 6 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-creditcard-management` | 275 |
| `trustt-platform-lib` | 105 |
| `trustt-platform-masterdata` | 65 |
| `trustt-platform-task-allocation` | 48 |
| `trustt-platform-actor` | 45 |
| `trustt-platform-banking-origination` | 39 |
| `trustt-platform-api-gateway` | 35 |
| `trustt-platform-notifications` | 21 |
| `trustt-platform-authorization` | 16 |
| `trustt-platform-consents` | 16 |
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
| HDP-7076 | 3 | trustt-platform-creditcard-management, trustt-platform-lib, trustt-platform-notifications |
| HDP-7828 | 3 | trustt-platform-authorization, trustt-platform-creditcard-management, trustt-platform-masterdata |
| HDP-9219 | 3 | trustt-platform-agent-webapp, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11535 | 2 | trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-11729 | 2 | trustt-platform-actor, trustt-platform-task-allocation |
| HDP-5581 | 2 | trustt-platform-creditcard-management, trustt-platform-masterdata |

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
| [HDP-8336](https://novopay.atlassian.net/browse/HDP-8336) | 2 | 18.2h | 2026-07-16 | 2026-07-17 |
| [HDP-5718](https://novopay.atlassian.net/browse/HDP-5718) | 2 | 1.1d | 2026-04-23 | 2026-04-24 |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 3 | 1.9d | 2026-09-16 | 2026-09-18 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | 2 | 2.9d | 2026-09-15 | 2026-09-18 |
| [HDP-8956](https://novopay.atlassian.net/browse/HDP-8956) | 2 | 3.7d | 2026-08-14 | 2026-08-18 |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | 5 | 5.7d | 2026-09-02 | 2026-09-08 |

#### Ticket age (first commit -> Ready for QA / Closed)

Start = earliest commit on authored PRs with the ticket key in the title. End = first Jira transition to Ready for QA or Closed/Done/Resolved. Window filter uses the end date.

| Ticket | Age | First commit | Ready / Closed | End status |
| --- | --- | --- | --- | --- |
| [DPB-1674](https://novopay.atlassian.net/browse/DPB-1674) | 0.6h | 2026-06-25 | 2026-06-25 | Ready for QA |
| [HDP-7316](https://novopay.atlassian.net/browse/HDP-7316) | 2.1d | 2026-06-15 | 2026-06-17 | Ready for QA |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | 3.7d | 2026-08-14 | 2026-08-18 | Done |
| [HDP-9219](https://novopay.atlassian.net/browse/HDP-9219) | 8.0d | 2026-08-12 | 2026-08-20 | Ready for QA |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 12.8d | 2026-09-04 | 2026-09-17 | Ready for QA |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 14.1d | 2026-09-09 | 2026-09-24 | Ready for QA |
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
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-7636](https://novopay.atlassian.net/browse/HDP-7636) | Follow-up after merge | 5 | 5 | trustt-platform-lib, trustt-platform-task-allocation | [QA] feat: BKYC shared CSV reader and FlywayMigrator (H \| [QA] feat: Manipal BKYC task-allocation (HDP-7636) \| [DEVELOP] feat: Manipal BKYC task-allocation (HDP-7636) |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | Follow-up after merge | 5 | 5 | trustt-platform-actor, trustt-platform-task-allocation | [HDP-9003] feat: add ADM1 corporate getTaskList for BKY \| [QA] fix: map annexure client, product, and geo onto AD \| [QA] fix: sort ADM1 task list by tab instead of last up |
| [HDP-9219](https://novopay.atlassian.net/browse/HDP-9219) | Follow-up after merge | 5 | 3 | trustt-platform-agent-webapp, trustt-platform-creditcard-management, trustt-platform-lib | [QA] [HDP-9219] feat: send DSE browser details on LOC l \| [QA] [HDP-9219] feat: add LOC MIS device-detail constan \| [QA] [HDP-9219] feat: persist DSE and customer device d |
| [DPB-1674](https://novopay.atlassian.net/browse/DPB-1674) | Follow-up after merge | 4 | 4 | trustt-platform-creditcard-management | [QA] DPB-1674: skip CC0005 for DSA/JAN_SAMARTH/SALES li \| [PROD] fix(cc): restore DPB-1674 IP strip and stop mult \| [UAT] fix(cc): restore DPB-1674 IP strip and stop multi |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [UAT] HDP-11729: expose assignedAgentPincode on getTask \| [UAT] HDP-11729: return OFFICE pincode on getAgentsById \| [QA] HDP-11729: expose assignedAgentPincode on getTaskL |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Retry after closed | 4 | 0 | trustt-platform-authorization | [UAT] fix: hide BKYC KYC List for non-entitled corporat \| [QA] fix: hide BKYC KYC List for non-entitled corporate \| [UAT] fix: hide BKYC KYC List for non-entitled corporat |
| [DPB-1461](https://novopay.atlassian.net/browse/DPB-1461) | Follow-up after merge | 3 | 3 | trustt-platform-approval | [QA] [DPB-1461] [DPB-1593]: scope DSA corporate join an \| [UAT] [DPB-1461] [DPB-1593]: scope DSA corporate join a \| [PROD] [DPB-1461] [DPB-1593]: scope DSA corporate join  |
| [DPB-1593](https://novopay.atlassian.net/browse/DPB-1593) | Follow-up after merge | 3 | 3 | trustt-platform-approval | [QA] [DPB-1461] [DPB-1593]: scope DSA corporate join an \| [UAT] [DPB-1461] [DPB-1593]: scope DSA corporate join a \| [PROD] [DPB-1461] [DPB-1593]: scope DSA corporate join  |

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
| **Ashutosh** | 0.303 | 642 | 642 | 7.0 | 35 | 3 | #1 |
| Abhishek | 0.416 | 953 | 953 | 14.5 | 83 | 0 | #2 |
| Harini | 0.859 | 654 | 654 | 19.0 | 246 | 0 | #3 |

---

## Last 30 days

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

### 1. About Ashutosh (Last 30 days)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 47 |
| Days per PR (career) | **0.314** |
| Career merged PRs | **642** / 700 total |
| PRs in window (30d) | **149** created, **127** merged, **14** repos |
| Lines touched (window) | +196417 / -15734 |
| PR TAT (create -> merge, median / p75) | 0.4h / 1.2h (127/127 under 24h) |
| Multi-repo flow span TAT (median) | 2.9d across 9 flows (5 under 72h) |
| Avg ticket age (first commit -> Ready for QA / Closed) | **20.9d** (median 6.5d, 9 tickets; 5 under 7d) |
| Merged PRs with no Jira key in title | 49.6% (63 PRs) - Jira often missing/late/wrong |
| Jira done (window) | 2 |
| Jira open now | 4 |
| Jira comments authored | 45 on 18 issues |
| Comments helping others (not assignee) | 38 on 15 issues |
| Reporter (not assignee) | 7 |
| Reopened in window | 1 (50.0%) |
| PR rework (same ticket 2+ PRs) | 22 tickets (19 follow-up after merge, 1 retry after closed) |
| Near-duplicate PR titles (same repo) | 25 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 47 active members - 0.314 days/PR, 624 merged PRs in ~6.9 months (source: pr-cadence-top10, as of 2026-09-22). |
| Does not ship volume | **FALSE** | Career: 642 merged / 700 PRs across trusttai; last 30d: 149 PRs, 14 repos, +196417/-15734 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 9 multi-repo flows shipped with median span TAT 2.9d (first PR open -> last merge across repos); 5 under 72h, 6 under 7d. PR create->merge median 0.4h (p75 1.2h); 127/127 merged in under 24h. Caveat: 49.6% of merged PRs in window have no Jira key in title - Jira is often missing/late/wrong, so flow evidence is GitHub TAT-first, not journey labels or 'touched N repos'. |
| Recurring quality / reopen problem | **CONTEXT** | 1 issues reopened in scope (last 30d) (~50.0% vs 2 done). Currently reopened: 1. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. Jira reopen % understates when tickets are never filed or not updated. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 22 tickets with 2+ authored PRs in window; 19 had follow-up after a merge; 1 retry after closed-unmerged; 25 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 45 comments authored on 18 issues in window; 15 of those were not assigned to Ashutosh (38 help comments). Also reporter on 7 issues assigned to others; 9 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 6 issues with RCA Remarks authored on the ticket, 1 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-task-allocation` | 34 |
| `trustt-platform-lib` | 30 |
| `trustt-platform-creditcard-management` | 23 |
| `trustt-platform-banking-origination` | 11 |
| `trustt-platform-actor` | 11 |
| `trustt-platform-authorization` | 9 |
| `trustt-platform-initial-setup` | 8 |
| `trustt-platform-masterdata` | 8 |
| `trustt-platform-api-gateway` | 4 |
| `trustt-platform-india-stack` | 4 |
| `trustt-platform-approval` | 2 |
| `trustt-platform-consents` | 2 |

#### Multi-repo tickets

Listed for context only - repo count alone is not proof of flow understanding. Prefer **flow span TAT** (first PR open -> last merge) below.

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-8930 | 5 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation |
| HDP-11579 | 3 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11535 | 2 | trustt-platform-authorization, trustt-platform-task-allocation |
| HDP-11729 | 2 | trustt-platform-actor, trustt-platform-task-allocation |
| HDP-8937 | 2 | trustt-platform-actor, trustt-platform-authorization |
| HDP-8961 | 2 | trustt-platform-actor, trustt-platform-task-allocation |
| HDP-9003 | 2 | trustt-platform-actor, trustt-platform-task-allocation |

#### Multi-repo flow span TAT

Hours from first authored PR open to last merge for the same ticket across 2+ repos. This is speed-of-shipping a flow, not 'touched'.

| Ticket | Repos | Span | First PR | Last merge |
| --- | --- | --- | --- | --- |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 2 | 0.2h | 2026-09-23 | 2026-09-23 |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | 2 | 20.3h | 2026-08-27 | 2026-08-28 |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | 5 | 23.6h | 2026-09-22 | 2026-09-23 |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 3 | 1.9d | 2026-09-16 | 2026-09-18 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | 2 | 2.9d | 2026-09-15 | 2026-09-18 |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | 5 | 5.7d | 2026-09-02 | 2026-09-08 |
| [HDP-8961](https://novopay.atlassian.net/browse/HDP-8961) | 2 | 7.1d | 2026-09-01 | 2026-09-08 |
| [HDP-8937](https://novopay.atlassian.net/browse/HDP-8937) | 2 | 13.1d | 2026-08-27 | 2026-09-09 |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | 5 | 28.0d | 2026-08-26 | 2026-09-23 |

#### Ticket age (first commit -> Ready for QA / Closed)

Start = earliest commit on authored PRs with the ticket key in the title. End = first Jira transition to Ready for QA or Closed/Done/Resolved. Window filter uses the end date.

| Ticket | Age | First commit | Ready / Closed | End status |
| --- | --- | --- | --- | --- |
| [HDP-9423](https://novopay.atlassian.net/browse/HDP-9423) | 0.2h | 2026-09-18 | 2026-09-18 | Ready for QA |
| [HDP-11725](https://novopay.atlassian.net/browse/HDP-11725) | 0.5h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | 1.6h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11477](https://novopay.atlassian.net/browse/HDP-11477) | 5.0h | 2026-09-15 | 2026-09-15 | Ready for QA |
| [HDP-10752](https://novopay.atlassian.net/browse/HDP-10752) | 6.5d | 2026-08-18 | 2026-08-25 | Ready for QA |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 12.8d | 2026-09-04 | 2026-09-17 | Ready for QA |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 14.1d | 2026-09-09 | 2026-09-24 | Ready for QA |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | 24.0d | 2026-08-25 | 2026-09-18 | Ready for QA |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | 129.9d | 2026-04-30 | 2026-09-07 | Ready for QA |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 14 | 10 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | fix(kyc-engine): promote ddp-bkup-qa to ddp-qa - KYC En \| fix(kyc-engine): promote ddp-bkup-qa to ddp-qa - KYC En \| fix(kyc-engine): map KYC Engine status filler2 to Final |
| [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930) | Follow-up after merge | 8 | 8 | trustt-platform-actor, trustt-platform-api-gateway, trustt-platform-initial-setup, trustt-platform-masterdata, trustt-platform-task-allocation | [QA] fix: getEmployeeCorporateIdForUser for BKYC admin  \| [QA] fix: BKYC corporate file mapping, admin scope, and \| [QA] fix: seed BKYC entitled corporate config keys (HDP |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 5 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [UAT] HDP-11729: expose assignedAgentPincode on getTask \| [UAT] HDP-11729: return OFFICE pincode on getAgentsById \| [QA] HDP-11729: expose assignedAgentPincode on getTaskL |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Retry after closed | 4 | 0 | trustt-platform-authorization | [UAT] fix: hide BKYC KYC List for non-entitled corporat \| [QA] fix: hide BKYC KYC List for non-entitled corporate \| [UAT] fix: hide BKYC KYC List for non-entitled corporat |
| [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [QA] fix: map annexure client, product, and geo onto AD \| [QA] fix: sort ADM1 task list by tab instead of last up \| [QA] fix: fill assigned agent code/name and ADM1 area c |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | Follow-up after merge | 3 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [PROD] fix: keep time on Excel Timestamp columns (HDP-1 \| [UAT] fix: keep time on Excel Timestamp columns (HDP-10 |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Follow-up after merge | 3 | 3 | trustt-platform-authorization, trustt-platform-task-allocation | [UAT] fix: restrict BKYC assign / re-assign / unassign  \| [QA] fix: restrict BKYC assign / re-assign / unassign t \| [QA] fix(uam): split BKYC Management feature by role gr |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time \| [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [QA] fix(infra-platform): map missing request part/valu \| [QA] fix(infra-platform): map missing request part/valu |
| (title match) | Near-duplicate title | 2 | 0 | trustt-platform-creditcard-management | [UAT] fix: migrate KYC Engine Jackson 2 ObjectMapper to \| [QA] fix: migrate KYC Engine Jackson 2 ObjectMapper to  |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [QA] fix(addon-card): tight CDATA wrapping for requestX \| [UAT] fix(addon-card): tight CDATA wrapping for request |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-creditcard-management | [QA] fix: persist KYC Engine initiate and poll in trans \| [UAT] fix: persist KYC Engine initiate and poll in tran |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-approval | [UAT] fix: hide closed applications from Pending Action \| [QA] fix: hide closed applications from Pending Actions |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-creditcard-management | [QA] fix: migrate KYC Engine Jackson 2 ObjectMapper to  \| [PROD] fix: migrate KYC Engine Jackson 2 ObjectMapper t |

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
| [HDP-11011](https://novopay.atlassian.net/browse/HDP-11011) | Story | On Hold | PROD New Requirement - Tenant-wise FD Report with Dynamic Filters | 2026-09-17 |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | Bug | On Hold | DSA Admin - Agent Lead Report dropdown displays CC Report entries instead of Agent Lead Report options | 2026-09-02 |

#### Reopened in this window - why

| Key | Now | Reopens | Bucket | RCA / notes |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Reopened | 1 | Log/masking (product OK) | QA/UAT infra-logging JSON masks for photo/auth_ref_code used ( +), which in JSON has almost no <, so they greedily ate sibling fields (poi.p |

### 2. Comparative analysis (Last 30 days)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.303 | 128 | 642 | 7.0 | 3 | 1 | #1 |
| Abhishek | 0.416 | 56 | 953 | 14.5 | 7 | 0 | #2 |
| Harini | 0.859 | 56 | 654 | 19.0 | 33 | 0 | #3 |

---

## Last 7 days

[All time](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#all-time) · [Last 30 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-30-days) · [Last 7 days](https://mdshare.trustt.com/md/s/pbNeFBryyGmF#last-7-days) · [Back to top](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

### 1. About Ashutosh (Last 7 days)

| Metric | Value |
| --- | --- |
| Org PR cadence rank (career) | **#1** of 47 |
| Days per PR (career) | **0.314** |
| Career merged PRs | **642** / 700 total |
| PRs in window (7d) | **57** created, **38** merged, **8** repos |
| Lines touched (window) | +123049 / -7047 |
| PR TAT (create -> merge, median / p75) | 0.2h / 2.3h (38/38 under 24h) |
| Multi-repo flow span TAT (median) | 1.1d across 4 flows (4 under 72h) |
| Avg ticket age (first commit -> Ready for QA / Closed) | **8.5d** (median 6.4d, 6 tickets; 3 under 7d) |
| Merged PRs with no Jira key in title | 23.7% (9 PRs) - Jira often missing/late/wrong |
| Jira done (window) | 0 |
| Jira open now | 4 |
| Jira comments authored | 2 on 1 issues |
| Comments helping others (not assignee) | 2 on 1 issues |
| Reporter (not assignee) | 2 |
| Reopened in window | 1 (0.0%) |
| PR rework (same ticket 2+ PRs) | 10 tickets (8 follow-up after merge, 1 retry after closed) |
| Near-duplicate PR titles (same repo) | 11 |

#### Claim vs evidence

| Leadership claim | Verdict | Evidence |
| --- | --- | --- |
| Slow / low output | **FALSE** | Org PR cadence rank #1 of 47 active members - 0.314 days/PR, 624 merged PRs in ~6.9 months (source: pr-cadence-top10, as of 2026-09-22). |
| Does not ship volume | **FALSE** | Career: 642 merged / 700 PRs across trusttai; last 7d: 57 PRs, 8 repos, +123049/-7047 lines. |
| Does not understand cross-service flows | **CHALLENGED** | 4 multi-repo flows shipped with median span TAT 1.1d (first PR open -> last merge across repos); 4 under 72h, 4 under 7d. PR create->merge median 0.2h (p75 2.3h); 38/38 merged in under 24h. Caveat: 23.7% of merged PRs in window have no Jira key in title - Jira is often missing/late/wrong, so flow evidence is GitHub TAT-first, not journey labels or 'touched N repos'. |
| Recurring quality / reopen problem | **CONTEXT** | 1 issues reopened in scope (last 7d) (~0.0% vs 0 done). Currently reopened: 1. Each case listed with status trajectory and RCA bucket - inspect before attributing to 'AI' or 'flow ignorance'. Jira reopen % understates when tickets are never filed or not updated. |
| Same work re-raised as new PRs (missed items) | **CONTEXT** | 10 tickets with 2+ authored PRs in window; 8 had follow-up after a merge; 1 retry after closed-unmerged; 11 near-duplicate title groups (same repo). See PR rework table - not all are defects (multi-repo / intentional follow-ups also land here). |
| Only counted when assignee (ignores help via comments) | **FALSE** | 2 comments authored on 1 issues in window; 1 of those were not assigned to Ashutosh (2 help comments). Also reporter on 2 issues assigned to others; 1 issues with status moved by him. |
| Too dependent on AI (implies no ownership) | **UNPROVEN** | AI usage is not measurable from GitHub/Jira. What is measurable: 6 issues with RCA Remarks authored on the ticket, 0 bugs closed as assignee, and authored tooling (Bob, skills, trackers) that other engineers use. Judge from RCA depth + multi-repo ownership below - not from tool presence. |

#### Where work lands (repos)

| Repository | PRs authored |
| --- | --- |
| `trustt-platform-lib` | 16 |
| `trustt-platform-creditcard-management` | 10 |
| `trustt-platform-banking-origination` | 9 |
| `trustt-platform-task-allocation` | 9 |
| `trustt-platform-authorization` | 5 |
| `trustt-platform-initial-setup` | 3 |
| `trustt-platform-masterdata` | 3 |
| `trustt-platform-actor` | 2 |

#### Multi-repo tickets

Listed for context only - repo count alone is not proof of flow understanding. Prefer **flow span TAT** (first PR open -> last merge) below.

| Ticket | Repos | Repositories |
| --- | --- | --- |
| HDP-7350 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-7351 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata |
| HDP-11579 | 3 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib |
| HDP-11729 | 2 | trustt-platform-actor, trustt-platform-task-allocation |

#### Multi-repo flow span TAT

Hours from first authored PR open to last merge for the same ticket across 2+ repos. This is speed-of-shipping a flow, not 'touched'.

| Ticket | Repos | Span | First PR | Last merge |
| --- | --- | --- | --- | --- |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 2 | 0.2h | 2026-09-23 | 2026-09-23 |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | 5 | 23.6h | 2026-09-22 | 2026-09-23 |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | 5 | 1.2d | 2026-09-22 | 2026-09-23 |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 3 | 1.9d | 2026-09-16 | 2026-09-18 |

#### Ticket age (first commit -> Ready for QA / Closed)

Start = earliest commit on authored PRs with the ticket key in the title. End = first Jira transition to Ready for QA or Closed/Done/Resolved. Window filter uses the end date.

| Ticket | Age | First commit | Ready / Closed | End status |
| --- | --- | --- | --- | --- |
| [HDP-9423](https://novopay.atlassian.net/browse/HDP-9423) | 0.2h | 2026-09-18 | 2026-09-18 | Ready for QA |
| [HDP-11725](https://novopay.atlassian.net/browse/HDP-11725) | 0.5h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | 1.6h | 2026-09-22 | 2026-09-22 | Ready for QA |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | 12.8d | 2026-09-04 | 2026-09-17 | Ready for QA |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | 14.1d | 2026-09-09 | 2026-09-24 | Ready for QA |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | 24.0d | 2026-08-25 | 2026-09-18 | Ready for QA |

#### PR rework / repeat raises

Same ticket with multiple authored PRs, or near-duplicate titles in the same repo (often a missed item in an earlier PR).

| Ticket / match | Signal | PRs | Merged | Repos | PR titles |
| --- | --- | --- | --- | --- | --- |
| [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) | Follow-up after merge | 10 | 8 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11579](https://novopay.atlassian.net/browse/HDP-11579) | Follow-up after merge | 5 | 4 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-lib | [QA] KYC engine step 1/2 - banking-origination: bank KY \| [QA] KYC engine step 2/2 - creditcard-management: send  \| [QA] KYC engine step 1/3 - lib: no code change, branch  |
| [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351) | Follow-up after merge | 5 | 5 | trustt-platform-banking-origination, trustt-platform-creditcard-management, trustt-platform-initial-setup, trustt-platform-lib, trustt-platform-masterdata | [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC \| [PROD] [HDP-7350] [HDP-7351] KYC Engine - EKYC + CKYC |
| [HDP-11729](https://novopay.atlassian.net/browse/HDP-11729) | Follow-up after merge | 4 | 4 | trustt-platform-actor, trustt-platform-task-allocation | [UAT] HDP-11729: expose assignedAgentPincode on getTask \| [UAT] HDP-11729: return OFFICE pincode on getAgentsById \| [QA] HDP-11729: expose assignedAgentPincode on getTaskL |
| [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732) | Follow-up after merge | 4 | 4 | trustt-platform-task-allocation | [UAT] fix(task): keep tenant and STAN across MapMyIndia \| [QA] fix(task): keep tenant and STAN across MapMyIndia  \| [UAT] fix(task): keep BKYC customer map pin inside the  |
| [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743) | Retry after closed | 4 | 0 | trustt-platform-authorization | [UAT] fix: hide BKYC KYC List for non-entitled corporat \| [QA] fix: hide BKYC KYC List for non-entitled corporate \| [UAT] fix: hide BKYC KYC List for non-entitled corporat |
| [HDP-10807](https://novopay.atlassian.net/browse/HDP-10807) | Follow-up after merge | 3 | 2 | trustt-platform-lib | [UAT] fix: keep time on Excel Timestamp columns (HDP-10 \| [PROD] fix: keep time on Excel Timestamp columns (HDP-1 \| [UAT] fix: keep time on Excel Timestamp columns (HDP-10 |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim \| [UAT] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+tim |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-lib | [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time \| [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time |
| (title match) | Near-duplicate title | 2 | 0 | trustt-platform-creditcard-management | [UAT] fix: migrate KYC Engine Jackson 2 ObjectMapper to \| [QA] fix: migrate KYC Engine Jackson 2 ObjectMapper to  |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-creditcard-management | [QA] fix: migrate KYC Engine Jackson 2 ObjectMapper to  \| [PROD] fix: migrate KYC Engine Jackson 2 ObjectMapper t |
| (title match) | Near-duplicate title | 2 | 0 | trustt-platform-banking-origination | [UAT] fix: add RBG kyc_detail CREATE (V9000006) before  \| [QA] fix: add RBG kyc_detail CREATE (V9000006) before E |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [UAT] fix: stop JSON log masks from swallowing photo an \| [QA] fix: stop JSON log masks from swallowing photo and |
| (title match) | Near-duplicate title | 2 | 0 | trustt-platform-banking-origination | [QA] fix: add RBG kyc_detail CREATE (V9000006) before E \| [PROD] fix: add RBG kyc_detail CREATE (V9000006) before |
| (title match) | Near-duplicate title | 2 | 2 | trustt-platform-lib | [QA] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+time \| [PROD] fix: ETB KYC Engine EKYC FILLER4 always NVKYC+ti |
| (title match) | Near-duplicate title | 2 | 1 | trustt-platform-creditcard-management | [UAT] fix: KYC Engine Jackson 3 Boot 4 via ddp-bkup-uat \| [QA] fix: KYC Engine Jackson 3 Boot 4 via ddp-bkup-qa |
| [HDP-10752](https://novopay.atlassian.net/browse/HDP-10752) | Multi-PR same ticket | 2 | 1 | trustt-platform-creditcard-management | [PROD] LOC MIS column order journeyName -> journeyType -> \| [PROD] LOC MIS column order (HDP-10752) + device column |
| [HDP-11397](https://novopay.atlassian.net/browse/HDP-11397) | Follow-up after merge | 2 | 2 | trustt-platform-task-allocation | [QA] fix: stamp who acted on the ADM6 activity log (HDP \| [UAT] fix: stamp who acted on the ADM6 activity log (HD |

#### Jira help via comments (not assignee)

Tickets owned by someone else where Ashutosh still commented (unblocks / guidance).

| Key | Assignee | My comments | Last | Snippet |
| --- | --- | --- | --- | --- |
| [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) | Salini PD | 2 | 2026-09-18 16:05:44 | HDP-11535 - FE change needed for BKYC menu Context Bank logins were seeing Assign / Re-assign, and permission clean-ups  |

#### Reopened in this window - why

| Key | Now | Reopens | Bucket | RCA / notes |
| --- | --- | --- | --- | --- |
| [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) | Reopened | 1 | Log/masking (product OK) | QA/UAT infra-logging JSON masks for photo/auth_ref_code used ( +), which in JSON has almost no <, so they greedily ate sibling fields (poi.p |

### 2. Comparative analysis (Last 7 days)

| Person | Days/PR (career) | Window merged | Career merged | Span (mo) | Jira done (window) | Reopened (window) | Group rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Ashutosh** | 0.303 | 38 | 642 | 7.0 | 0 | 1 | #1 |
| Abhishek | 0.416 | 13 | 953 | 14.5 | 0 | 0 | #3 |
| Harini | 0.859 | 14 | 654 | 19.0 | 5 | 0 | #2 |

---

_Generated 2026-09-24 02:07. Peers: trusttAshutosh, trustt-abhishek, Harini-Trustt._
