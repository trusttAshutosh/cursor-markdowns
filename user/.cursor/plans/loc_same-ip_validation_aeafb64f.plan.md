---
name: LOC same-IP validation
overview: Extend the same customer/agent IP chain handling and CC0005-style check to LOC by reusing one shared checker, mirroring manageCC processor order where applicable, without changing CC behavior. Treat LOC consent as product-driven (templates may live outside this repo); validate at agent→customer transition (hybrid handoff) when context has both sides, otherwise on the first customer LOC API that does.
todos:
  - id: extract-checker
    content: Add SameNetworkIpOverlapChecker; refactor ValidateCustomerIPAddressProcessor to delegate only (CC behavior unchanged)
    status: cancelled
  - id: loc-agent-ip-persist
    content: Persist agent_ip_addr from client_ip on LOC txn create/update (LOC-only, mirror CC intent)
    status: cancelled
  - id: get-txn-fallback
    content: "GetTransactionAuditProcessor: resolve audit by client_reference_code when client_reference_number blank"
    status: completed
  - id: orchestrate-loc-xml
    content: "Update common_loanOnCards.xml: getTxn + getAttr + validate before inquire/getLOCOffers/submit; optional fetchAgentDetails if needed"
    status: completed
  - id: hybrid-handoff-ip
    content: "manageLOCTransactionAudit HYBRID_JOURNEY: run shared validation when EC has customer IP + persisted agent_ip (or document deferral to first customer LOC API)"
    status: pending
  - id: tests
    content: Add/update unit and journey tests; run targeted Gradle
    status: completed
  - id: reconcile-bulk-branch
    content: "Before prod merge: rebase/merge ddp-fea-cc-bulk-upload; single shared IP module; resolve overlaps in ValidateCustomerIPAddressProcessor, bulk overlap validator, GetTransactionAuditProcessor"
    status: pending
isProject: false
---

# LOC same-network IP validation (parity with CC)

## Answers to your placement questions

### Is LOC “v1 API”?
LOC in this service is **not** the `manageCreditCardApplication` request. It is a **separate** orchestration file: [`deploy/application/orchestration/common_loanOnCards.xml`](deploy/application/orchestration/common_loanOnCards.xml) (`inquireCardEligibility`, `getLOCOffers`, `submitLoanOnCards`, etc.), plus [`deploy/application/orchestration/common_manageLOCTransactionAudit.xml`](deploy/application/orchestration/common_manageLOCTransactionAudit.xml). That is the usual “v1-style” pattern (validators + processor chain per request), **without** `run_mode` REAL/TRIAL like [`common_manageCreditCardApplication.xml`](deploy/application/orchestration/common_manageCreditCardApplication.xml).

### Follow manageCC XML for where to put IP validation?
**Follow the same ordering idea, not the REAL-only gate by default.**

In manageCC, the important sequence is ([`common_manageCreditCardApplication.xml`](deploy/application/orchestration/common_manageCreditCardApplication.xml)):

1. `getTransactionAuditProcessor`
2. `getTransactionAuditAttrProcessor` (with `overwrite_optional_params` where needed)
3. Optional `fetchAgentDetailsProcessor` (when `is_external_agent=N`)
4. **`validateCustomerIPAddressProcessor`** only under `run_mode=REAL`

For LOC, there is **no** `run_mode` today. Recommended approach:

- **Mirror steps 1–3 (as applicable)** so `system_ip_address`, `agent_ip_addr`, and gateway/header keys match what CC validation expects.
- Run **`validateCustomerIPAddressProcessor`** (same bean, after extraction to a shared checker — see below) **without** a REAL-only wrapper **unless** product explicitly introduces `run_mode` for LOC and wants TRIAL vs REAL parity with CC.

Earliest safe point per request: **after** txn + attrs are on `ExecutionContext`, **before** the first expensive bank call on that request (e.g. before `inquireCardDetails`, before `getCardSummary` / `getProductEligibility`, before `submitInstaLoan`).

### Consent / agent → customer (LOC)

**Consent templates for LOC** may exist in **consent / masterdata** (outside this repo). This service still only “sees” consent when a request carries the resulting customer context (e.g. `system_ip_address` / browser details / internal consent API mirroring CC).

