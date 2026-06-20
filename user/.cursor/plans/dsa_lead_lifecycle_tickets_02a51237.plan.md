---
name: DSA Lead Lifecycle Tickets
overview: Four product-ready tickets for DSA/DSE lead lifecycle (60-day cleanup, report accuracy, DSA deactivation, office closure), with engineering detail kept in a separate section for ticket comments.
todos:
  - id: ticket-1-purge
    content: "Ticket 1: Auto-remove stale leads from DSE after 60 days"
    status: pending
  - id: ticket-2-report
    content: "Ticket 2: DSA Admin report shows only active leads"
    status: pending
  - id: ticket-3-dsa-deact
    content: "Ticket 3: DSA deactivation - disable users, keep lead history, allow re-onboarding"
    status: pending
  - id: ticket-4-office-close
    content: "Ticket 4: Office closure - keep attribution in reports, allow staff re-onboarding"
    status: pending
isProject: false
---

# DSA Lead Lifecycle - Finalized After Product Feedback

Use the **Product ticket** blocks below when creating Jira/Linear items. Copy the matching **Technical comment** and **QA reference** blocks into the ticket as separate comments.

**Delivery order:** Ticket 1 → Ticket 3

**Assumptions to confirm with product:**

- Lead freshness source timestamp is one final field (`created_on` or `submitted_on`) and will be used consistently across dashboard, admin portal, and deletion validation.
- Agent deletion is blocked only when at least one lead is both active and within 60 days.
- Ticket 2 behavior is merged into Ticket 1 (no standalone implementation ticket for report alignment).
- DSA lifecycle semantics are final for both actions:
  - DELETE DSA: mapped agents/admins are deleted under old DSA mapping.
  - DISABLE DSA: mapped agents/admins remain in system but cannot access; re-onboard flow deletes old mapping first, then creates new mapping.
- Office-level functionality is not a standalone feature and follows DSA-level lifecycle handling.

**Branch check before build:** Compare against `ddp-prod` (backend) and `dsa-prod` (frontend, if UI changes).

### Jira journey dropdown - quick reference


| Ticket | Select (multiple allowed)                                               |
| ------ | ----------------------------------------------------------------------- |
| **1**  | Credit Card, Agent App, Agent, Admin Portal, Platform                   |
| **2**  | Merged into Ticket 1 (do not use standalone)                            |
| **3**  | Corporate, Credit Card, Admin Portal, Agent, Agent App, ESO, Onboarding |
| **4**  | Closed - not feasible (do not use standalone)                           |


**Never select for any of these four tickets:** Add-on Card, Loan On Card, ALM, AEPS, savings/loan/deposit product journeys, Complaint Management, Data Migration, Technical Backlog, Other (unless PM explicitly expands scope).

---

## Ticket 1

### Product ticket

**Title:** Enforce 60-day lead freshness for Agent Dashboard, Admin Portal, and agent deletion validation

**Description:**

Over time, DSEs accumulate customer leads that are no longer being worked. We need a background process that, on a regular schedule, identifies credit card leads that have been with a DSE for more than 60 days and are no longer active, and releases them from that DSE’s ownership.

Important behaviour:

- Leads that are still active and being worked must **not** be released.
- When a lead is released, we still keep the full history of the application (who the DSE was, which DSA, partner details, etc.) for reporting and audit.
- The DSE should no longer see or be blocked by these old leads when trying to deactivate or move to another partner.
- Only leads within the last 60 days should be operationally accessible in:
  - Agent Dashboard
  - Admin Portal
- Agent deletion should be blocked only when a lead is both:
  - active, and
  - within 60 days
- Lead freshness should use one source timestamp consistently (`created_on` or `submitted_on`).

**Acceptance criteria:**

- Leads older than 60 days that are not active are no longer tied to the DSE.
- Active leads remain tied to the DSE.
- Only in-scope (<=60-day) leads are accessible in Agent Dashboard and Admin Portal.
- Agent deletion is blocked only by active + <=60-day leads.
- Historical application and attribution data is unchanged.
- Process runs automatically on a schedule and can be run again safely without duplicate impact.

**Depends on:** Nothing (first ticket)

**Jira journey field - select these (multiple):**

- **Credit Card** (primary - CC customer leads / `transaction_sub_type = CC`)
- **Agent App** (DSE CC home, resume/pending lists)
- **Agent** (DSE entity, deactivation active-lead check)
- **Admin Portal** (lead visibility/access)
- **Platform** (scheduled batch job registration)

