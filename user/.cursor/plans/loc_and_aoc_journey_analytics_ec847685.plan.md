---
name: LOC and AOC Journey Analytics
overview: Implement "what failed" logging and journey stage capture for Loan on Card (LOC) flow and Add-on Card (AOC) journey, following the existing CaptureStages pattern, with optional centralised/structured logging and failure-reason persistence.
todos: []
isProject: false
---

# LOC and AOC Journey Analytics Implementation

## Context

- **Reference:** [CaptureStages](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/components/stages/CaptureStages.java) persists stage + status + stan via [TransactionAuditLogCapture](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/components/stages/TransactionAuditLogCapture.java) into `transaction_audit_logs` (state, status, attempt, stan). No failure-reason column exists; [TransactionAuditAttributes](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/entity/TransactionAuditAttributes.java) (attr_key/attr_value) can store extra context.
- **LOC flow** (from PDF + [common_loanOnCards.xml](novopay-platform-creditcard-management/deploy/application/orchestration/common_loanOnCards.xml)): inquireCardEligibility → (customerOTPLoc OTP gen/validate) → getLOCOffers (cardSummary + loanOffers) → submitLoanOnCards. Product codes: 007 (Insta), 010 (Jumbo). Inquire returns AAN and SVC_RETURN; eligibility returns product list.
- **AOC flow:** create app ([AddOnCardService](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AddOnCardService.java)) → OTP (consent flow; LOC uses [customerOTPLoc](novopay-platform-creditcard-management/deploy/application/orchestration/common_fetchCustomerDetailsWithDedupe.xml) with [CustomerOtpGenerationProcessor](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/transaction/processor/CustomerOtpGenerationProcessor.java)) → card summary ([AOCCardSummaryService](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AOCCardSummaryService.java): inquire → card summary → account info → view recipient) → add recipient ([AddRecipientController](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/controller/AddRecipientController.java)) → submit (docs reference `POST /api/v2/addOnCard/submit`; implement capture when that endpoint exists, e.g. dsa-add-on branch).

## 1. LOC flow – stage capture and “what failed” logging

### 1.1 Stage names and persistence

- Add LOC stages (use string state names; no enum change required if you keep flexibility) and persist via existing `TransactionAuditLogCapture.saveAuditTransactionLog(transactionAudit, state, status, stan)`.
- Suggested state names: `INQUIRE_CARD_ELIGIBILITY`, `LOC_OTP_GENERATE`, `LOC_OTP_VALIDATE`, `PRODUCT_ELIGIBILITY`, `LOC_CARD_SUMMARY`, `LOC_ACCOUNT_INFO`, `SUBMIT_LOAN_INSTA`, `SUBMIT_LOAN_JUMBO`.

### 1.2 Inquire card details (AAN / journey stop)

- **Where:** [InquireCardEligibilityProcessor](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/loc/processors/InquireCardEligibilityProcessor.java) (LOC) and [AOCCardSummaryService.inquireCardDetails](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AOCCardSummaryService.java) (AOC card summary).
- **Capture:** On success (SVC_RETURN P + AAN present): save stage `INQUIRE_CARD_ELIGIBILITY` (or AOC equivalent) SUCCESS.
- **Failure:** When AAN missing or SVC_RETURN not P: persist FAIL for same stage; store in `transaction_audit_attributes` e.g. `loc_failure_stage=INQUIRE_CARD_ELIGIBILITY`, `loc_failure_reason=AAN_MISSING` or `SVC_RETURN_F` and optionally `svc_return=<value>`. Log clearly: “AAN missing in inquire details API – stopping journey” (and product code 010, 008, 007, svc_return in inquire context if available from response).

### 1.3 Product eligibility – no offers

- **Where:** [LoanOffersProcessor](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/loc/processors/LoanOffersProcessor.java) (getProductEligibility → product list).
- **Capture:** On empty `productList`: persist stage `PRODUCT_ELIGIBILITY` FAIL; store product codes returned (010, 008, 007) and svc_return in attributes (e.g. `eligibility_product_codes`, `inquire_svc_return`) and ensure these are available in “inquire details” context for logging (log: “Eligibility API – no offers; product codes 010, 008, 007, svc_return in inquire details API”).
- On success: persist SUCCESS and store which products were offered (e.g. `offered_product_codes`).

### 1.4 Insta vs Jumbo offered and chosen

