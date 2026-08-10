---
name: KYC Engine Platformization
overview: Visual map plus approvals pack - KYC across CC, BO, lib, India Stack on ddp-qa QA.
todos:
  - id: schema-align
    content: "QA/ddp-qa: apply V400044 for ddp kyc_detail.product_source; align tenant migration template"
    status: pending
  - id: lib-dtos
    content: Add shared KycEngine DTOs/enums to infra-transaction-interface
    status: pending
  - id: extract-hdfc-client
    content: Extract HdfcKycEngineClient + transformer from BO KycService into infra-transaction-hdfc
    status: pending
  - id: product-routing-registry
    content: Replace productSource if/else with KycProductRoutingStrategy + per-product masterdata keys
    status: pending
  - id: generic-bo-bridge
    content: Move KycEngineBridgeService HTTP logic to lib KycEngineBoClient; thin CC wrapper
    status: pending
  - id: india-stack-dedupe
    content: "Consolidate consent/decrypt processors into india-stack; fix orchestration bean refs on ddp-qa"
    status: pending
isProject: false
---

# KYC - CC / BO / lib / India Stack (`ddp-qa` QA)

**TLDR:** QA runs **two KYC paths** - CUG **Engine** (CC→BO→HDFC REST) and legacy **DAP** (CC→India Stack→lib SOAP). Engine code is split across CC+BO today; **platformize HDFC transport + DTOs + product bridge into lib**, keep BO as journey host, India Stack for DAP/NPCI only. CC keeps CUG, APIs, and audit.

**QA:** `np-ddp-qa-app` | gateway `ddp-qa.novopay.in` | test tenant `dsa`

---

## 1. What lives where TODAY (ddp-qa)

```mermaid
flowchart TB
  subgraph CC ["CC creditcard-management"]
    direction TB
    CC_E1["ENGINE: Initiate/Get/Apply processors"]
    CC_E2["ENGINE: KycEngineBridgeService"]
    CC_E3["ENGINE: CugGuard StatusCache ApplyAudit"]
    CC_E4["ENGINE: 5 APIs + orchestration XML"]
    CC_L1["LEGACY: FetchEkycDetailsProcessor wrapper"]
    CC_L2["LEGACY: validateAadhaar wrapper + txn audit"]
    CC_S1["SHARED: EkycAuditMappingService"]
  end

  subgraph BO ["BO banking-origination"]
    direction TB
    BO_E1["ENGINE: KycService + KycTransformer"]
    BO_E2["ENGINE: KycInitiateController REST"]
    BO_E3["ENGINE: kyc_detail DAO + callbacks"]
    BO_E4["ENGINE: ES/S3 APPLICATION_DATA"]
    BO_O1["OBP: KycCommonService SMS geo"]
  end

  subgraph LIB ["lib novopay-platform-lib"]
    direction TB
    LIB_L1["LEGACY: EkycService interface"]
    LIB_L2["LEGACY: EkycServiceHdfc SOAP clients"]
    LIB_L3["LEGACY: WSDLs OTP bio face iris"]
    LIB_P1["PLUMBING: ExecutionContext HttpClient Cache Config"]
    LIB_X["ENGINE: none on ddp-qa"]
  end

  subgraph IS ["India Stack INDIA-STACK"]
    direction TB
    IS_L1["LEGACY: fetchEkycDetails API"]
    IS_L2["LEGACY: OTP Bio Face Iris processors"]
    IS_L3["LEGACY: AbstractEkycProcessor geo SMS"]
    IS_N1["NPCI: doAEPSeKYC executor"]
    IS_X["ENGINE: none"]
  end

  subgraph HDFC ["HDFC bank"]
    HDFC_SOA["SOAP UIDAI DAP"]
    HDFC_ENG["REST KYC Engine Pehchaan"]
    NPCI["NPCI network"]
  end
```

---

## 2. RUNTIME - Engine path CUG (Track B)