**Do not select:** Add-on Card, Loan On Card, Reports (standalone ticket), Corporate, Onboarding, ESO, Agent PWA (unless your project treats PWA same as Agent App - then add Agent PWA instead of or in addition to Agent App), savings/loan/deposit journeys, AEPS, ALM, etc.

**Journeys impacted:**


| Journey                               | Who                       | What changes                                                                                                           |
| ------------------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| DSE assisted credit card application  | DSE (agent app)           | Old idle leads (>60 days) drop off the DSE’s active ownership; customer can still be assisted if a new lead is started |
| CC resume / pending list              | DSE (agent app - CC home) | Resume and pending counts/lists no longer treat purged leads as “my” open work                                         |
| Admin Portal lead access              | Ops / DSA Admin           | Only leads within 60 days are operationally accessible                                                                 |
| DSE deactivation                      | Ops / DSA Admin           | Deletion/deactivation checks consider only leads that are both active and within 60 days                               |
| DSE lead reassignment (manual)        | Ops / backoffice          | Remains the manual path; purge is the automatic equivalent for old idle leads                                          |
| Bulk CC lead upload                   | DSE / ops                 | Unaffected for new uploads; only aged inactive linked rows are released                                                |
| *(background)* Scheduled lead cleanup | System                    | New nightly/scheduled run - no user-facing screen                                                                      |


*Out of scope for this ticket:* Jan Samarth link-only journey (no DSE assistor), DSA delete/disable lifecycle, office-level lifecycle.

---

### Technical comment (attach to Ticket 1)

**Journey / flow map:**


| Flow                                 | API / entry                                                                                  | Module                        |
| ------------------------------------ | -------------------------------------------------------------------------------------------- | ----------------------------- |
| CC assisted application              | `manageCreditCardApplication` → `createOrUpdateCCApplicationProcessor`                       | creditcard-management         |
| CC resume list                       | `getCreditCardTransactionHistory` (`function_sub_code=RESUME`) → `getTnxResumeListProcessor` | creditcard-management         |
| Active-lead check (deactivate guard) | `getCustomerLeadByDseCode` → `GetCustomerLeadProcessor`                                      | creditcard-management         |
| DSE deactivate guard                 | `updateAgentStatus` (DEACTIVATE) → `checkAgentDeletableBasedOnActiveLeadsProcessor`          | actor (`dsa_agent_orc.xml`)   |
| Manual lead move                     | `uploadLeadReassignFile` → `LeadReassignAuditProcessor`                                      | creditcard-management         |
| Bulk CC ingest                       | `batchValidateLeads` / bulk upload                                                           | creditcard-management         |
| **New** scheduled purge              | TBD batch → `PurgeStaleDseLeadsBatchProcessor`                                               | creditcard-management + batch |


**Frontend (dsa-prod):** `novopay-platform-agent-webapp`  - `/CC` `CCHomeScreen` (resume/pending lists).

**Modules:** `novopay-platform-creditcard-management`, `novopay-platform-batch`, `novopay-platform-masterdata-management`

**Baseline:** No CC lead purge exists today. Reuse patterns from:

- `[GetCustomerLeadProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/GetCustomerLeadProcessor.java)`  - active = consent not `PENDING`/`EXPIRED`
- `[UpdateCreditCardStatusBatchProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/UpdateCreditCardStatusBatchProcessor.java)`  - batch + `@NovopayConfig` days
- `[LeadReassignAuditProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/LeadReassignAuditProcessor.java)`  - inverse: clear `assistor_`* instead of reassign

**Schema (flyway on `transaction_audit`):**

- `lead_link_status` (`LINKED` | `DELINKED`)
- `delinked_on`, `delink_reason` (e.g. `PURGE_60D`)

**Implementation:**

1. Extract `CustomerLeadEligibilityService` from `GetCustomerLeadProcessor` (consent via `getCustomerConsentStatus`).
2. New `PurgeStaleDseLeadsBatchProcessor`: query CC rows with `assistor_code` set, `created_on` < 60 days (config `cc.lead.purge.interval.days`), `lead_link_status` null/LINKED; skip `APPROVED` / `FAIL`; if not active → clear `assistor_id/code/name/type`, set `DELINKED`.
3. Do **not** update `hierarchy_log_id`, `transaction_hierarchy_log`, or `transaction_audit_attributes`.
4. Register batch in `novopay-platform-batch` DSA migrations (daily off-peak).
5. Config flyway in masterdata: `cc.lead.purge.interval.days` default `60`.
6. Apply same 60-day freshness predicate consistently to Agent Dashboard, Admin Portal, and DSE deletion guard (`active + <=60 days` only).

**Tests:** Unit eligibility + delink; batch idempotency; `hierarchy_log_id` unchanged.