- **Where:** LoanOffersProcessor (offered list); [SubmitLoanOnCardsProcessor](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/loc/processors/SubmitLoanOnCardsProcessor.java) (chosen product_code 007 vs 010).
- **Capture:** After eligibility success, persist in attributes e.g. `offered_insta_jumbo` (007/010 or both). On submit, persist `chosen_product_code` (007 or 010) and capture stage `SUBMIT_LOAN_INSTA` or `SUBMIT_LOAN_JUMBO` with SUCCESS/FAIL.

### 1.5 API failure – what and why

- **Where:** InquireCardEligibilityProcessor, LoanOffersProcessor, CardSummaryProcessor, SubmitLoanOnCardsProcessor, and bank/adapter layer where exceptions are caught.
- **Capture:** On any API failure: persist FAIL for the corresponding stage; store in attributes e.g. `loc_failure_stage`, `loc_failure_reason`, `loc_api_error_code`, `loc_api_error_message` (or a single structured key). Log with: api name, error code, message, stan.

### 1.6 LOC-specific wiring

- LOC processors currently do not use [CaptureStages](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/components/stages/CaptureStages.java) or [TransactionAuditLogCapture](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/components/stages/TransactionAuditLogCapture.java). Inject `TransactionAuditLogCapture` (or a thin LOC-specific facade that uses it + attribute writes) into InquireCardEligibilityProcessor, LoanOffersProcessor, CardSummaryProcessor, SubmitLoanOnCardsProcessor. Use [LOCUtils.createOrUpdateAttribute](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/loc/util/LOCUtils.java) for failure reason and product-code attributes. Ensure `TransactionAudit` and `stan` are available in ExecutionContext (LOC flow already has transaction audit and stan in context).

## 2. Add-on card (AOC) journey analytics

### 2.1 Stage list (match your 1–6)

- 1. Create app
- 1. OTP generation
- 1. OTP validation
- 1. Card summary (4a card eligibility, 4b card summary, 4c account info, 4d view recipient)
- 1. Add recipient
- 1. Submit

Use string state names e.g. `AOC_CREATE_APP`, `AOC_OTP_GENERATION`, `AOC_OTP_VALIDATION`, `AOC_CARD_ELIGIBILITY`, `AOC_CARD_SUMMARY`, `AOC_ACCOUNT_INFO`, `AOC_VIEW_RECIPIENT`, `AOC_ADD_RECIPIENT`, `AOC_SUBMIT`.

### 2.2 Where to capture

- **Create app:** [AddOnCardService.generateConsentLink](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AddOnCardService.java) after successful consent and insertTransactionAudit (or right after insert). Need access to TransactionAudit and stan (pass via headers or resolve from request/clientReferenceCode). Persist `AOC_CREATE_APP` SUCCESS/FAIL.
- **OTP generation / validation:** If AOC uses the same customerOTPLoc flow with a different transaction_sub_type (e.g. AOC), extend [TransactionAuditUtil.getServiceStage](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/utils/TransactionAuditUtil.java) to map that API + function_sub_code to `AOC_OTP_GENERATION` / `AOC_OTP_VALIDATION` so existing [CustomerOtpGenerationProcessor](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/transaction/processor/CustomerOtpGenerationProcessor.java) / CustomerOtpValidationProcessor audit log already captures the right state. If AOC uses a different API, add corresponding cases and capture there.
- **Card summary (4a–4d):** In [AOCCardSummaryService.getCardSummary](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AOCCardSummaryService.java): after inquireCardDetails → AOC_CARD_ELIGIBILITY; after getCardSummary → AOC_CARD_SUMMARY; after submitAccountInfo → AOC_ACCOUNT_INFO; after addRecipientData (view recipient) → AOC_VIEW_RECIPIENT. Inject TransactionAuditLogCapture (or CaptureStages) and persist SUCCESS/FAIL per sub-step; on AAN missing or inquire FAIL, persist FAIL and reason in attributes.
- **Add recipient:** In AddRecipientService.addRecipient (and update if needed): capture `AOC_ADD_RECIPIENT` SUCCESS/FAIL. Requires audit id/transaction audit and stan from request/context.
- **Submit:** When `POST /api/v2/addOnCard/submit` is implemented (e.g. in dsa-add-on), in the service that performs the submit: capture `AOC_SUBMIT` SUCCESS/FAIL and optional failure reason in attributes.