```mermaid
sequenceDiagram
  participant FE as Frontend
  participant GW as Gateway_v1
  participant CC as CC
  participant BO as BO
  participant H as HDFC_Engine_REST
  participant DB as kyc_detail

  FE->>GW: initiateKycEngineForCCDSA
  GW->>CC: orchestration
  CC->>CC: CugGuard
  CC->>BO: POST kycInitiate productSource=CC
  BO->>H: PS_InitiateSyncKycRequest
  H-->>BO: kycUrl journeyId
  BO->>DB: insert kyc_detail
  BO-->>CC: kyc_url timings
  CC-->>FE: redirect Pehchaan

  FE->>GW: getKycEngineStatusForCC
  GW->>CC: poll
  CC->>BO: POST getKycStatus
  BO->>H: GETKYCStatus
  H-->>BO: status addresses
  BO-->>CC: kyc_status customer
  CC-->>FE: poll response

  FE->>GW: applyKycEngineStatusForCCDSA
  GW->>CC: apply
  CC->>BO: getKycStatus cache or live
  CC->>CC: transaction_audit attrs
```

**Not in path:** India Stack, lib EkycService

---

## 3. RUNTIME - Legacy DAP path non-CUG

```mermaid
sequenceDiagram
  participant FE as Frontend
  participant GW as Gateway_v1
  participant CC as CC
  participant IS as India_Stack
  participant LIB as lib_EkycService
  participant H as HDFC_SOAP

  FE->>GW: fetchEkycDetailsForCCDSA
  GW->>CC: orchestration
  CC->>CC: FetchEkycDetailsProcessor audit wrapper
  CC->>IS: internal API fetchEkycDetails v1
  IS->>IS: OTP or Bio Face Iris processor
  IS->>LIB: EkycServiceHdfc
  LIB->>H: UIDAI SOAP
  H-->>LIB: demographic POI POA
  LIB-->>IS: ExecutionContext
  IS-->>CC: eKYC response
  CC->>CC: transaction_audit attrs
  CC-->>FE: in-app OTP result
```

**Not in path:** BO KycService, HDFC Engine REST

---

## 4. Approvals required

### Goal

Enable **new HDFC products/tenants** on KYC Engine with **config + thin product adapters**, not copying `KycService` / bridge code per product.

### Non-goals

| Will not do |
|-------------|
| Products call HDFC Engine REST directly |
| Fold KYC Engine into India Stack |
| Replace BO as journey host (`kyc_detail`, callbacks, ES/S3) |
| Change public CC API names or FE contract during platformization |
| Remove legacy DAP path (`fetchEkycDetails` via India Stack) |

### Alternatives

```mermaid
flowchart LR
  subgraph rejected ["Rejected"]
    A1["CC to HDFC direct"]
    A2["Engine in India Stack"]
    A3["Single mega KYC service"]
  end
  subgraph chosen ["Chosen"]
    C1["lib transport plus contracts"]
    C2["BO journey host"]
    C3["Product bridge plus audit in CC"]
    C4["DAP stays India Stack plus lib SOAP"]
  end
  rejected -.->|"duplication or wrong boundary"| chosen
```

| Option | Why rejected |
|--------|----------------|
| CC → HDFC direct | Duplicates BO; loses callbacks/idempotency |
| Engine in India Stack | Wrong protocol; IS owns sync DAP/NPCI only |
| One new KYC microservice | Extra deploy surface; BO already hosts journey |

### Deploy order (coordinated)

```mermaid
flowchart LR
  F1["Flyways schema config apis"] --> F2["lib release"]
  F2 --> F3["BO delegates to lib"]
  F3 --> F4["CC thin bridge"]
  F4 --> F5["India Stack dedupe"]
```

| Step | Repo | Change |
|------|------|--------|
| 1 | masterdata, initial-setup, BO | configs, api registry, `kyc_detail` schema |
| 2 | lib | DTOs, `HdfcKycEngineClient`, `KycEngineBoClient`, routing strategy |
| 3 | BO | `KycService` delegates; keep REST + persistence |
| 4 | CC | swap bridge to lib client; APIs unchanged |
| 5 | India Stack | consent/decrypt dedupe only |

### Tenant and security (unchanged model)

