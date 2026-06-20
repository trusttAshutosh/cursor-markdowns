---
name: Submit AddOn Card integration and test
overview: Wire the credit-card-management app to the lib's SubmitAddOnCardApplicationService (same pattern as accountInfo/cardSummary), add an API to trigger submit add-on application, and provide steps and curl to test request parsing (URL + SOAP body) without relying on bank response.
todos: []
isProject: false
---

# Submit Add-On Card Application integration and request-parsing test

## Current state

**accountInfo flow (for reference)**  

- In credit-card-management, “account info” is **not** exposed as a separate API. It runs inside the **card summary** flow.  
- Flow: `GET /api/v2/addOnCard/cardSummary/{client_reference_code}` → [AOCCardSummaryService.getCardSummary()](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AOCCardSummaryService.java) → `LoanOnCardServicePartnerDiscoveryService.submitAccountInfo(executionContext)` → (lib HDFC) → [SubmitAccountInfoService.process()](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAccountInfoService.java) → bank SOAP (different endpoint: ActiveCreditCardsAccountSummaryApplicationServiceSpi).  
- So the “accountInfo” you test via Postman is effectively the **card summary** API; the bank call is SubmitAccountInfoService (account summary SOAP), not the `requestAddOnCard` SOAP.

**Submit application flow (gap)**  

- Lib side is implemented: [AddOnCardServiceHdfc](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/transaction/hdfc/service/impl/AddOnCardServiceHdfc.java) → [SubmitAddOnCardApplicationService.process()](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationService.java) → same SOAP shape as your curl (`requestAddOnCard`, AddOnCreditCardRequestApplicationServiceSpi).  
- Credit-card-management does **not** call `AddOnCardServicePartnerDiscoveryService.submitAddOnCardApplication()` anywhere. So there is no app API that triggers the submit-application bank call.  
- Credit-card-management already depends on `infra-transaction-hdfc` and `infra-transaction-interface` ([build.gradle](novopay-platform-creditcard-management/build.gradle)); the lib’s `AddOnCardService` (and thus `SubmitAddOnCardApplicationService`) is available once the integration is wired.

---

## Goal

- Integrate submit add-on application in **novopay-platform-creditcard-management** so that a credit-card app API builds `ExecutionContext`, calls the lib’s `submitAddOnCardApplication`, and (for testing) allows you to verify **request parsing** (URL + SOAP body) without depending on a successful bank response.

---

## 1. Clarification: accountInfo vs submit application

- **accountInfo** in the app = card summary API → **LoanOnCardService.submitAccountInfo** → SubmitAccountInfoService (account summary SOAP).  
- **Submit application** = **AddOnCardService.submitAddOnCardApplication** → SubmitAddOnCardApplicationService → `requestAddOnCard` SOAP (your second curl).  
- The lib has both; the app currently uses only the former (via `LoanOnCardServicePartnerDiscoveryService` in [AOCCardSummaryService](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AOCCardSummaryService.java)).

---

## 2. ExecutionContext keys required by SubmitAddOnCardApplicationService

From [SubmitAddOnCardApplicationService](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationService.java) (prepareRequest / buildDataString / buildRecString):


| Key                                                          | Source (suggestion in app)                                  |
| ------------------------------------------------------------ | ----------------------------------------------------------- |
| `partner_code`                                               | `"Hdfc"` (for partner discovery)                            |
| `aan`                                                        | Transaction audit / attributes (AAN from card summary flow) |
| `addon_name`                                                 | Recipient name                                              |
| `pan_card`                                                   | Recipient PAN                                               |
| `relationship`                                               | Recipient relationShipType                                  |
| `date_of_birth`                                              | Recipient DOB (format ddMMyyyy)                             |
| `mem_category`                                               | Optional / config                                           |
| `mem_sub_cat`                                                | Optional / config                                           |
| `customer_id`                                                | Optional / case number                                      |
| `dept`                                                       | Optional (default "Net-banking")                            |
| `mobile_number`                                              | Recipient mobile                                            |
| `email`                                                      | Recipient emailId                                           |
| `external_reference_no`, `transacting_party_code`, `user_id` | Optional overrides                                          |


AAN is stored in transaction attributes by [AOCCardSummaryService.getCardSummary()](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AOCCardSummaryService.java) (via `locUtils.createOrUpdateAttribute(transactionAudit.getId(), AAN, ...)`). Recipient data is in [CustomerRelationshipDetails](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/entity/CustomerRelationshipDetails.java) (name, mobileNumber, pan, dob, relationShipType, emailId).

---

