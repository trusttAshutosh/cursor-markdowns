---
name: Invoke lib submit application from cc-mgmt
overview: Ensure the credit card repo invokes the lib's AddOn Card submit-application flow the same way it invokes account info (lib), and document how to run with lib branch ddp-fea-addon-credit-card-request-application to test request/URL parsing.
todos: []
isProject: false
---

# Invoke lib submit application from credit card repo (test request/URL parsing)

## Current state

**How account info is invoked from credit card repo (lib):**

- **Orchestration path:** `api/v1/getLOCOffers` with body `{ request, headers }` → gateway → `RequestProcessorImpl` → orchestration XML (`common_loanOnCards.xml`) → **CardSummaryProcessor** → `LoanOnCardServicePartnerDiscoveryService.getCardSummary(executionContext)` (lib). The lib then runs card summary and account info internally.
- **Direct path (if present):** A controller can also call an app service that builds context and calls the same lib service.

**How submit application is invoked today:**

- **Direct REST only:** `POST /api/v2/addOnCard/submitApplication` → [AddOnCardController](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/controller/AddOnCardController.java) → [AddOnCardService.submitAddOnCardApplication](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AddOnCardService.java) (credit card) → builds `ExecutionContext` (partner_code, user_id, aan, addon_name, pan_card, etc.) → **infraAddOnCardService.submitAddOnCardApplication(ctx)** (lib). So the lib **is** already invoked in the same way: app builds context and calls the lib interface.

So the “similar” invocation (app → lib) is already in place for submit application via the v2 endpoint. What may be missing is the **orchestration path** so you can hit the same flow via `api/v1/submitAddOnCardApplication` with a `{ request, headers }` body (like `dummyCrudV1` / getLOCOffers).

---

## Goal

- Use the **credit card repo** to drive the **lib’s** submit-application flow so you can test that **request**, **URL**, and everything inside the request are parsed correctly by your changes in the lib branch **ddp-fea-addon-credit-card-request-application**.

---

## Plan

### 1. Keep using the existing v2 path (no code change)

The existing flow already invokes your lib code:

- **Credit card:** [AddOnCardController](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/controller/AddOnCardController.java) `POST /api/v2/addOnCard/submitApplication` → [AddOnCardService.submitAddOnCardApplication](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AddOnCardService.java) → builds `ExecutionContext` and calls **lib** `AddOnCardService.submitAddOnCardApplication(ctx)`.

So you can test request/URL parsing **today** by:

- Building and running **credit card** with the **lib** coming from branch **ddp-fea-addon-credit-card-request-application** (see “How to run with the lib branch” below).
- Calling `POST .../api/v2/addOnCard/submitApplication` with the same headers and body you use today.
- Setting breakpoints in the **lib** where URL and request are built/sent (see “Where to verify parsing in the lib” below).

No change to the credit card repo is required for this path.

---

### 2. (Optional) Add orchestration path so v1 mirrors account info

To invoke submit application **via orchestration** (same style as getLOCOffers / account info):

- **In credit card repo:** Add a request in the orchestration XML that points at the lib’s processor.
  - File: [deploy/application/orchestration/common_loanOnCards.xml](novopay-platform-creditcard-management/deploy/application/orchestration/common_loanOnCards.xml).
  - Root is `<CreditCardManagement>`; parser uses `tenant` on root or defaults to `"product"`.
  - Add a block:

```xml
    <Request name="submitAddOnCardApplication">
        <Processors>
            <Processor bean="submitAddOnCardApplicationProcessor" />
        </Processors>
    </Request>
    

```

- **In lib repo (branch ddp-fea-addon-credit-card-request-application):** Ensure there is a Spring bean **submitAddOnCardApplicationProcessor** that implements the orchestration processor contract and calls the existing lib flow (e.g. `AddOnCardService.submitAddOnCardApplication(executionContext)`). If that processor does not exist on that branch, add it (e.g. in `infra-transaction-hdfc`) and ensure it is a `@Processor` that delegates to the same service used by the v2 path.