---

### QA reference

**Pre-requisites:** DSA tenant with at least one DSE, test CC leads in mixed states. Ability to run/trigger purge batch manually in QA. DB read access to `transaction_audit`, `transaction_hierarchy_log`, `transaction_audit_attributes`.

**Test data setup (minimum):**


| #   | Lead                | Age      | Consent / status                     | Expected after purge              |
| --- | ------------------- | -------- | ------------------------------------ | --------------------------------- |
| A   | Linked to DSE       | >60 days | Consent EXPIRED or idle (non-active) | Delinked from DSE                 |
| B   | Linked to DSE       | >60 days | Consent PENDING (still active)       | Stays linked                      |
| C   | Linked to DSE       | <60 days | Non-active                           | Stays linked                      |
| D   | Linked to DSE       | >60 days | APPROVED or txn FAIL                 | Stays linked or excluded per spec |
| E   | Bulk-upload CC lead | >60 days | Non-active                           | Delinked (assistor cleared)       |


**Functional tests:**

1. **Happy path - stale lead released**
  - Run purge batch (or wait for schedule).
  - Verify lead A: `assistor_code` cleared on `transaction_audit`; `lead_link_status = DELINKED`; `delink_reason = PURGE_60D` (or agreed value).
  - Verify DSE CC resume/pending list (Agent App) no longer shows lead A.
  - Verify `transaction_hierarchy_log` and attributes unchanged for lead A (DSE/DSA/partner codes same as before).
2. **Active lead protected**
  - Lead B still has `assistor_code` set after batch.
  - DSE still sees lead B in resume/pending counts.
3. **Young lead protected**
  - Lead C unchanged after batch.
4. **Portal/dashboard freshness**
  - Verify Agent Dashboard and Admin Portal only show operational leads within 60 days.
  - Verify >60-day leads are not operationally accessible in both channels.
5. **DSE deactivation after purge**
  - DSE with only stale (>60-day) leads: deactivate/delete succeeds (no error 4000360).
  - DSE with active + <=60-day linked lead: deactivate/delete still blocked.
6. **Idempotency**
  - Run batch twice on same data: no duplicate errors; already-delinked rows not reprocessed incorrectly.
7. **Manual reassignment still works**
  - Upload lead reassign file for a non-delinked lead: existing flow unaffected.

**DB checks (sample):**

```sql
-- After purge on lead A
SELECT assistor_code, lead_link_status, delink_reason, hierarchy_log_id FROM transaction_audit WHERE client_reference_code = '<CRN-A>';
SELECT dse_code, dsa_code, partner_id FROM transaction_hierarchy_log WHERE id = <hierarchy_log_id>;
```

**Regression:** New CC application creation, bulk upload, consent flow - unaffected.

**Out of scope for this ticket:** DSA delete/disable lifecycle, office-level lifecycle.

---

## Ticket 2

### Product ticket

**Status:** Merged into Ticket 1 (no standalone implementation required).

**Title:** DSA Admin report should only show active leads

**Description:**

After we start releasing old leads from DSEs (Ticket 1), the DSA Admin credit card report must only show leads that are still active and still linked to a DSE. Released or archived leads should not appear in day-to-day operational reporting.

The report should continue to show correct DSE, DSA Admin, office, and partner information for the leads that **are** included.

**Acceptance criteria:**

- DSA Admin downloadable/operational report lists only active, linked leads.
- Leads released under the 60-day process do not appear.
- Partner and hierarchy details on included rows remain accurate.
- Manual MIS export (if used by ops) follows the same rules.

**Depends on:** Ticket 1

**Jira journey field - select these (multiple):**

- **Credit Card** (primary - report data source)
- **Reports** (DSA Admin CC transaction report / MIS)
- **Admin Portal** (DSA Admin downloads export from backoffice)

**Do not select:** Agent App (unless follow-up scopes DSE list filter), Corporate, Onboarding, Platform, ESO, Add-on Card, Loan On Card, savings/loan/deposit journeys, etc.

**Journeys impacted:**


| Journey                                   | Who                             | What changes                                                                                         |
| ----------------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------- |
| DSA Admin CC transaction report download  | DSA Admin (portal / backoffice) | Export/list shows only active leads still tied to a DSE                                              |
| DSA Admin analytics / Superset dashboards | DSA Admin                       | Same data rules if fed from the same report API                                                      |
| Manual MIS / ops export                   | Operations                      | SQL MIS export aligned with the same “active leads only” rule                                        |
| DSE CC home / resume list                 | DSE (agent app)                 | *Optional follow-up* - only if product wants the same filter on the agent app (not in default scope) |