```mermaid
flowchart TB
  REQ["Request x-tenant-Code"] --> CC_BO["CC or BO"]
  CC_BO --> SCHEMA["tenant_banking_origination.kyc_detail"]
  CC_BO --> REDIS["tenant-scoped cache"]
  HDFC_CB["Bank callback"] --> GW["Gateway tenant path"] --> BO
```

- No hardcoded `dsa`/`ddp` in KYC Java
- PII/audit: products write own `transaction_audit`; bank callbacks land on BO only

### Risks

| Risk | Mitigation |
|------|------------|
| lib version skew across CC/BO | composite `includeBuild`; release lib first |
| Dual path Engine + DAP forever | config routing per CUG; both paths tested |
| `kyc_detail` schema drift per tenant | single product migration template |
| Refactor breaks QA engine E2E | behavior-neutral phase 1 DTOs; delegate-only phase 2 |

### Success criteria (sign-off when)

- [ ] New product adds **routing strategy + masterdata keys** only (no new BO `if productSource`)
- [ ] Product bridge is **lib `KycEngineBoClient`** with `productSource` param
- [ ] HDFC async I/O lives in **one lib client** (unit-tested)
- [ ] CC public APIs and legacy DAP path **unchanged**
- [ ] QA engine + legacy regression pass on `ddp-qa`

---

## 5. TARGET - what CAN move (future)

```mermaid
flowchart LR
  subgraph stay_cc ["STAY in CC"]
    S1["CugGuard"]
    S2["ApplyAudit transaction_audit"]
    S3["5 API names orchestration XML"]
    S4["FetchEkycDetails audit wrapper"]
  end

  subgraph stay_bo ["STAY in BO"]
    B1["KycInitiateController"]
    B2["kyc_detail callbacks ES S3"]
    B3["KycCommonService OBP"]
  end

  subgraph stay_is ["STAY in India Stack"]
    I1["fetchEkycDetails orchestration"]
    I2["DAP processors NPCI AEPS"]
    I3["dedupe consent decrypt here"]
  end

  subgraph move_lib ["MOVE to lib"]
    M1["HdfcKycEngineClient async REST"]
    M2["KycTransformer HDFC JSON POJOs"]
    M3["KycEngineBoClient generic"]
    M4["Shared DTOs enums routing strategy"]
    M5["EkycService already here"]
  end

  subgraph thin_bo ["BO becomes thin"]
    T1["KycService delegates to lib client"]
  end

  subgraph thin_cc ["CC becomes thin"]
    T2["Bridge uses lib KycEngineBoClient"]
  end

  move_lib --> thin_bo
  move_lib --> thin_cc
  thin_bo --> stay_bo
  thin_cc --> stay_cc
```

---

## 6. Move matrix (one glance)

| Component | Today | Future home |
|-----------|-------|-------------|
| Engine processors + CUG | CC | **CC** |
| Engine bridge HTTP | CC | **lib** `KycEngineBoClient` |
| Engine apply audit | CC | **CC** |
| `KycService` HDFC HTTP | BO | **lib** `HdfcKycEngineClient` |
| `kyc_detail` callbacks | BO | **BO** |
| `KycTransformer` routing | BO | **lib** strategy + config |
| SOAP eKYC transport | lib | **lib** (done) |
| `fetchEkycDetails` orchestration | India Stack | **India Stack** |
| DAP OTP/bio processors | India Stack | **India Stack** |
| `decryptUsingPrivateKey` | CC bean refs IS XML | **India Stack** |
| `CheckIfConsentApproved` | duplicated CC+IS | **India Stack** |

---

## 7. QA blockers (ddp-qa only)

| Item | Status |
|------|--------|
| Gateway APIs `V702135` | 404 until flyway applied |
| BO `V400044` product_source ddp | not on branch |
| Bank status URL from QA host | timeout - use pehchaan-uat2 alternate |

---

## 8. Phases (short)

1. **QA fix** - flyways + status URL
2. **lib** - DTOs + `HdfcKycEngineClient` + `KycEngineBoClient`
3. **BO** - delegate to lib; product routing registry
4. **CC** - thin bridge; keep audit/CUG
5. **India Stack** - dedupe consent/decrypt only
