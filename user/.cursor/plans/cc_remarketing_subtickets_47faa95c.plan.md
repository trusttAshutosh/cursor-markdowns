---
name: CC Remarketing Subtickets
overview: Data-purging-style plan for daily unassisted CC remarketing SMS, with per-subticket Product ticket, Engineering reference, QA reference, journey tables, estimation/justification tables, and <=4h task slices.
todos:
  - id: finalize-ticket1
    content: Finalize Ticket 1 text with product wording and sign-off fields
    status: pending
  - id: finalize-ticket2
    content: Finalize Ticket 2 retail batch ticket body and comments
    status: pending
  - id: finalize-ticket3
    content: Finalize Ticket 3 bulk kafka ticket body and comments
    status: pending
  - id: finalize-ticket4
    content: Finalize Ticket 4 configs/flyways ticket body and comments
    status: pending
  - id: finalize-ticket5
    content: Finalize Ticket 5 QA/docs handoff ticket body and comments
    status: pending
  - id: align-journey-select
    content: Confirm Jira journey-field options per ticket with PM/Engg
    status: pending
  - id: lock-parallel-dependency
    content: Add parallel resumable-link stream owner and timeline into ticket dependency notes
    status: pending
isProject: false
---

# CC Remarketing SMS - Finalized After Product + Engg Discussion

Use the **Product ticket** blocks below for Jira/Linear ticket body. Copy matching **Engineering reference** and **QA reference** as ticket comments, exactly like data-purging format.

**Branch check before build:** Compare with latest prod branch baselines before implementation:

- Backend: `ddp-prod` in [novopay-platform-creditcard-management](novopay-platform-creditcard-management), [novopay-platform-batch](novopay-platform-batch), [novopay-platform-masterdata-management](novopay-platform-masterdata-management), [novopay-platform-notifications](novopay-platform-notifications), [novopay-platform-consents](novopay-platform-consents)
- Frontend (for regression checks only): `dsa-prod` in [novopay-platform-agent-webapp](novopay-platform-agent-webapp)

---

## Product UD vs Locked Decisions

### Product UD baseline
- Batch picks resumable `PENDING` applications.
- Exclude terminal statuses (`SUCCESS`, `FAILED`, `REJECTED`).
- Send resume link using existing communication template.
- Configurable frequency/batch/retry; maintain logs and audit.

### Locked decisions (from discussion)
- `transaction_sub_type='CC'`, `is_assisted='N'` only.
- Applicable for bulk too.
- Eligibility gate: `txn_status='PENDING'` + initial consent agreed (`AGREED` / `INPROGRESS`).
- Same link every time (reuse existing initial consent link).
- Same template as existing consent link SMS.
- Daily scheduler at **9:00 AM**.
- Default frequency: daily same time (24h), configurable.
- Same-day suppression: if app started today and initial link already sent today, do not send again.
- 10-day app validity, day-10 expiry batch unchanged.
- No existing MIS/report changes in phase-1; separate tracking via dedicated audit table.
- Parallel dependency: resumable-link validity stream (day-9 24h behavior).

---

## Ticket 1

### Product ticket

**Title:** CC-RMK-001: Define and implement eligibility + suppression contract for daily remarketing SMS

**Description:**

Before building sender flows, we need one finalized eligibility contract for remarketing candidates:

- CC only, unassisted only (`is_assisted='N'`)
- `txn_status='PENDING'`
- Initial consent already agreed (`AGREED` / `INPROGRESS`)
- Application still within resumable window (<10 days)
- Same-day duplicate prevention: if app started today and initial link already sent today, do not send again today

This ticket defines and implements candidate selection and suppression policy used by both retail batch and bulk Kafka flows.

**Acceptance criteria:**

- Eligibility query returns only unassisted CC pending + consent-agreed rows.
- Assisted/terminal/ineligible rows are excluded.
- Same-day suppression rule is enforced.
- Query contract is reusable for both retail and bulk callers.

**Depends on:** None (first implementation ticket)

**Jira journey field - select these (multiple):**

- **Credit Card** (primary candidate selection)
- **Agent App** (pending/resume impact validation only)
- **Admin Portal** (operational visibility checks)
- **Platform** (policy enforced in backend)