*Out of scope for this ticket:* Lead purge batch itself (Ticket 1), DSA deactivation, office closure, new CC application creation.

---

### Technical comment (attach to Ticket 2)

**Journey / flow map:**


| Flow                        | API / entry                                                                  | Module                                    |
| --------------------------- | ---------------------------------------------------------------------------- | ----------------------------------------- |
| DSA Admin report download   | `creditCardTransactionReport` → `TransactionReportProcessor` → `DSACCReport` | creditcard-management                     |
| DSA Admin list (non-export) | Same orchestration `common_getCreditCardTransactionHistory.xml`              | creditcard-management                     |
| Ops MIS export              | `cc_lead_mis_export.sql` (manual)                                            | trustt-platform-ddp-manual-report-queries |
| Superset / analytics        | Guest token + dashboards (if sourced from same CC data)                      | actor / api-gateway                       |


**Frontend:** DSA Admin portal / Superset (validate on `dsa-prod`); agent app CC home only if scoped.

**Modules:** `novopay-platform-creditcard-management`, `trustt-platform-ddp-manual-report-queries`

**Touch points:**

- `[TransactionListReportRowMapper.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/dao/TransactionListReportRowMapper.java)`  - `getDSACCTransactionsReportList` / `applyDataFilter`
- `[DSACCReport.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/reports/impl/DSACCReport.java)`  - API `creditCardTransactionReport`
- `[cc_lead_mis_export.sql](trustt-platform-ddp-manual-report-queries/sql/cc_lead_mis_export.sql)`

**SQL filters (base subquery):**

- `ta.assistor_code IS NOT NULL AND <> ''`
- `lead_link_status IS NULL OR = 'LINKED'`
- For DSA Admin scope: exclude terminal (`application_status != APPROVED`, `txn_status != FAIL`)

**Active-lead filter:** SQL cannot call consent API. Prefer precomputed `is_active_lead` flag (updated by purge/consent batch)  - option B: post-filter via `CustomerLeadEligibilityService` (slower).

**Optional:** Align `GetTnxResumeListProcessor` / DSE dashboard if product wants UI parity.

**Tests:** Extend `[DSACCReportTest](novopay-platform-creditcard-management/src/test/java/in/novopay/creditcard/reports/impl/DSACCReportTest.java)`.

---

### QA reference

**Pre-requisites:** Ticket 1 deployed (or manually delink test leads). DSA Admin login with report download access. Mix of linked active, linked inactive, and delinked CC leads under same DSA.

**Test data setup:**


| #   | Lead state                            | In report?         |
| --- | ------------------------------------- | ------------------ |
| F   | Active + linked to DSE                | Yes                |
| G   | Delinked (purge or manual)            | No                 |
| H   | Linked but consent EXPIRED / terminal | No (if non-active) |
| I   | Linked, in progress (active consent)  | Yes                |


**Functional tests:**

1. **DSA Admin report download (portal)**
  - Download CC transaction report for date range covering F, G, H, I.
  - Verify F and I present; G absent; H absent per active-lead rules.
  - For included rows: DSE name/code, DSA Admin, office, partner columns match hierarchy on record.
2. **Delinked lead excluded**
  - Lead G (delinked in Ticket 1): not in export even if within date range.
3. **MIS SQL export (if ops uses it)**
  - Run `cc_lead_mis_export.sql` for same DSA/date range.
  - Same inclusion/exclusion as portal report.
4. **Superset / dashboard (if applicable)**
  - If dashboard uses same API, counts align with report (no delinked leads inflating totals).
5. **Edge cases**
  - Report with only delinked leads: empty file or zero rows (no error).
  - Report date range before/after purge: behaviour consistent.
  - DSA Admin scope: user sees only their partner/employee-scoped data (existing auth unchanged).

**Negative / regression:**

- Active in-progress application still appears while DSE is working it.
- Confirm with product: approved/completed leads included or excluded per final rule.

**Out of scope:** Purge batch (Ticket 1), DSE Agent App resume list (unless scoped), DSA deactivation, office closure.

**Depends on Ticket 1:** Validate after at least one lead delinked via purge.

---

## Ticket 3

### Product ticket

**Title:** Handle DSA Delete vs Disable lifecycle, user access, lead linkage, and re-onboarding transitions

**Description:**

This ticket has two lifecycle branches:

1. **Delete DSA**
  - All agents and DSA admins mapped under that DSA are deleted under that DSA mapping.
  - They can later be re-onboarded under a different DSA.