## 3. Implementation plan (credit-card-management)

### 3.1 Add a service that builds context and calls the lib

- Add a method (e.g. in a new or existing service) that:
  - Takes `clientReferenceCode` and optionally a **recipient identifier** (e.g. `recipientId` or use first recipient).
  - Loads `TransactionAudit` by client reference and ensures AAN exists (e.g. from attributes via existing LOCUtils or equivalent).
  - Loads recipient(s) for that transaction (e.g. [CustomerRelationshipDetailsDaoService.getCustomerRelationShipDetails(transactionAuditId)](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/dao/CustomerRelationshipDetailsDaoService.java)).
  - Builds an `ExecutionContext` with `partner_code`, `aan`, and the keys above mapped from the chosen recipient (dob → ddMMyyyy).
  - Injects [AddOnCardServicePartnerDiscoveryService](novopay-platform-lib/infra-transaction-interface/src/main/java/in/novopay/infra/transaction/service/impl/AddOnCardServicePartnerDiscoveryService.java) (same style as [AOCCardSummaryService](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/service/AOCCardSummaryService.java) injecting `LoanOnCardServicePartnerDiscoveryService`).
  - Calls `addOnCardServicePartnerDiscoveryService.submitAddOnCardApplication(executionContext)`.

### 3.2 Expose an API for testing (and later for real use)

- Add an endpoint, e.g. `POST /api/v2/addOnCard/submitApplication` (or `GET` for quick curl), with at least:
  - Path or query: `client_reference_code`.
  - Optional: `recipient_id` or use first recipient.
  - Headers: same as existing add-on APIs (e.g. userId, clientCode, tenantCode, stan, channelCode) if needed for audit.
- Controller calls the new service method.

### 3.3 Optional: return or log outgoing request for “request only” testing

- The lib’s SOAP executor puts the built request into the context with `executionContext.putLocal("service_request", strMsg)` **before** calling the bank (see AbstractSoapPostWebServiceExecutor / AbstractSoapReqStringServiceExecutor in lib). If the bank call fails (timeout, 4xx/5xx), the exception propagates and the app never reads the context.
- To verify request parsing without depending on bank response:
  - **Option A (recommended):** In the new service, **catch** the exception (e.g. `NovopayNonFatalException` / `NovopayFatalException`) after `submitAddOnCardApplication(executionContext)`, then read `executionContext.getLocal("service_request")` (and optionally `service_response` if present). Log this in a structured way, or return it in the API response (e.g. under a query param `?debugRequest=true` or only in non-prod) so you can compare the SOAP body and URL (URL is in lib config `hdfc.soap.addon.card.request.url`) with your expected curl.
  - **Option B:** Rely on existing lib unit tests ([SubmitAddOnCardApplicationServiceTest](novopay-platform-lib/infra-transaction-hdfc/src/test/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationServiceTest.java)) for request build; app integration then only verifies that the app builds context correctly and calls the lib (and optionally log `service_request` on success).

---

## 4. Config (lib)

- URL and other params for submit application are in [SubmitAddOnCardApplicationService](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationService.java) (`@NovopayConfig`):
  - `hdfc.soap.addon.card.request.url` (default: `https://hbentbpuatap.hdfcbankuat.com:9444/.../AddOnCreditCardRequestApplicationServiceSpi`)
  - `hdfc.soap.addon.card.bank.code`, `channel`, `transaction.branch`, `user.id`, `transacting.party.code`, `external.reference.no`
- Ensure credit-card-management (or shared config) has these set for the environment where you run the app (e.g. UAT) so the built request targets the same base URL as your curl.

---

## 5. Steps to test “request parsing” with a credit-card app curl

1. **Prerequisites**
  - Run credit-card app (novopay-platform-creditcard-management) with lib branch that includes `SubmitAddOnCardApplicationService` (e.g. `ddp-fea-addon-credit-card-request-application`).
  - Have at least one transaction with:
    - Existing card summary already fetched (so AAN is stored in transaction attributes).
    - At least one recipient (CustomerRelationshipDetails) with name, PAN, DOB, relationship, mobile, email.
2. **Get a valid client_reference_code**
  - Use a client reference that already went through add-on card flow (e.g. after calling `POST /api/v2/addOnCard/create` and then `GET /api/v2/addOnCard/cardSummary/{client_reference_code}` so AAN is present).
3. **Call the new submit-application API**
  - Example (after implementation), using the same headers as your other add-on APIs:

```bash
   curl -X POST 'http://<host>:<port>/api/v2/addOnCard/submitApplication?client_reference_code=<client_reference_code>' \
     -H 'Content-Type: application/json' \
     -H 'userId: <userId>' \
     -H 'clientCode: <clientCode>' \
     -H 'tenantCode: <tenantCode>' \
     -H 'stan: <stan>' \
     -H 'channelCode: <channelCode>'
   

```

- If you add a debug flag: `...?client_reference_code=...&debugRequest=true` and the handler returns or logs `service_request`, use that to compare with your bank SOAP.

1. **Verify request parsing (without caring about bank response)**
  - **If you implemented Option A:** When the bank returns an error or times out, the app can still return 200 with (or log) the outgoing SOAP from `service_request`. Compare that and the configured URL to your working curl:
    - Same endpoint path and query (URL from config).
    - Same SOAP shape: `requestAddOnCard`, `arg0` (context), `arg1` with `requestXML` containing the inner `<emsg>` with `<data>` and `<rec>` (BBIADN, 400-char rec).
  - **If you only have logs:** Ensure logs print the full SOAP request (and URL) when an exception occurs so you can confirm the rec/data segments match the format expected by the bank (and your second curl).
2. **Optional: unit test in app**
  - Unit test the new service: mock `AddOnCardServicePartnerDiscoveryService`, call the service method with a known transaction + recipient, verify the execution context passed to the lib contains the expected keys (aan, addon_name, pan_card, relationship, date_of_birth, mobile_number, email, etc.) and that the mock was invoked with `submitAddOnCardApplication`.

---

## 6. Summary diagram

```mermaid
sequenceDiagram
    participant Client
    participant AddOnCardController
    participant AOCSubmitService
    participant AddOnCardServicePDS
    participant SubmitAddOnCardAppSvc
    participant Bank

    Client->>AddOnCardController: POST /submitApplication?client_reference_code=...
    AddOnCardController->>AOCSubmitService: submitApplication(clientRef, ...)
    AOCSubmitService->>AOCSubmitService: Load TransactionAudit + AAN + Recipient
    AOCSubmitService->>AOCSubmitService: Build ExecutionContext (aan, addon_name, pan, ...)
    AOCSubmitService->>AddOnCardServicePDS: submitAddOnCardApplication(ctx)
    AddOnCardServicePDS->>SubmitAddOnCardAppSvc: process(ctx)
    SubmitAddOnCardAppSvc->>SubmitAddOnCardAppSvc: prepareRequest(ctx) -> SOAP body
    SubmitAddOnCardAppSvc->>SubmitAddOnCardAppSvc: putLocal("service_request", strMsg)
    SubmitAddOnCardAppSvc->>Bank: HTTP POST (URL from config) + SOAP
    alt Bank error / timeout
        Bank-->>SubmitAddOnCardAppSvc: error
        SubmitAddOnCardAppSvc-->>AOCSubmitService: exception
        AOCSubmitService->>AOCSubmitService: catch; read ctx.getLocal("service_request")
        AOCSubmitService-->>Client: e.g. 200 + debug request body (or log)
    else Success
        Bank-->>SubmitAddOnCardAppSvc: 200 + response
        SubmitAddOnCardAppSvc-->>AOCSubmitService: return
        AOCSubmitService-->>Client: 200 + business response
    end
```



---

## 7. Files to add or change (credit-card-management)


| Action       | File                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Add / extend | New service class (e.g. `AOCSubmitApplicationService`) or extend `AOCCardSummaryService` / a dedicated “add-on card operations” service that builds ExecutionContext and calls `AddOnCardServicePartnerDiscoveryService.submitAddOnCardApplication`.                                                                                                                                                                                                                                                    |
| Inject       | `in.novopay.infra.transaction.service.impl.AddOnCardServicePartnerDiscoveryService` in that service.                                                                                                                                                                                                                                                                                                                                                                                                    |
| Add          | New API in [AddOnCardController](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/controller/AddOnCardController.java): e.g. `POST /api/v2/addOnCard/submitApplication` (or GET with query param) calling the new service.                                                                                                                                                                                                                                                    |
| Use          | Existing [LOCUtils](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/loc/util/LOCUtils.java) / transaction attributes for AAN; [CustomerRelationshipDetailsDaoService](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/dao/CustomerRelationshipDetailsDaoService.java) and [CustomerRelationshipDetails](novopay-platform-creditcard-management/src/main/java/in/novopay/creditcard/entity/CustomerRelationshipDetails.java) for recipient fields. |


No changes are required in the lib for the integration; only the credit-card-management app needs the new service, controller endpoint, and optional “return/log service_request on error” logic for request-parsing verification.