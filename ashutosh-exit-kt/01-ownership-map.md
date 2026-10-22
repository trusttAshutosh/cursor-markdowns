# 01 - Ownership map

What a successor must take from Ashutosh. Code how-it-works is in git.

**GitHub:** `trusttAshutosh`  
**Jira:** Ashutosh Kumar

## Must take (walks out with him)

| Area | What he uniquely holds | Git already has |
| --- | --- | --- |
| BKYC auto-assign | Why 10 auto / 15 manual, pincode = office address not agent column, visit owner = `employee.corporate_id` not `user.id` / `actor.id` | Tickets HDP-8949-8953, solution-document |
| BKYC admin APIs | ADM1 leftover list, ADM2 eligible agents, ADM3 assign/reassign/unassign, ADM6 activity - and that FE screens existed before mutate APIs | HDP-9003-9005, HDP-9551 |
| BKYC assign SMS | Batch vs manual-window; which notification codes; join `task.customer_mobile` = `sms_log.msisdn` (no task_id FK) | HDP-8954, `BKYC_SMS_SCENARIO_MESSAGES.md` |
| Bank response CSV after assign | What bank actually consumes vs what we generate | HDP-8956, HDP-8957 |
| CC / KYC Engine | eKYC vs cKYC only (no Digilocker); `filler1` mobile_match rules; bank-facing evidence must be real applogs | CC repo docs |
| Product onboarding doc | Master copy in CC repo + mdshare id `6abd71df5c3812e8ca51ab39` must stay in sync | `.cursor/rules/onboarding-doc-mdshare-sync.mdc` |
| Agent OS | Cursor rules, Bob as proof-only, remote-db.env, continual-learning **off on purpose** | `AGENTS.md`, `BOB_GUIDE.md`, `cursor-markdowns` |
| Flyway process | Common-scripts first; TaskAlloc DDL only in initial-setup (HDP-8967 collision) | `AGENTS.md` + flyway rules |
| PR / QA-UAT promote | Never open conflicting feature-to-QA PR; bkup path; never 0-file PR; `[QA]`/`[UAT]`/`[PROD]` title prefix | `AGENTS.md` |

## Shared / do not re-KT as "his"

| Area | Owner to confirm | Note |
| --- | --- | --- |
| BKYC ingest + ADM7 upload + close file | Abhishek Puranik (`trustt-abhishek`) - **leaving** | Get his KT separately; Ashutosh is not the ingest owner |
| BKYC service/schema/consent | Deepankar | |
| Agent list/detail/bio/submit | Harini | |
| Admin PWA | Anshu / Salini | |
| APK | Shailendra / Vinay | |
| Jenkins TaskAlloc | Arnold | |

## Repos he actually lives in

Keep this list current. Do not add a repo because he reviewed one PR.

- `novopay-platform-creditcard-management` (and `*-ddp-uat` clone when used)
- `trustt-platform-task-allocation`
- `novopay-platform-initial-setup` (TaskAlloc Flyway)
- `trustt-platform-masterdata` / `novopay-platform-masterdata-management` (common-scripts)
- `novopay-platform-lib`
- `novopay-platform-api-gateway`
- `novopay-platform-actor` (when BKYC/Actor eligibility)
- `bob-the-builder`
- `Desktop/novopay` workspace + `Desktop/cursor-markdowns`

## [FILL] areas he still needs to declare

- [ ] Anything he is the silent owner of outside BKYC assign / CC / agent OS (reports? gateway v2? actor UAM?)
- [ ] Which QA/UAT Jenkins jobs only he knows how to retry
- [ ] Which mdshare docs he publishes besides onboarding + BKYC tracker