2. **Disable DSA**
  - Agents/admins remain in system but cannot access the application.
  - If re-onboarding comes from another DSA, old mapping under current DSA is marked deleted first, then onboarding under new DSA is processed.
3. **Common rule**
  - Credit card lead ownership is operationally removed where applicable, but historical UTM/application attribution remains unchanged.

**Acceptance criteria:**

- Delete flow removes old DSA user mappings and supports future re-onboarding under new DSA.
- Disable flow blocks login/access without removing user records immediately.
- Re-onboarding from disabled DSA first closes old mapping, then creates new mapping.
- Historical UTM/application attribution remains unchanged across both flows.

**Depends on:** Ticket 1 (shared lead status model)

**Jira journey field - select these (multiple):**

- **Corporate** (primary - DSA deactivation cascade)
- **Credit Card** (archive CC leads under DSA, preserve attribution)
- **Admin Portal** (ops/DSA Admin triggers DSA deactivate)
- **Agent** (child DSE status / user disable)
- **Agent App** (DSE login blocked until re-onboarded)
- **ESO** (DSE onboarding / re-onboarding under new partner)
- **Onboarding** (DSA Admin employee re-onboarding via UAM)

**Do not select:** Reports (Ticket 2), Platform (batch only in Ticket 1), Add-on Card, Loan On Card, office-specific flows (Ticket 4), savings/loan/deposit journeys, etc.

**Journeys impacted:**


| Journey                                         | Who                         | What changes                                                                                          |
| ----------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------------------------------- |
| DSA delete                                      | Platform / parent DSA Admin | Deleting DSA removes mapped users under old DSA mapping; users can be re-onboarded under another DSA  |
| DSA disable                                     | Platform / parent DSA Admin | Disabling DSA keeps users in system but blocks access                                                 |
| DSE deactivation                                | DSA Admin                   | Can proceed without “active leads” errors for leads already archived by DSA deactivation              |
| DSE onboarding (new partner)                    | DSE                         | Same person can onboard under a different DSA/partner after prior DSA is deactivated                  |
| DSA Admin employee onboarding (new partner)     | DSA Admin / UAM             | Same person can be onboarded under another DSA                                                        |
| DSE / DSA Admin login                           | DSE, DSA Admin              | Logins for deactivated DSA are blocked; new onboarding gets new access                                |
| CC application journey (in-flight & historical) | Customer + DSE              | Applications keep original partner/DSE/DSA Admin attribution on record; live DSE ownership is removed |
| Agent login                                     | DSE                         | Existing users under deactivated DSA cannot log in until re-onboarded                                 |


*Out of scope for this ticket:* 60-day freshness purge implementation (Ticket 1), standalone office-level feature.

---

### Technical comment (attach to Ticket 3)

**Journey / flow map:**


| Flow                       | API / entry                                | Module                                  |
| -------------------------- | ------------------------------------------ | --------------------------------------- |
| DSA corporate lifecycle    | `updateCorporateStatus` (DELETE / DISABLE) | actor (`product_corporate_orc.xml`)     |
| Child DSE terminate        | `updateAgentStatusProcessor` (cascade)     | actor                                   |
| Corp employee terminate    | `updateCorporateEmployeeStatusProcessor`   | actor                                   |
| User disable               | `updateUserAndUserHandleStatusProcessor`   | actor                                   |
| DSE onboarding (re-)       | `createOrUpdateESO` (SUBMIT)               | actor (`dsa_eso_orc.xml`)               |
| DSA Admin onboarding (re-) | `createOrUpdateCorpEmployeeViaUam`         | actor (`dsa_uam_corp_employee_orc.xml`) |
| DSE login                  | `agentLogin`                               | actor (`dsa_agent_self_mgmt.xml`)       |
| CC apps under DSA          | `manageCreditCardApplication` (all stages) | creditcard-management                   |
| **New** bulk lead archive  | `delinkLeadsByDsaCode` (internal)          | creditcard-management                   |


**Frontend:** Agent app login blocked; backoffice DSA status change triggers cascade.

**Modules:** `novopay-platform-actor`, `novopay-platform-creditcard-management`

**Actor - add separate lifecycle handling in `[product_corporate_orc.xml](novopay-platform-actor/deploy/application/orchestration/product_corporate_orc.xml)` for DELETE and DISABLE:

- `updateAgentStatusProcessor`, `updateCorporateEmployeeStatusProcessor`, `updateUserAndUserHandleStatusProcessor`

**Add after cascade:**