**Do not select:** Add-on Card, Loan On Card, Corporate lifecycle, Office closure, savings/loan/deposit journeys.

**Journeys impacted:**

| Journey | Who | What changes |
| --- | --- | --- |
| Unassisted CC pending candidate selection | System | Only valid pending consent-agreed unassisted leads become remarketing candidates |
| Same-day duplicate guard | Customer | Customer does not receive duplicate link on day-0 |
| Assisted exclusion | DSE / agent app | Assisted leads never enter remarketing candidate pool |
| Pending-to-expired window handling | Ops / system | Only day 1-9 leads eligible for reminders |

**Estimation**

| Subtask | Est (hrs) | Why this size / justification |
| --- | ---:| --- |
| Finalize eligibility predicate + edge rules | 2.0 | Decision-heavy contract that blocks all downstream tickets |
| Implement repository/DAO query and mapper | 3.5 | Focused DB/query work with controlled conditions |
| Add same-day suppression predicate and reason enum | 2.5 | Isolated business rule with clear output state |
| Unit tests for include/exclude matrix | 4.0 | High-risk regression area; needs explicit matrix coverage |

---

### Engineering reference

**Journey / flow map:**

| Flow | API / entry | Module |
| --- | --- | --- |
| Candidate selection (retail) | `ccRemarketingResumeSmsBatch` -> eligibility service | creditcard-management |
| Candidate selection (bulk) | `ccRemarketingPublishKafkaBatch` -> eligibility service | creditcard-management |
| Consent status source | join/lookup around consent audit in CC flows | creditcard-management + consents |
| Existing status expiry behavior | `updateCreditCardStatusBatch` | creditcard-management + batch |

Frontend (`dsa-prod`) regression touchpoint: `novopay-platform-agent-webapp` `/CC` dashboards (read-only impact validation).

**Modules:** `novopay-platform-creditcard-management`

**Baseline patterns to reuse:**

- [GetTnxResumeListProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/transaction/processor/GetTnxResumeListProcessor.java)
- [TransactionResumeListRowMapper.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/dao/TransactionResumeListRowMapper.java)
- [UpdateCreditCardStatusBatchProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/UpdateCreditCardStatusBatchProcessor.java)

**Implementation:**

1. Build `RemarketingEligibilityService` with query contract.
2. Add same-day suppression input predicate and skip reason.
3. Exclude terminal states and non-mobile rows.
4. Expose candidate query for retail and bulk callers.

---

### QA reference

**Pre-requisites:** DSA tenant with at least one unassisted CC lead, consent records in mixed states. Ability to trigger eligibility path manually in QA. DB read access to `transaction_audit`, consent audit source, and remarketing audit table.

**Test data setup (minimum):**

| # | Lead | Age | Consent / status | Expected from eligibility |
| --- | --- | --- | --- | --- |
| A | Unassisted CC pending | day-2 | AGREED | Included |
| B | Unassisted CC pending | day-0 | AGREED and initial link sent today | Excluded (`SAME_DAY_INITIAL_LINK`) |
| C | Assisted CC pending | day-2 | AGREED | Excluded |
| D | Unassisted CC success | day-2 | AGREED | Excluded |
| E | Unassisted CC pending | day-11 | AGREED | Excluded |

**Functional tests:**

1. Happy path candidate included (A).
2. Same-day suppression excludes B.
3. Assisted exclusion (C).
4. Terminal exclusion (D).
5. Day-window exclusion (E).

**DB checks (sample):**

```sql
SELECT client_reference_code, txn_status, is_assisted
FROM transaction_audit
WHERE client_reference_code IN ('<CRN-A>','<CRN-B>','<CRN-C>');
```

Regression: Existing CC creation, bulk upload, and consent/resume flows unaffected.

Out of scope for this ticket: SMS sender paths, scheduler registration, Kafka consumer.

---

## Ticket 2

### Product ticket

**Title:** CC-RMK-002: Implement daily 9:00 AM retail remarketing SMS batch

**Description:**

Implement scheduled retail remarketing flow that runs daily at 9:00 AM and sends SMS reminders for eligible unassisted pending CC cases using same-link reuse, dedupe, and per-record failure tolerance.

**Acceptance criteria:**