Then you can call:

- **URL:** `POST http://localhost:8016/cc-mgmt/api/v1/submitAddOnCardApplication`
- **Body:** `{ "request": { aan, addon_name, pan_card, ... }, "headers": { tenant_code, stan, user_id, ... } }`

Same gateway/orchestration stack as getLOCOffers; the only difference is the request name and the processor that calls the lib. This is “similarly” to how account info is invoked via getLOCOffers.

---

### 3. How to run with the lib branch (so your parsing changes are used)

To test that **request, URL, and payload** are parsed correctly by your lib changes:

1. **Checkout the lib branch:** In **novopay-platform-lib**, checkout **ddp-fea-addon-credit-card-request-application**.
2. **Run credit card with composite build:** From **novopay-platform-creditcard-management**, run (e.g. `gradlew bootRun`). [settings.gradle](novopay-platform-creditcard-management/settings.gradle) has `includeBuild '../novopay-platform-lib'`, so the lib that is compiled and used at runtime is the one in the sibling folder (your branch).
3. **Call the submit-application endpoint:**
  - Either **v2:** `POST http://localhost:8016/cc-mgmt/api/v2/addOnCard/submitApplication` with headers and JSON body (aan, addonName, panCard, etc.).
  - Or **v1 (if you add orchestration):** `POST http://localhost:8016/cc-mgmt/api/v1/submitAddOnCardApplication` with body `{ "request": { ... }, "headers": { ... } }`.

The code path that runs will be in the **lib** (your branch): `AddOnCardService` (impl) → `SubmitAddOnCardApplicationService` → URL and request building → `AbstractSoapPostWebServiceExecutor`.

---

### 4. Where to verify parsing in the lib

Use breakpoints in the **lib** (branch ddp-fea-addon-credit-card-request-application) to confirm URL and request content:


| What to verify                         | File (lib)                                                                                                                                                                           | Location                                                                                                                              |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **URL** used for the SOAP call         | [AbstractSoapPostWebServiceExecutor.java](novopay-platform-lib/infra-transaction-interface/src/main/java/in/novopay/infra/core/AbstractSoapPostWebServiceExecutor.java)              | Line ~169: `String serviceURL = getServiceURL();` and line ~186: `httpClient.post(serviceURL, ...)`                                   |
| **Request body** (data/rec segments)   | [SubmitAddOnCardApplicationService.java](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationService.java) | `buildDataString(executionContext)`, `buildRecString(executionContext)`, and `prepareRequest(executionContext)` (data, rec, innerXml) |
| **Final SOAP string** sent to the bank | [AbstractSoapPostWebServiceExecutor.java](novopay-platform-lib/infra-transaction-interface/src/main/java/in/novopay/infra/core/AbstractSoapPostWebServiceExecutor.java)              | Lines ~182–186: `strMsg = modifyRequestString(...)` and `httpClient.post(..., strMsg, ...)`                                           |


So: **request** parsing is best checked in `SubmitAddOnCardApplicationService` (data/rec built from `ExecutionContext`); **URL** and **final request string** are best checked in `AbstractSoapPostWebServiceExecutor`.

---

## Summary

- **No change required** to the credit card repo if you only need to test parsing: the existing **v2** endpoint already invokes the lib the same way the app invokes “add account info” (app builds context → calls lib).
- **Optional:** Add the **orchestration** request `submitAddOnCardApplication` in cc-mgmt and ensure the lib branch has **submitAddOnCardApplicationProcessor** so you can also test via **v1** with `{ request, headers }`.
- **To test your lib branch:** Use lib branch **ddp-fea-addon-credit-card-request-application** and run cc-mgmt with `includeBuild '../novopay-platform-lib'`, then hit the submit-application endpoint and break in the lib at the points above to confirm request and URL are parsed correctly.