1. Internal CC API `delinkLeadsByDsaCode` (`dsa_corporate_code`, reason by action: `DSA_DELETED` / `DSA_DISABLED`).
2. Soft-delete `hierarchy_element` for DSE/DSA_ADMIN under corp (`HierarchyElementRepository.is_deleted = true`).
3. Do **not** delete historical `corporate__partner__mapping` on old applications.

**CC  - bulk delink:**

- Join `transaction_audit` + `transaction_hierarchy_log` where `dsa_code = ?`, still linked.
- Set `lead_link_status=DELINKED`, `delink_reason=DSA_DEACTIVATED`, clear `assistor`_*.
- Do **not** touch `hierarchy_log_id`, attributes, or `thl` rows.

**Guards:** `[GetCustomerLeadProcessor](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/GetCustomerLeadProcessor.java)` and `[CheckAgentDeletableBasedOnActiveLeadsProcessor](novopay-platform-actor/src/main/java/in/novopay/actor/processor/CheckAgentDeletableBasedOnActiveLeadsProcessor.java)`  - skip `DELINKED` leads (no `4000360`).

**Re-onboarding:** Verify `createOrUpdateESO` / `createOrUpdateCorpEmployeeViaUam` allow new hierarchy when prior corp `DEACTIVATED`; update dedupe if mobile/PAN blocked.

**Tests:** DELETE and DISABLE flows both validated; access behavior differs by flow; old mapping transition before re-onboard is enforced; `thl` unchanged.

---

### QA reference

**Pre-requisites:** Two DSAs (DSA-1 to deactivate, DSA-2 for re-onboarding). DSA-1 with at least one DSE, one DSA Admin employee, and multiple CC leads (in-flight + completed). Admin Portal access to deactivate corporate.

**Test data setup:**


| #   | Entity                | State before test                    |
| --- | --------------------- | ------------------------------------ |
| J   | DSA-1                 | ACTIVE with DSE, DSA Admin, CC leads |
| K   | DSE under DSA-1       | ACTIVE, linked CC leads              |
| L   | DSA Admin under DSA-1 | ACTIVE                               |
| M   | CC lead under DSA-1   | In progress (active)                 |
| N   | CC lead under DSA-1   | Completed / idle                     |


**Functional tests:**

1. **DSA DELETE lifecycle**
  - Delete DSA-1 from Admin Portal.
  - Verify mapped users are deleted under old DSA mapping.
  - Verify re-onboarding under DSA-2 succeeds.
2. **DSA DISABLE lifecycle**
  - Disable DSA-1 from Admin Portal.
  - Verify users remain in DB but cannot log in.
  - Re-onboard same user under DSA-2 and verify old mapping is marked deleted first.
3. **CC leads archived, attribution preserved**
  - For leads M and N: `assistor_code` cleared; `lead_link_status = DELINKED`; `delink_reason = DSA_DEACTIVATED`.
  - Verify `transaction_hierarchy_log` unchanged (DSE, DSA Admin, partner, office codes same as before deactivation).
  - Verify `transaction_audit_attributes` unchanged (`partner_id`, `lead_source_key`, etc.).
4. **Login blocked**
  - DSE (K) and DSA Admin (L) cannot log in to Agent App / portal with old credentials.
5. **DSE re-onboarding under new DSA**
  - Onboard same DSE person under DSA-2 via ESO flow.
  - Onboarding succeeds; new hierarchy and partner mapping created.
  - New CC application under DSA-2 works end-to-end.
6. **DSA Admin re-onboarding under new DSA**
  - Onboard same DSA Admin employee under DSA-2 via UAM/onboarding flow.
  - Login and report access work under new DSA.
7. **No false active-lead block**
  - After DSA-1 deactivation, attempt individual DSE deactivate under DSA-1: no error 4000360 from archived leads.
8. **Historical reference**
  - Pull old lead M/N by client reference in DB or historical MIS: original DSA-1 attribution still visible.

**Regression:**

- Deactivating DSA with zero leads still disables users correctly.
- Other active DSAs (DSA-2) unaffected.

**Out of scope:** 60-day freshness implementation (Ticket 1), standalone office-level feature.

**Depends on Ticket 1:** Shared `lead_link_status` / delink model.

---

## Ticket 4

### Product ticket

**Status:** Closed as not feasible by product. Office-level behavior follows DSA delete/disable lifecycle from Ticket 3; no standalone implementation.

**Title:** When an office is closed, keep lead attribution in reports but allow staff to re-join

**Description:**

When a DSA office is marked as closed:

- Reports should still show which DSE or DSA Admin and office were associated with past applications (for MIS and audit).
- Live linkage between that office and its DSEs / DSA Admins should be removed so those people can be onboarded again  - either under the same DSA or a different one.
- Open leads tied to that office should be released from active DSE ownership without changing the stored application/partner details.