- Batch runs at 9:00 AM.
- Only eligible retail (non-bulk) candidates are processed.
- SMS uses existing template + same link.
- Per-record failures do not stop full batch.
- Batch summary logs and audit entries are persisted.

**Depends on:** Ticket 1

**Jira journey field - select these (multiple):**

- **Credit Card**
- **Platform**
- **Agent App** (behavioral impact only)

**Journeys impacted:**

| Journey | Who | What changes |
| --- | --- | --- |
| Daily retail reminder run | System | Eligible retail pending cases receive reminder SMS |
| Retry-safe processing | Ops | Batch continues despite individual send failures |
| Dedupe in retail flow | Customer | Avoid duplicate same-day/interval sends |

**Estimation**

| Subtask | Est (hrs) | Why this size / justification |
| --- | ---:| --- |
| Processor skeleton + orchestration wiring | 3.0 | Boilerplate + integration setup |
| End-to-end retail send pipeline integration | 4.0 | Highest complexity path in this ticket |
| Pagination/counters/logging | 2.5 | Operational reliability requirement |
| Unit tests for branches/errors | 4.0 | Required for safe batch behavior |

---

### Engineering reference

**Journey / flow map:**

| Flow | API / entry | Module |
| --- | --- | --- |
| Retail scheduled trigger | `ccRemarketingResumeSmsBatch` | creditcard-management + batch |
| Candidate fetch | `RemarketingEligibilityService` | creditcard-management |
| SMS send | existing notifications send path | creditcard-management + notifications |
| Audit write | `cc_remarketing_communication_audit` | creditcard-management |

**Modules:** `novopay-platform-creditcard-management`, `novopay-platform-batch`

**Baseline patterns to reuse:**

- [UpdateCreditCardStatusBatchProcessor.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/common/processors/UpdateCreditCardStatusBatchProcessor.java)
- Existing sendSMS integration path in platform libs/notifications

**Implementation:**

1. Create `RemarketingResumeSmsBatchProcessor` (`AbstractProcessor`).
2. Wire orchestration XML and API template for scheduled batch invocation.
3. Apply eligibility + dedupe + same-link resolver + sendSMS.
4. Persist SUCCESS/FAILED/SKIPPED audit with reasons and counters.

---

### QA reference

**Pre-requisites:** Ticket 1 deployed; scheduler enabled in QA; test customers with pending unassisted leads and valid mobile numbers.

**Test data setup (minimum):**

| # | Lead | Type | State | Expected after run |
| --- | --- | --- | --- | --- |
| A | Retail pending eligible | non-bulk | day-2, consent agreed | SMS sent |
| B | Retail same-day suppression | non-bulk | day-0 link sent | Skipped |
| C | Retail ineligible terminal | non-bulk | success/fail | Skipped |

**Functional tests:**

1. 9 AM run sends A.
2. B is skipped with same-day reason.
3. C is skipped as ineligible.
4. Inject one send failure -> batch continues and logs failed row.
5. Re-run within interval -> no duplicate send.

**DB checks (sample):**

```sql
SELECT client_reference_code, communication_status, skip_reason
FROM cc_remarketing_communication_audit
WHERE client_reference_code IN ('<CRN-A>','<CRN-B>','<CRN-C>')
ORDER BY created_on DESC;
```

Regression: Existing status expiry batch and standard consent flow unaffected.

Out of scope for this ticket: Bulk Kafka path.

---

## Ticket 3

### Product ticket

**Title:** CC-RMK-003: Implement bulk remarketing via Kafka publish + consumer send

**Description:**

Implement bulk remarketing pipeline where eligible bulk leads are published by scheduled job and SMS is sent by consumer with consumer-side throttling.

**Acceptance criteria:**

- Bulk leads are published to remarketing Kafka topic.
- Consumer sends SMS using same-link + same-template policy.
- Retail leads are never published to bulk remarketing topic.
- Consumer throttling config is respected.

**Depends on:** Ticket 1

**Jira journey field - select these (multiple):**

- **Credit Card**
- **Platform**

**Journeys impacted:**