**Agent → customer handoff in-repo:** [`ManageLOCTransactionAuditProcessor`](src/main/java/in/novopay/creditcard/common/processors/ManageLOCTransactionAuditProcessor.java) handles `function_sub_code=HYBRID_JOURNEY`: creates/updates txn, marks hybrid in `CCAdditionalTxnData`, caches `hybrid_journey_data` under `target_api_payload_<client_reference_code>`. That is the natural **transition point** from assisted agent setup to **customer** continuing the journey.

**Validation timing (your requirement: “as soon as we go from agent to customer”):**

1. **Preferred instant:** Run the **same shared** IP validation **immediately after** txn + attrs are consistent and the **current** `ExecutionContext` has a **trustable customer IP chain** (`system_ip_address` and/or `consent_system_ip_address` after any populate step) **and** **agent side** (`agent_ip_addr` and/or `client_ip` / gateway headers), matching CC rules. On the hybrid handoff **request**, implement only if the gateway/body actually includes the **customer** IP at that moment; if the handoff payload is agent-only, validation cannot be correct yet.

2. **Fallback (typical):** First **customer-originated** LOC call after handoff (`inquireCardEligibility` / `getLOCOffers`) already loads audit attrs and request IPs — place **`validateCustomerIPAddressProcessor`** there (per manageCC order) so validation runs on the **first** hop where both sides exist. That is effectively “as soon as the customer channel hits the backend” with full context, which aligns with consent-opened + customer device if the FE sends updated `browser_details` on that call (same CC doc pattern in [`docs/IP_VALIDATION_CONTEXT_SINGLE_VS_BULK.md`](docs/IP_VALIDATION_CONTEXT_SINGLE_VS_BULK.md)).

3. **If LOC orchestration later wires consent processors** (like CC): insert **`validateCustomerIPAddressProcessor`** **immediately after** the step that applies consent / trusted system IP to the context (between `getAttr` and bank calls), not only at submit.

**Implementation note:** avoid duplicating logic — invoke the same **shared checker** from orchestration; for `HYBRID_JOURNEY`, either call a small **delegating service** used by `ValidateCustomerIPAddressProcessor` or add a **thin** orchestration step that calls that service only when dual-sided IP is present (open-closed).

---

## Coordination with `ddp-fea-cc-bulk-upload` (avoid prod merge conflicts / duplicate code)

Bulk/CC IP hardening is expected on branch **`ddp-fea-cc-bulk-upload`** (shared strip + overlap checks, Kafka header `client_ip`, `BulkUploadLeadIpOverlapValidator` or equivalent, possible `SameNetworkIpOverlapChecker`, `IpExecutionContextTrace` touchpoints, `GetTransactionAuditAttrProcessor` / `CreditCardApplicationService` changes).

**Rules for LOC work:**

1. **Single source of truth:** LOC must call the **same** shared IP validation module that CC retail and bulk use on that branch — **no second copy** of strip / `novopay.ip.pattern` / CC0005 logic under `loc/`.
2. **Land order:** Prefer implementing LOC on top of **`ddp-fea-cc-bulk-upload`** (or merge that branch into the LOC feature branch **first**), then add LOC-only orchestration + `agent_ip_addr` persistence. If LOC lands first, schedule an explicit **reconcile pass** when bulk merges so you do not reintroduce inlined `findUniqueIP` or a duplicate checker class.
3. **High-churn files:** Watch for overlapping edits in:
   - [`ValidateCustomerIPAddressProcessor`](src/main/java/in/novopay/creditcard/common/processors/ValidateCustomerIPAddressProcessor.java)
   - [`GetTransactionAuditProcessor`](src/main/java/in/novopay/creditcard/common/processors/GetTransactionAuditProcessor.java) (LOC `client_reference_code` fallback must compose with any bulk-branch changes)
   - Any `common/ip/*` or bulk consumer / `BatchValidateLeadsService` paths — LOC should **import** shared helpers, not edit bulk pipelines unless required.
4. **Verification:** After combining branches locally, run **CC + bulk + LOC** targeted tests and fix conflicts once so prod is a single merged story.

---

## Design constraints (from earlier requirements)