**Acceptance criteria:**

- Closing an office removes operational linkage for DSE/DSA Admin under that office.
- Historical reports still show correct DSE, DSA Admin, office, and partner on past leads.
- Affected users can be onboarded under the same or another DSA after closure.
- Open leads at closure are archived/released without altering stored UTM/attribution.

**Depends on:** Tickets 1 and 3

**Jira journey field - select these (multiple):**

- **Corporate** (primary - office belongs to DSA corporate)
- **Credit Card** (delink open CC leads for office; reports keep historical attribution)
- **Admin Portal** (DSA Admin sets office `closed_on`)
- **Onboarding** (DSE / DSA Admin re-onboard under same or new DSA)
- **Agent** (hierarchy unlink for staff at closed office)
- **Agent App** (affected DSE login / lead ownership)
- **ESO** (DSE tied to closed office re-onboarding)

**Do not select:** Reports (operational filter is Ticket 2; historical attribution unchanged), Platform, Add-on Card, Loan On Card, whole-DSA deactivate (Ticket 3), savings/loan/deposit journeys, etc.

**Journeys impacted:**


| Journey                                      | Who                    | What changes                                                                                    |
| -------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------- |
| Office create / update / close               | DSA Admin (backoffice) | Marking `closed_on` triggers removal of live office↔staff linkage                               |
| DSE / DSA Admin onboarding (same or new DSA) | DSE, DSA Admin         | Staff tied to a closed office can be onboarded again under same or different DSA                |
| DSE assisted CC application                  | DSE, Customer          | Open leads for that office are released from active DSE ownership; stored attribution unchanged |
| CC transaction report & MIS                  | DSA Admin, Ops         | Past applications still show DSE, DSA Admin, and office in the report                           |
| DSE deactivation                             | DSA Admin              | Not blocked by leads archived due to office closure                                             |
| Agent login                                  | DSE at closed office   | Access removed until re-onboarded under a valid office/DSA                                      |


*Out of scope for this ticket:* Whole-DSA deactivation (Ticket 3), 60-day purge (Ticket 1).

---

### Technical comment (attach to Ticket 4)

**Status:** Deprecated section - do not implement. Keep for historical context only.

**Journey / flow map:**


| Flow                 | API / entry                                                        | Module                                     |
| -------------------- | ------------------------------------------------------------------ | ------------------------------------------ |
| Office close         | `createOrUpdateCorpOffice` + `UpdateOfficeProcessor` (`closed_on`) | actor (`dsa_createOrUpdateCorpOffice.xml`) |
| Hierarchy unlink     | `hierarchy_element__entity__mapping` (OFFICE-CHANNEL) soft-delete  | actor                                      |
| DSE/Admin re-onboard | `createOrUpdateESO`, `createOrUpdateCorpEmployeeViaUam`            | actor                                      |
| CC lead archive      | `delinkLeadsByOfficeCode` (internal, new)                          | creditcard-management                      |
| Report attribution   | `creditCardTransactionReport` reads `transaction_hierarchy_log`    | creditcard-management                      |
| Active-lead guard    | `getCustomerLeadByDseCode`                                         | creditcard-management                      |


**Frontend:** Backoffice office maintenance; agent app for affected DSE login/onboarding.

**Modules:** `novopay-platform-actor`, `novopay-platform-creditcard-management`

**Trigger:** `[UpdateOfficeProcessor](novopay-platform-actor/src/main/java/in/novopay/actor/office/processor/UpdateOfficeProcessor.java)` / `[dsa_createOrUpdateCorpOffice.xml](novopay-platform-actor/deploy/application/orchestration/dsa_createOrUpdateCorpOffice.xml)` when `closed_on` set (null → date).

**Actor:**

- Resolve DSE/DSA_ADMIN via `hierarchy_element__entity__mapping` (`OFFICE-CHANNEL`).
- Soft-delete hierarchy elements + mappings; deactivate users (scoped office closure, mirror Ticket 3).
- Do not alter historical partner mapping used only for past txn attribution.

**CC:**

- API `delinkLeadsByOfficeCode` (or agent code list from Actor).
- `delink_reason=OFFICE_CLOSED`; preserve `transaction_hierarchy_log` (reports read `thl`  - office/DSE/DSA Admin columns remain for old txns).
- Operational report excludes delinked rows per Ticket 2.

**Tests:** `closed_on` set → hierarchy soft-deleted → leads delinked → MIS still shows `thl.office_code` for historical rows.

---

### QA reference

**Status:** Deprecated section - do not execute as standalone QA scope.