### 2.3 Improvements over current CaptureStages

- Use explicit stage names (no dependency on OfferTypes for AOC/LOC).  
- Persist failure reason and key context (product_code, svc_return, error_code) in `transaction_audit_attributes` instead of only state/status in `transaction_audit_logs`.  
- Optional: extend [CaptureStages](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/components/stages/CaptureStages.java) with an overload e.g. `capture(transactionAudit, stage, status, stan, failureReason, contextMap)` that writes one row to transaction_audit_logs and optional attributes for reason/context; LOC and AOC use this for consistency.

## 3. Centralised / structured logging

- Add a small **journey logger** utility (e.g. `JourneyAuditLogger` or use a dedicated logger name) that:
  - Accepts: journeyType (LOC | AOC), stage, status, stan, clientReferenceCode / transactionAuditId, and optional map (product_code, svc_return, failure_reason, error_code, etc.).
  - Logs one structured line (e.g. JSON or key=value) with consistent keys so log aggregation/analytics can parse. Use SLF4J + MDC: put stan, journey_type, stage, client_reference_code at entry; log at capture points; clear where appropriate (e.g. in filter or controller).
- Use this in LOC processors and AOC services at the same points where DB stage capture happens, so “what failed” and “which offer/chosen” are both in DB and in logs.

## 4. Data storage and schema

- **transaction_audit_logs:** Keep existing schema (state, status, attempt, stan). Use state = stage name (LOC and AOC as above).
- **transaction_audit_attributes:** Store failure and context with fixed keys to keep queries simple, e.g.  
`loc_failure_stage`, `loc_failure_reason`, `loc_product_codes`, `loc_chosen_product_code`, `eligibility_svc_return`, `aan_missing` (or one JSON attribute per stage if you prefer). Same idea for AOC: `aoc_failure_stage`, `aoc_failure_reason`.
- Avoid adding a new column to `transaction_audit_logs` if attributes are sufficient; otherwise add a single `failure_reason` or `metadata` (e.g. JSON) column and migration in product/dsa Flyway as per project rules.

## 5. Architecture and best practices

- **Single responsibility:** Keep stage capture and failure-reason persistence in one place (TransactionAuditLogCapture + attributes), and optional JourneyAuditLogger for logs only.  
- **Reuse:** Reuse [TransactionAuditLogCapture](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/components/stages/TransactionAuditLogCapture.java), [LOCUtils.createOrUpdateAttribute](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/loc/util/LOCUtils.java), and existing TransactionAudit resolution.  
- **Idempotency:** Use same “find or create” audit log by (transaction_audit_id, state) as today; increment attempt on each capture when appropriate.  
- **dsa-add-on branch:** Implement so that the same stage names and attribute keys work when run from dsa-add-on; if submit or OTP flow differs there, use the same capture points and stage enums/strings.

## 6. Implementation order (suggested)

1. Add LOC stage capture and failure-reason attributes in InquireCardEligibilityProcessor and LoanOffersProcessor (including “no offers” and product codes 010, 008, 007, svc_return).
2. Add capture in CardSummaryProcessor and SubmitLoanOnCardsProcessor (Insta/Jumbo chosen, API failure).
3. Add AOC stages: AddOnCardService (create), AOCCardSummaryService (4a–4d), AddRecipientService (add/update), and submit when present.
4. Wire OTP stages for AOC (TransactionAuditUtil or equivalent) if AOC shares customerOTPLoc.
5. Introduce JourneyAuditLogger and MDC and call it from the same capture points.
6. Optional: extend CaptureStages with overload for failure reason + context and refactor LOC/AOC to use it.

## Key files to touch


| Area        | Files                                                                                                                                     |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| LOC capture | InquireCardEligibilityProcessor, LoanOffersProcessor, CardSummaryProcessor, SubmitLoanOnCardsProcessor, LOCUtils (or new LOCStageCapture) |
| AOC capture | AddOnCardService, AOCCardSummaryService, AddRecipientService, (submit service when present)                                               |
| Stage util  | TransactionAuditUtil (AOC OTP mapping if needed)                                                                                          |
| Shared      | TransactionAuditLogCapture, CaptureStages (optional overload), TransactionAuditAttributes DAO                                             |
| Logging     | New JourneyAuditLogger + MDC in controllers/filters                                                                                       |


No mermaid diagram is required for this plan; the flow is already documented in the PDF and orchestration XML.