- **Same IP math as CC:** comma-split, trim, `novopay.ip.pattern` stripping, join, then same-network rule and **CC0005** when `novopay.cc.enable.ip.validation=Y` (single shared implementation; [`ValidateCustomerIPAddressProcessor`](src/main/java/in/novopay/creditcard/common/processors/ValidateCustomerIPAddressProcessor.java) delegates — **no behavior change** for manageCC).
- **Avoid duplication / class explosion:** one small shared module (e.g. `SameNetworkIpOverlapChecker` + optional thin `CustomerAgentIpValidation` façade) used by CC processor and LOC orchestration; **do not** fork the algorithm in LOC-only classes.
- **Open-closed:** LOC gains validation via **orchestration + persistence hooks**, not by editing CC processors’ branching for LOC.
- **Bulk:** This repo’s bulk pipeline is CC-oriented; **retail LOC APIs** are in scope; a future LOC bulk entry should call the **same** checker (no second algorithm).

---

## Implementation outline

1. **Extract shared checker** from current `ValidateCustomerIPAddressProcessor` (`findUniqueIP` + fatal `CC0005` guard) into e.g. `SameNetworkIpOverlapChecker` with `resolveUniquePublicSide` + `throwIfSameNetwork` (+ optional `resolveCustomerAndAgentPublicSides` for DRY). Refactor processor to call it only — **golden tests** on strings that CC uses today.

2. **LOC audit parity for `agent_ip_addr`:** CC persists `agent_ip_addr` from `client_ip` on TRIAL ([`CreateOrUpdateCCApplicationProcessor`](src/main/java/in/novopay/creditcard/transaction/processor/CreateOrUpdateCCApplicationProcessor.java)). LOC never touches `agent_ip_addr` today. Add a **minimal** write in LOC txn lifecycle (e.g. end of [`CreateOrUpdateLOCTransactionAuditProcessor`](src/main/java/in/novopay/creditcard/loc/processors/CreateOrUpdateLOCTransactionAuditProcessor.java) or dedicated tiny processor) when `client_ip` is present — **LOC-only**, no CC change.

3. **`GetTransactionAuditProcessor` LOC compatibility:** LOC requests use `client_reference_code`; processor today keys off `client_reference_number`. Add a **backward-compatible** fallback: if number blank, resolve by `client_reference_code` (same as CC constant [`CLIENT_REFERENCE_CODE`](src/main/java/in/novopay/creditcard/constants/TransactionAuditConstants.java)).

4. **Orchestration** ([`common_loanOnCards.xml`](deploy/application/orchestration/common_loanOnCards.xml)) and **hybrid handoff** ([`common_manageLOCTransactionAudit.xml`](deploy/application/orchestration/common_manageLOCTransactionAudit.xml) / processor tail): for `inquireCardEligibility`, `getLOCOffers`, and `submitLoanOnCards`, before existing business processors, add (manageCC order):

   - `getTransactionAuditProcessor`
   - `getTransactionAuditAttrProcessor` (`overwrite_optional_params=Y` aligned with manageCC)
   - Optional: `fetchAgentDetailsProcessor` if LOC assisted flows need same agent context as CC (match manageCC guard on `is_external_agent` if that flag exists on LOC requests)
   - `validateCustomerIPAddressProcessor`

   **Earliest journey validation:** including **`inquireCardEligibility`** satisfies “don’t wait until end” better than only `submitLoanOnCards`.

   **Hybrid / agent→customer:** During implementation, confirm whether `HYBRID_JOURNEY` requests include **customer** `system_ip_address` (or consent-enriched equivalent). If **yes**, extend [`manageLOCTransactionAudit`](deploy/application/orchestration/common_manageLOCTransactionAudit.xml) (after `manageLOCTransactionAuditProcessor` or inside processor via shared validator) to run validation once attrs + IPs are on context. If **no**, rely on the first `common_loanOnCards` request from the customer channel (still “as soon as” the backend sees both sides).

5. **Tests:** extend LOC processor/journey tests and orchestration-related tests per [`.cursor/rules/cc-backend-tests-required.mdc`](.cursor/rules/cc-backend-tests-required.mdc); targeted Gradle runs.

---

## Mermaid — LOC request with manageCC-like IP gate

```mermaid
flowchart LR
  req[LOC_request]
  getTxn[getTransactionAuditProcessor]
  getAttr[getTransactionAuditAttrProcessor]
  valIp[validateCustomerIPAddressProcessor]
  biz[LOC_bank_processors]
  req --> getTxn --> getAttr --> valIp --> biz
```

Hybrid handoff: optional branch from `manageLOCTransactionAudit` to `valIp` when customer IP is present on the same request.

Consent (future / other repo): insert consent processors between `getAttr` and `valIp` when LOC wiring matches CC; validate right after trusted customer IP is on context.