**Pre-requisites:** DSA with at least one office, DSE and DSA Admin mapped to that office, open CC leads tied to office hierarchy. Admin Portal access to update office. Ticket 1 delink model in place.

**Test data setup:**


| #   | Entity                    | State before test                                 |
| --- | ------------------------- | ------------------------------------------------- |
| O   | Office OFF-1              | ACTIVE, `closed_on` null                          |
| P   | DSE mapped to OFF-1       | ACTIVE, open CC leads                             |
| Q   | DSA Admin mapped to OFF-1 | ACTIVE                                            |
| R   | CC lead                   | In progress, linked to DSE P, office in hierarchy |


**Functional tests:**

1. **Office closure trigger**
  - Set `closed_on` on OFF-1 via Admin Portal (`createOrUpdateCorpOffice`).
  - Verify office record updated with closure date.
2. **Linkage removed**
  - DSE P and DSA Admin Q hierarchy/office mapping removed (soft-deleted or unlinked per implementation).
  - Affected users cannot log in until re-onboarded.
3. **Open leads released**
  - Lead R: `assistor_code` cleared; `lead_link_status = DELINKED`; `delink_reason = OFFICE_CLOSED`.
  - Lead R no longer on DSE resume/pending list in Agent App.
4. **Attribution preserved in reports**
  - Run historical report / MIS query for lead R (by CRN or date range).
  - DSE, DSA Admin, office, partner columns still show original values from `transaction_hierarchy_log`.
  - Note: operational DSA Admin report (Ticket 2) should **not** list delinked lead R; historical/audit query may still show it.
5. **Re-onboarding - same DSA**
  - Re-onboard DSE P under same DSA at a different (open) office.
  - Onboarding succeeds; new CC application can be created.
6. **Re-onboarding - different DSA**
  - Re-onboard DSE P under a different DSA.
  - Onboarding succeeds.
7. **DSA Admin re-onboarding**
  - Re-onboard DSA Admin Q under same or different DSA.
  - Login and access restored.
8. **No false active-lead block**
  - Deactivate DSE P after office closure: no 4000360 from leads archived at closure.

**Edge cases:**

- Close office with no open leads: users still unlinked/disabled; no errors.
- Close office already closed (`closed_on` set again): idempotent, no duplicate side effects.
- Other offices under same DSA remain active and unaffected.

**Regression:**

- Open offices continue normal CC flow.
- Whole-DSA deactivation (Ticket 3) still works independently.

**Out of scope:** 60-day purge (Ticket 1), operational report filter rules (Ticket 2), whole-DSA deactivate (Ticket 3).

**Depends on:** Tickets 1 and 3 (delink model and hierarchy soft-delete patterns).

---

## Appendix - Engineering reference (not for product ticket body)

### Linkage vs attribution


| Removable (linkage)                 | Must preserve (attribution / UTM)                                                |
| ----------------------------------- | -------------------------------------------------------------------------------- |
| `transaction_audit.assistor`_*      | `transaction_hierarchy_log` snapshot                                             |
| Actor `hierarchy_element` live tree | `transaction_audit_attributes` (`partner_id`, `lead_source_key`, `link_journey`) |
| User login status                   | `hierarchy_log_id` on existing applications                                      |


### Cross-ticket decisions


| Topic                       | Decision                                                                 |
| --------------------------- | ------------------------------------------------------------------------ |
| Active implementation scope | Ticket 1 and Ticket 3 only                                               |
| Ticket mapping              | Ticket 2 merged into Ticket 1; Ticket 4 closed as not feasible          |
| Delink policy               | Clear assistor + status flag; never hard-delete `transaction_audit`      |
| UTM policy                  | Never update `hierarchy_log_id` or attribution attributes on delink      |
| Freshness policy            | 60-day rule applies to dashboard, admin portal, and deletion validation  |
| Deletion block condition    | Block only when lead is active and <=60 days                             |
| DSA lifecycle policy        | Separate DELETE and DISABLE flows; DISABLE re-onboard deletes old mapping first |
| Execution timing            | Ticket 1 scheduled batch; Ticket 3 synchronous lifecycle transitions     |
| Frontend impact             | Agent/App/Admin access behavior changes; validate on `dsa-prod`          |


### Verification (all tickets)

- Diff vs `ddp-prod` before merge
- DSA batch jobs in `novopay-platform-batch/migrations/dsa`
- Targeted tests per cc-backend-test-generation skill
- QA: 60-day purge + portal/dashboard freshness, merged report behavior, DSA DELETE flow, DSA DISABLE flow, re-onboarding transition