| Journey | Who | What changes |
| --- | --- | --- |
| Bulk remarketing publish | System | Eligible bulk leads queued for messaging |
| Bulk consumer send | Customer | Bulk pending customers receive reminder SMS |
| Kafka throttle control | Ops | Bulk send rate managed at consumer side |

**Estimation**

| Subtask | Est (hrs) | Why this size / justification |
| --- | ---:| --- |
| Publish processor + payload contract | 3.0 | Clear, bounded producer work |
| Consumer send + audit integration | 4.0 | Integration-heavy and failure-prone |
| Throttle/config handling | 3.0 | Operational requirement |
| Producer/consumer unit tests | 4.0 | Needed for correctness + safety |

---

### Engineering reference

**Journey / flow map:**

| Flow | API / entry | Module |
| --- | --- | --- |
| Bulk publish scheduler | `ccRemarketingPublishKafkaBatch` | creditcard-management + batch |
| Topic publish | Kafka producer | creditcard-management |
| Consumer send | `RemarketingSmsKafkaConsumer` | creditcard-management |
| Notification send | existing notifications API | creditcard-management + notifications |

**Modules:** `novopay-platform-creditcard-management`, `novopay-platform-batch`, `novopay-platform-masterdata-management`

**Baseline patterns to reuse:**

- [BatchValidateLeadsService.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/bulk/BatchValidateLeadsService.java)
- [BulkUploadLeadsConsumer.java](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/consumers/BulkUploadLeadsConsumer.java)

**Implementation:**

1. Build `RemarketingPublishKafkaBatchProcessor` for bulk candidates.
2. Define payload contract (`client_reference_code`, tenant/source metadata).
3. Build `RemarketingSmsKafkaConsumer` for send + audit update.
4. Enforce non-retail publish and consumer throttle configs.

---

### QA reference

**Pre-requisites:** Kafka topic configured in QA, consumer enabled, bulk pending data available.

**Test data setup (minimum):**

| # | Lead | Bulk flag | State | Expected |
| --- | --- | --- | --- | --- |
| A | Bulk eligible | Y | pending + consent agreed | Published and sent |
| B | Retail eligible | N | pending + consent agreed | Not published to bulk topic |
| C | Bulk ineligible | Y | terminal/same-day excluded | Not published |

**Functional tests:**

1. A published then consumed then sent.
2. B not present in topic.
3. C skipped and no send.
4. Throttle values affect send pacing.
5. Consumer failure path writes FAILED audit and retry path behaves as configured.

**DB checks (sample):**

```sql
SELECT client_reference_code, communication_source, communication_status
FROM cc_remarketing_communication_audit
WHERE client_reference_code IN ('<CRN-A>','<CRN-B>','<CRN-C>')
ORDER BY created_on DESC;
```

Regression: Existing bulk upload and consent initiation path unaffected.

Out of scope for this ticket: Retail scheduler path.

---

## Ticket 4

### Product ticket

**Title:** CC-RMK-004: Add configs, scheduler, and flyways for remarketing rollout

**Description:**

Add all required configuration keys, scheduler rows, and DB structures to support remarketing rollout safely across environments.

**Acceptance criteria:**

- Required configs exist with defaults.
- Retail and bulk scheduler entries exist (9 AM).
- Audit table flyway applied successfully.
- Feature can be toggled/controlled via config.

**Depends on:** None (can run in parallel with Tickets 2/3 after schema contract alignment)

**Jira journey field - select these (multiple):**

- **Platform**
- **Credit Card**

**Journeys impacted:**

| Journey | Who | What changes |
| --- | --- | --- |
| Feature rollout control | Ops | Enable/disable and tune remarketing safely |
| Daily scheduling | System | Retail + bulk runs triggered at configured time |
| Audit persistence | Ops/Product | Separate impact tracking available |

**Estimation**

| Subtask | Est (hrs) | Why this size / justification |
| --- | ---:| --- |
| Config key flyways + defaults | 3.0 | Mostly declarative with validation |
| Scheduler flyways for two jobs | 2.0 | Straightforward batch row setup |
| Audit schema flyway + index pass | 3.0 | Requires careful schema design and compatibility checks |

---

### Engineering reference

**Journey / flow map:**

