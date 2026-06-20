---
name: Credit Card Bulk Build Plan
overview: "Build plan for the Credit Card Bulk feature on branch ddp-fea-credit-card-bulk: verify compilation, document current state and remaining work, and explicitly do not push."
todos: []
isProject: false
---

# Credit Card Bulk – Build Plan (No Push)

## Current state

- **Branch:** `ddp-fea-credit-card-bulk` (from `ddp-prod`) in [novopay-platform-creditcard-management](novopay-platform-creditcard-management).
- **Build:** `./gradlew compileJava` passes after fixing `CcBulkFileDAO.findById` (return `Optional.orElse(null)`).
- **Controller:** All five endpoints call processor `.execute(ctx)` (not `.process(ctx)`).

## What’s implemented


| Area            | Details                                                                                                                                 |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| DB              | Flyway `V000077__create_cc_bulk_file_and_lead.sql` – `cc_bulk_file`, `cc_bulk_lead`                                                     |
| Enum            | `TransactionAuditStages`: CC_BULK_FILE_UPLOADED, CC_BULK_LEAD_CREATE, CC_BULK_LINK_SENT, CC_BULK_LEAD_STATUS_UPDATED, CC_BULK_LINK_FAIL |
| Entities / DAOs | `CcBulkFileEntity`, `CcBulkLeadEntity`; `CcBulkFileDAO`, `CcBulkLeadDAO`, `CcBulkLeadSearchRowMapper`                                   |
| Service         | `ProcessCreditCardBulkFileService` – DMS by document_code, CSV parse, process-all (no fail-fast)                                        |
| Processors      | Upload, GetList, BulkSendLink, UpdateStatus, BulkResend – each with public `execute(ExecutionContext)`                                  |
| Orchestration   | XMLs and request/response templates for all five flows                                                                                  |
| REST            | `CreditCardBulkController` at `/api/v2/creditCardBulk`: POST upload, GET leads, POST sendLink, PATCH leads/{id}/status, POST resendLink |


## Build steps (local only – no push)

1. **Compile:**
  `cd novopay-platform-creditcard-management && ./gradlew compileJava`  
   (Already verified – success.)
2. **Full build (optional):**
  `./gradlew build`  
   (Runs tests; fix any test failures if you run it.)
3. **Do not push**
  Do not run `git push` for `ddp-fea-credit-card-bulk`. Push when you are ready after review.

## Remaining work (optional)

- **Unit tests (plan section 7.2):** ProcessCreditCardBulkFileService, Upload/GetList/BulkSend/UpdateStatus/BulkResend processors, CcBulkLeadSearchRowMapper/DAO, CreditCardBulkController (MockMvc). Assert process-all and capture stages where relevant.
- **Batch status API:** PUT `/leads/status` with list of updates – only if product requires it.
- **PAN for bulk:** Confirm how PAN is provided per lead (e.g. CSV column or context); no code change beyond current context-based `pan_number` unless required.

## Summary

- Code compiles; controller uses `.execute(ctx)`; DAO fix applied.
- Build plan: compile (done), optionally full build; **do not push** until you choose to.