| Flow | API / entry | Module |
| --- | --- | --- |
| Config load | `@NovopayConfig` resolution | creditcard-management + masterdata |
| Scheduler registration | `batch_master` rows | batch |
| Audit persistence | DB flyway + repository | creditcard-management |

**Modules:** `novopay-platform-masterdata-management`, `novopay-platform-batch`, `novopay-platform-creditcard-management`

**Implementation:**

1. Add config flyways:
   - enable flag
   - interval hours
   - batch size
   - kafka topic + throttle
2. Add scheduler flyways:
   - retail batch 9 AM
   - bulk publish batch 9 AM
3. Add audit table flyway with indexes for query/trace.

---

### QA reference

**Pre-requisites:** Migration execution access and env-level config visibility in QA.

**Functional tests:**

1. Verify config values resolved by service.
2. Verify both scheduler jobs present and active.
3. Verify feature disable stops processing.
4. Verify audit table write/read paths operational.

**DB checks (sample):**

```sql
SELECT batch_name, cron_expression FROM batch_master WHERE batch_name LIKE '%Remarketing%';
SELECT prop_key, prop_value FROM configuration WHERE prop_key LIKE 'cc.remarketing%';
```

Out of scope for this ticket: Candidate logic and send logic validation.

---

## Ticket 5

### Product ticket

**Title:** CC-RMK-005: Execute QA pack, documentation, and release handoff

**Description:**

Finalize QA validation matrix, documentation, and operational handoff artifacts for safe release.

**Acceptance criteria:**

- QA matrix covers retail + bulk + suppression + dedupe + failures.
- Docs include config/runbook/rollback and sample impact queries.
- Evidence pack generated for release sign-off.

**Depends on:** Tickets 1-4

**Jira journey field - select these (multiple):**

- **Credit Card**
- **Platform**
- **Admin Portal** (operational checks where relevant)

**Journeys impacted:**

| Journey | Who | What changes |
| --- | --- | --- |
| End-to-end retail reminder | QA/Ops | Verified for release confidence |
| End-to-end bulk reminder | QA/Ops | Verified for release confidence |
| Operational monitoring | Ops/Product | Runbook and tracking queries available |

**Estimation**

| Subtask | Est (hrs) | Why this size / justification |
| --- | ---:| --- |
| QA matrix and test data guide finalization | 3.0 | Critical for deterministic validation |
| Documentation + operational query pack | 3.0 | Required handoff artifact |
| Targeted run + evidence capture | 4.0 | Time-bound but mandatory sign-off activity |

---

### Engineering reference

**Modules for documentation/test evidence:** CC management, batch, masterdata, notifications, consents dependency notes.

**Implementation artifacts:**

1. README + runbook updates.
2. Test evidence bundle for critical flows.
3. Rollback checklist.

---

### QA reference

**Pre-requisites:** Tickets 1-4 deployed to QA; parallel resumable-link stream state known.

**Functional tests:**

1. Retail happy path + same-day suppression.
2. Bulk publish + consume + throttle.
3. Assisted exclusion.
4. Terminal exclusion.
5. Failure and retry visibility.
6. No regression in dashboard manual resend.

Out of scope for this ticket: New product behavior changes.

---

## Estimation Summary

| Ticket | Total Est (hrs) | Notes |
| --- | ---:| --- |
| Ticket 1 | 12.0 | Core policy foundation |
| Ticket 2 | 13.5 | Retail send path |
| Ticket 3 | 14.0 | Bulk Kafka path |
| Ticket 4 | 8.0 | Flyways + scheduler + config |
| Ticket 5 | 10.0 | QA + docs + release pack |
| **Total** | **57.5** | Excludes parallel resumable-link stream effort |

---

## Justification Table

| Split decision | Justification |
| --- | --- |
| Separate policy foundation first | Prevents rework across both sender flows |
| Retail and bulk as separate tickets | Different runtime and failure models (scheduler vs consumer) |
| Config/flyway separate | Safe rollout control and quicker operational recovery |
| QA/docs dedicated ticket | Release quality and auditability |
| <=4h subtasks | Review-friendly slices, parallel-friendly delivery |

---

## Parallel dependency (external to this ticket set)

- Resumable-link validity stream (day-9 last reminder 24h validity behavior)
- This dependency blocks final UAT sign-off for the day-9 link window scenario