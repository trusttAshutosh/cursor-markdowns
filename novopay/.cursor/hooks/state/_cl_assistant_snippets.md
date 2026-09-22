
# ff96e707-1f7d-46da-a220-44d919fad31f


## asst snippet 1
Confirming `mobile_match_flag` is missing from audit attrs — checking the FE attribute fetch and bank filler1 on status.


## asst snippet 2
**Verdict:** Lead ran KYC Engine EKYC successfully, but bank status returned **no `filler1` and `kycMobileNo=null`**, so **`mobile_match_flag` was never written**. FE then asked for it and got an empty map.
---
### Why `mobile_match_flag` is missing
Bank/BO status snapshot for this lead:
---
- `kycMobileNo=null`
- `filler2=` blank
- **no `filler1`** (so nothing to map to Y/N)
- also odd bank fields: `kycType=cKYC`, `externalRefNo=UATTEST133`, bank `kycJourneyId=P10072024125210` (not the initiate journey)
---
ES behaviour matches the matrix: preferred mode **EKYC** + blank/missing `filler1` → **do not persist** `mobile_match_flag` (no phone-compare fallback).
---
**TL;DR:** Journey is fine through EKYC complete + manageCC; mobile-match attr is absent because bank status gave null mobile and no filler1, and EKYC does not derive from lead mobile.


## asst snippet 3
**Partly yes for our code, mostly no for the bank payload.**
---
| Layer | Valid? | Why |
| --- | --- | --- |
| **Our ES rule** | Yes | Preferred mode `EKYC` + no bank `filler1` Y/N → do **not** write `mobile_match_flag`. Matches the remote QA/UAT matrix. |
| **FE empty attrs** | Expected consequence | DB has no attr → `getCCTransactionAttributes` returns `{}`. |
| **This bank status** | Suspect / not a clean prod-like case | `kycMobileNo=null`, no `filler1`, `kycType=cKYC` while message is `EKYC-COMPLETED`, `externalRefNo=UATTEST133`, bank journey id ≠ initiate journey `D18092026348326`. Looks like reused/stale UAT KYC data, not a normal live EKYC status. |
---
So: **valid gap scenario for “EKYC + blank filler1 → flag not stored”**, but **not a trustworthy real-customer EKYC match/mismatch sample** until bank returns `filler1` Y/N (and usually `kycMobileNo`).
---
**TL;DR:** Code behaved as designed; this lead’s bank response is the odd part, not a good golden EKYC mobile-match case.


## asst snippet 4
Persisted on `transaction_audit_attributes` during **poll** and **apply**. Also may persist `aadhar_phone_number` from bank `kycMobileNo` when present.
---
| Scenario | Bank `filler1` | Phones | Stored? | Value |
| --- | --- | --- | --- | --- |
| EKYC match | `Y` | any | Yes | `Y` |
| EKYC mismatch | `N` | any | Yes | `N` |
| EKYC, blank/missing `filler1` | blank / absent | any | **No** | — |
| EKYC, invalid `filler1` | e.g. garbage | any | **No** | — |
| CKYC, bank sends `Y`/`N` | `Y` or `N` | any | Yes | bank value (`Y`/`N`) |
| CKYC, blank `filler1`, KYC mobile = lead mobile | blank | both present, last-10 match | Yes | `Y` |
| CKYC, blank `filler1`, KYC mobile ≠ lead mobile | blank | both present, last-10 differ | Yes | `N` |
| CKYC, blank `filler1`, missing KYC or lead mobile | blank | incomplete | **No** | — |
| Both blank / nothing to derive | — | — | **No** | — |
---
Rules in short:
1. Bank `filler1` is `Y`/`N` → store that (EKYC or CKYC).
2. Else only if preferred mode is **CKYC** → compare last-10 digits of KYC mobile vs lead mobile → store `Y` or `N`.
3. EKYC never phone-compares when `filler1` is blank.
---
**Your QA lead (`DSA3941789711540`):** EKYC + no `filler1` + `kycMobileNo=null` → **not stored** (row 3).
---
**TL;DR:** Store only when we have bank `Y`/`N`, or CKYC phone compare can decide; value is always `Y` or `N` when stored.


## asst snippet 5
Persisted on `transaction_audit_attributes` during **poll** and **apply**. Also may persist `aadhar_phone_number` from bank `kycMobileNo` when present.
---
| S.No. | Scenario | Bank `filler1` | Phones | Stored? | Value |
| --- | --- | --- | --- | --- | --- |
| `1` | EKYC match | `Y` | any | Yes | `Y` |
| `2` | EKYC mismatch | `N` | any | Yes | `N` |
| `3` | EKYC, blank/missing `filler1` | blank / absent | any | **No** | — |
| `4` | EKYC, invalid `filler1` | e.g. garbage | any | **No** | — |
| `5` | CKYC, bank sends `Y`/`N` | `Y` or `N` | any | Yes | bank value (`Y`/`N`) |
| `6` | CKYC, blank `filler1`, KYC mobile = lead mobile | blank | both present, last-10 match | Yes | `Y` |
| `7` | CKYC, blank `filler1`, KYC mobile ≠ lead mobile | blank | both present, last-10 differ | Yes | `N` |
| `8` | CKYC, blank `filler1`, missing KYC or lead mobile | blank | incomplete | **No** | — |
| `9` | Both blank / nothing to derive | — | — | **No** | — |
---
Rules in short:
1. Bank `filler1` is `Y`/`N` → store that (EKYC or CKYC).
2. Else only if preferred mode is **CKYC** → compare last-10 digits of KYC mobile vs lead mobile → store `Y` or `N`.
3. EKYC never phone-compares when `filler1` is blank.
---
**Your QA lead (`DSA3941789711540`):** S.No. `3` - EKYC + no `filler1` + `kycMobileNo=null` → **not stored**.
---
**TL;DR:** Store only when bank sends `Y`/`N`, or CKYC phone compare can decide; stored value is always `Y` or `N`.


## asst snippet 6
For S.No. `1`, `2`, and `5`, bank `filler1` is already `Y` or `N`, so we store that flag whether or not:
- bank `kycMobileNo` is present, and/or  
- lead mobile is present.
---
Phone compare only matters on S.No. `6`–`8` (CKYC + blank `filler1`).
---
**TL;DR:** “any” = irrelevant for that scenario; bank `Y`/`N` wins.


# c246405c-1abf-4cfc-a2f7-1a1aaeb2aa6b


## asst snippet 1
KYC engine PAN handling shows up in consents-webapp and banking-origination — tracing that path end-to-end.


## asst snippet 2
In the **KYC Engine** path (CC consent portal → CC → Banking Origination → HDFC), PAN is RSA-encrypted on the wire to Novopay, decrypted only in BO, sent **plain** to the bank, and **not stored** on `kyc_detail`.
---
```mermaid
sequenceDiagram
  participant FE as Consent / Agent FE
  participant Auth as Auth getEncryptionKey / getDecryptionKey
  participant CC as Credit Card
  participant BO as Banking Origination
  participant DB as BO kyc_detail
  participant Bank as HDFC KYC Engine
---
  FE->>Auth: getEncryptionKey (PASSWORD-ENCRYPTION-KEY public)
  FE->>FE: RSA-OAEP encrypt plain PAN
  FE->>CC: initiateKycEngineForCCDSA pan_no = RSA cipher
  CC->>BO: bridge panNo = same cipher (no decrypt)
  BO->>Auth: getDecryptionKey (MPIN-ENCRYPTION-KEY private)
  BO->>BO: RSA decrypt → plain PAN
  BO->>Bank: Initiate KYC requestParam.panNo = plain
  BO->>DB: save journey ids/status/url (no PAN column)
  Note over FE,Bank: Status poll / apply: PAN not sent
```
---
| Hop | Who | What is sent / held | Format |
| --- | --- | --- | --- |
| 1. Key fetch | Consent FE | `getEncryptionKey` with `PASSWORD-ENCRYPTION-KEY` | Public key (SPKI) |
| 2. Encrypt | Consent FE (or Agent earlier) | Plain PAN → RSA-OAEP | Base64 cipher |
| 3. Initiate API | FE → Gateway → CC | `pan_no` in `initiateKycEngineForCCDSA` | Still RSA cipher |
| 4. Bridge | CC → BO | `panNo` forwarded as-is | Still RSA cipher (CC does **not** decrypt) |
| 5. Decrypt | BO `KycCommonService.getDecryptedValue` | Private key via `getDecryptionKey` / `MPIN-ENCRYPTION-KEY`; `x-channel-code` WEB → SHA-256 OAEP, else other RSA-OAEP | Plain PAN in memory |
| 6. Bank | BO → HDFC initiate (`hdfc.kyc.async.initiate.url`) | `requestParam.panNo` | **Plain text** |
| 7. DB | BO `kyc_detail` | Journey fields only (`client_reference_number`, `journey_id`, `kyc_url`, status, …) | **PAN not stored** |
| 8. Status / apply | FE poll / bank callback | No PAN | - |
---
SoT matrix: [CC journey - bank API PAN matrix](https://mdshare.trustt.com/md/s/a9CD6eEv96Sw) - KYC initiate = PAN yes, plain; status poll = no PAN.
---
### FE: who encrypts when
---
**Agent assist**  
Agent portal RSA-encrypts PAN when building consent attributes (`consentHelper` / CC screens). Consent portal reuses `attributes.pan_number` as-is for KYC initiate.
---
**Customer (self) assist**  
After OTP, Redux holds PAN as **Base64 of plaintext** (not RSA). On Digital/CKYC, FE Base64-decodes → RSA-encrypts with the public key → sends as `pan_no`.


# a717ff40-a52c-4387-8eae-3b1071682f40


## asst snippet 1
I'll gather every KYC-engine config the bank would recognize, with the DB key for each, so you can confirm UAT vs prod parity.


## asst snippet 2
This is the Credit Card KYC Engine config set (not BKYC TaskAlloc). Pulling the full masterdata seed and live code keys next.


## asst snippet 3
Credit Card **KYC Engine** configs (DSA). Table is what the bank can confirm. Values below are live **Bank UAT** (`dsa_masterdata.configuration`). Prod was not readable from here - fill the last column with bank/ops.
---
### A. Bank KYC Engine contract (what they send / host)
---
| S.No. | What the bank calls it | DB key (`prop_key`) | Bank UAT value now | Same in Prod? |
| --- | --- | --- | --- | --- |
| `1` | Channel ID (`channelId` on Initiate) | `hdfc.cc.kyc.channel.id` | `SFDCA-COPTNR` | **Confirm** - usually same if prod channel is also COPTNR |
| `2` | Product code for eKYC (`prodCd`) | `hdfc.cc.kyc.prod.cd` | `BOTH` | **Confirm** - usually same (`BOTH` per HDFC manual) |
| `3` | Product code for CKYC (`prodCd`) | `hdfc.cc.kyc.ckyc.prod.cd` | `BOTH` | **Confirm** - usually same (`BOTH`) |
| `4` | Initiate KYC Engine URL | `hdfc.kyc.async.initiate.url` | `https://osbsesoauat.hdfcbank.com:5142/KYCEngine/ProxyService/v1/PS_InitiateSyncKycRequest` | **No** - prod host/path will differ; bank must give prod URL |
| `5` | Get KYC Status URL | `hdfc.kyc.async.status.url` | `https://osbsesoauat.hdfcbank.com:5142/KYCEngine/ProxyService/v1/PS_GetKycStatus` | **No** - prod host/path will differ; bank must give prod URL |
| `6` | Initiate call timeout (ms) | `hdfc.kyc.async.initiate.initiate.timeout` | `60000` | **Usually yes** - same unless bank/network needs different |
| `7` | Initiate retry timeout (ms) | `hdfc.kyc.async.initiate.retry.timeout` | `30000` | **Usually yes** |
---
### B. Rollout / pilot switches (bank + product to confirm for go-live)
---
| S.No. | What it means (plain English) | DB key (`prop_key`) | Bank UAT value now | Same in Prod? |
| --- | --- | --- | --- | --- |
| `8` | KYC Engine feature on/off | `creditcard.kyc.engine.cug.enabled` | `TRUE` | **Confirm** - prod should stay `TRUE` once live |
| `9` | Only CUG users use KYC Engine (others blocked / legacy) | `creditcard.kyc.engine.restrict.to.cug` | `TRUE` | **Likely no** - full prod rollout usually needs `FALSE` (all eligible users) |
| `10` | For CUG users: use Engine or old DAP path | `creditcard.kyc.engine.routing.for.cug` | `ENGINE` | **Confirm** - stay `ENGINE` if prod uses KYC Engine |
---
### C. Platform technical (bank usually does not rename these; ops can keep same)
---
| S.No. | What it means | DB key (`prop_key`) | Bank UAT value now | Same in Prod? |
| --- | --- | --- | --- | --- |
| `11` | Internal link CC → Banking Origination base URL (empty = service discovery) | `banking.origination.internal.base.url` | *(empty)* | **Usually yes** (empty on both) |
| `12` | Connect timeout to Banking Origination (ms) | `creditcard.kyc.engine.bridge.connection.timeout.ms` | `5000` | **Usually yes** |
| `13` | Initiate read timeout (ms) | `creditcard.kyc.engine.bridge.initiate.socket.timeout.ms` | `30000` | **Usually yes** |
| `14` | Status poll read timeout (ms) | `creditcard.kyc.engine.bridge.status.socket.timeout.ms` | `60000` | **Usually yes** |
| `15` | Fail-fast when BO keeps failing | `creditcard.kyc.engine.bridge.fail.fast.enabled` | `FALSE` | **Usually yes** |
| `16` | Fail-fast failure count | `creditcard.kyc.engine.bridge.fail.fast.threshold` | `5` | **Usually yes** |
| `17` | Fail-fast window (ms) | `creditcard.kyc.engine.bridge.fail.fast.window.ms` | `60000` | **Usually yes** |
| `18` | Cache successful KYC status poll | `creditcard.kyc.engine.status.cache.enabled` | `TRUE` | **Usually yes** |
| `19` | Status cache TTL (seconds) | `creditcard.kyc.engine.status.cache.ttl.seconds` | `120` | **Usually yes** |
---
Schema for all of the above: `dsa_masterdata.configuration` (service = `BANKING-ORIGINATION` for rows `1`-`7`, `CREDIT-CARD-MANAGEMENT` for `8`-`19`).


# 56dc9aea-af5a-43df-a073-0f1c4ddbde0e


## asst snippet 1
**Are journey SELECTs required?** No for RCA - logs already prove it. Use them only after sim fix, on a **new** DSA (old audits stay address-less).
---
```sql
SELECT id, client_reference_number, reference_number, bank_external_ref_no, journey_id, kyc_type, product_source, kyc_status, is_kyc_changed, updated_on FROM dsa_banking_origination.kyc_detail WHERE client_reference_number IN ('DSA4871789653168','DSA4871789653372','DSA4871789654451') ORDER BY id;
```
---
```sql
SELECT taa.transaction_audit_id, taa.attr_key, LEFT(taa.attr_value,120) AS attr_value FROM dsa_credit_card_mgmt.transaction_audit_attributes taa WHERE taa.transaction_audit_id IN (49206,49207,49208) AND (taa.attr_key LIKE '%address%' OR taa.attr_key IN ('name','gender','dob','kyc_preferred_mode','kyc_status')) ORDER BY taa.transaction_audit_id, taa.attr_key;
```
---
Expect: name/gender present; **no** `address_line_*`.
---
### Simulator (chameleon DB on sim host - usually `localhost:3306/chameleon`, not app DB)
---
```sql
SELECT sc.id AS config_id, sc.api_name, sc.request_type, sr.id AS response_id, sr.validation, sr.response_code, sr.response LIKE '%DIGILOCKER%' AS has_digilocker, LEFT(sr.response,300) AS response_head FROM chameleon.simulator_config sc JOIN chameleon.simulator_response sr ON sr.simulator_config_id = sc.id WHERE sc.api_name = 'GETKYCStatus';
```
---
Update (EKYC - KYC engine supported mode; keeps address fields):
---
```sql
UPDATE chameleon.simulator_response sr JOIN chameleon.simulator_config sc ON sc.id = sr.simulator_config_id SET sr.response = REPLACE(REPLACE(sr.response, '"kycType": "DIGILOCKER"', '"kycType": "EKYC"'), '"kycType":"DIGILOCKER"', '"kycType":"EKYC"') WHERE sc.api_name = 'GETKYCStatus' AND sr.response LIKE '%DIGILOCKER%';
```


## asst snippet 2
Blank Aadhaar address on Personal Details is caused by the **QA KYC status simulator**, not by the KYC engine product change.
---
KYC engine supports **eKYC and cKYC only** (Digilocker is out of scope). The simulator returns a completed KYC with address data, but marks the KYC type as **Digilocker**. Our flow therefore does not treat it as eKYC/cKYC address data, so name and gender are saved and shown, while address is not applied to the application and stays blank on Personal Details.
---
Update the QA `GETKYCStatus` simulator stub so the KYC type is **EKYC** or **CKYC** (matching the journey), and keep the address fields. Restart the simulator service, then retest on a **new** application.
---
`^M` in logs is preexisting line-ending noise in the simulator response - cosmetic only; not the address defect.
```


## asst snippet 3
### Exact simulator SQL (chameleon DB on sim host)
---
```sql
SELECT sc.id AS config_id, sc.api_name, sc.request_type, sr.id AS response_id, sr.validation, sr.response_code, sr.response LIKE '%DIGILOCKER%' AS has_digilocker, LEFT(sr.response, 400) AS response_head FROM chameleon.simulator_config sc JOIN chameleon.simulator_response sr ON sr.simulator_config_id = sc.id WHERE sc.api_name = 'GETKYCStatus';
```
---
Update (change Digilocker → EKYC; keep address text as-is):
---
```sql
UPDATE chameleon.simulator_response sr JOIN chameleon.simulator_config sc ON sc.id = sr.simulator_config_id SET sr.response = REPLACE(REPLACE(sr.response, '"kycType": "DIGILOCKER"', '"kycType": "EKYC"'), '"kycType":"DIGILOCKER"', '"kycType":"EKYC"') WHERE sc.api_name = 'GETKYCStatus' AND sr.response LIKE '%DIGILOCKER%';
```
---
```sql
SELECT sr.id, sr.response LIKE '%DIGILOCKER%' AS still_digilocker, sr.response LIKE '%"kycType": "EKYC"%' OR sr.response LIKE '%"kycType":"EKYC"%' AS now_ekyc FROM chameleon.simulator_response sr JOIN chameleon.simulator_config sc ON sc.id = sr.simulator_config_id WHERE sc.api_name = 'GETKYCStatus';
```
---
Blank Aadhaar address on Personal Details is caused by the **QA KYC status simulator**, not by the KYC engine product change.
---
KYC engine supports **eKYC and cKYC only** (Digilocker is out of scope). The simulator returns a completed KYC with address data, but marks the KYC type as **Digilocker**. Our flow therefore does not treat it as eKYC/cKYC address data, so name and gender are saved and shown, while address is not applied and stays blank on Personal Details.
---
Update the QA `GETKYCStatus` simulator stub so the KYC type is **EKYC** or **CKYC** (matching the journey), keep the address fields, restart the simulator service, then retest on a **new** application.


## asst snippet 4
Blank Aadhaar address on Personal Details is caused by the **QA KYC status simulator**, not by a KYC engine product defect.
---
**We do not support Digilocker** on the KYC engine path (supported modes are **eKYC** and **cKYC** only). The simulator returns completed KYC with address data, but sets KYC type as **Digilocker**. Because Digilocker is unsupported, address is not applied to the application - name and gender still show; address stays blank.
---
Fix the QA `GETKYCStatus` simulator stub: set KYC type to **EKYC** (or **CKYC**), keep address fields. Restart chameleon, then retest on a **new** application.
---
### Simulator update (chameleon DB on sim host)
---
Find:
`SELECT sc.id AS config_id, sc.api_name, sc.request_type, sr.id AS response_id, sr.validation, sr.response_code, sr.response LIKE '%DIGILOCKER%' AS has_digilocker, LEFT(sr.response, 400) AS response_head FROM chameleon.simulator_config sc JOIN chameleon.simulator_response sr ON sr.simulator_config_id = sc.id WHERE sc.api_name = 'GETKYCStatus';`
---
Update:
`UPDATE chameleon.simulator_response sr JOIN chameleon.simulator_config sc ON sc.id = sr.simulator_config_id SET sr.response = REPLACE(REPLACE(sr.response, '"kycType": "DIGILOCKER"', '"kycType": "EKYC"'), '"kycType":"DIGILOCKER"', '"kycType":"EKYC"') WHERE sc.api_name = 'GETKYCStatus' AND sr.response LIKE '%DIGILOCKER%';`
---
Confirm:
`SELECT sr.id, sr.response LIKE '%DIGILOCKER%' AS still_digilocker, (sr.response LIKE '%"kycType": "EKYC"%' OR sr.response LIKE '%"kycType":"EKYC"%') AS now_ekyc FROM chameleon.simulator_response sr JOIN chameleon.simulator_config sc ON sc.id = sr.simulator_config_id WHERE sc.api_name = 'GETKYCStatus';`


## asst snippet 5
**Queries were almost right - wrong schema name.** QA uses `novopay_simulator`, not `chameleon`.
---
| Field | Value |
| --- | --- |
| config_id | 529 |
| api_name | GETKYCStatus |
| request_type | JSON |
| response_id | 10023 |
| has_digilocker | **1** |
| snippet | `kycType": "DIGILOCKER"` (spaced form) |
---
```sql
SELECT sc.id AS config_id, sc.api_name, sc.request_type, sr.id AS response_id, sr.validation, sr.response_code, sr.response LIKE '%DIGILOCKER%' AS has_digilocker, LEFT(sr.response, 400) AS response_head FROM novopay_simulator.simulator_config sc JOIN novopay_simulator.simulator_response sr ON sr.simulator_config_id = sc.id WHERE sc.api_name = 'GETKYCStatus';
```
---
```sql
UPDATE novopay_simulator.simulator_response sr JOIN novopay_simulator.simulator_config sc ON sc.id = sr.simulator_config_id SET sr.response = REPLACE(sr.response, '"kycType": "DIGILOCKER"', '"kycType": "EKYC"') WHERE sc.api_name = 'GETKYCStatus' AND sr.id = 10023 AND sr.response LIKE '%DIGILOCKER%';
```
---
```sql
SELECT sr.id, sr.response LIKE '%DIGILOCKER%' AS still_digilocker, sr.response LIKE '%"kycType": "EKYC"%' AS now_ekyc FROM novopay_simulator.simulator_response sr WHERE sr.id = 10023;
```
---
Then restart chameleon on QA (`/apps/novopay-platform-simulator`) so the cached stub refreshes.
---
**TL;DR:** Use schema `novopay_simulator`; SELECT is confirmed; Digilocker stub is response id `10023`. Say if you want the UPDATE run.


## asst snippet 6
Blank Aadhaar address on Personal Details is caused by the **QA KYC status simulator**, not by a KYC engine product defect.
---
**We do not support Digilocker** on the KYC engine path (supported modes are **eKYC** and **cKYC** only). The simulator returns a completed KYC with address data, but sets KYC type as **Digilocker**. Because Digilocker is unsupported, address is not applied to the application - name and gender still show; address stays blank.
---
Checked on QA: DSA4871789653168, DSA4871789653372, DSA4871789654451 - same pattern. Simulator row confirmed: `GETKYCStatus` response id `10023` currently has Digilocker.
---
Update the QA `GETKYCStatus` simulator stub so KYC type is **EKYC** (or **CKYC**), keep address fields, restart the simulator service, then retest on a **new** application.
---
### Simulator SQL (QA DB schema `novopay_simulator`)
---
Find:
`SELECT sc.id AS config_id, sc.api_name, sc.request_type, sr.id AS response_id, sr.validation, sr.response_code, sr.response LIKE '%DIGILOCKER%' AS has_digilocker, LEFT(sr.response, 400) AS response_head FROM novopay_simulator.simulator_config sc JOIN novopay_simulator.simulator_response sr ON sr.simulator_config_id = sc.id WHERE sc.api_name = 'GETKYCStatus';`
---
Update:
`UPDATE novopay_simulator.simulator_response sr JOIN novopay_simulator.simulator_config sc ON sc.id = sr.simulator_config_id SET sr.response = REPLACE(sr.response, '"kycType": "DIGILOCKER"', '"kycType": "EKYC"') WHERE sc.api_name = 'GETKYCStatus' AND sr.id = 10023 AND sr.response LIKE '%DIGILOCKER%';`
---
Confirm:
`SELECT sr.id, sr.response LIKE '%DIGILOCKER%' AS still_digilocker, sr.response LIKE '%"kycType": "EKYC"%' AS now_ekyc FROM novopay_simulator.simulator_response sr WHERE sr.id = 10023;`


# 6d631b7d-e04b-430a-9228-2b994db9a3b7


## asst snippet 1
| S.No. | Check | Pass when |
| --- | --- | --- |
| `1` | New application has DS before KYC | After create, DS id is present before eKYC / cKYC starts |
| `2` | eKYC to KYC engine | Reference sent to bank is **DS…** (not DSA…) |
| `3` | cKYC to KYC engine | Reference sent to bank is **DS…** (not DSA…) |
| `4` | DSA journey still works | Resume, status, and agent/customer journey still use DSA as before |
| `5` | Document upload unchanged | DS still goes in `filler1`; bank application ref stays in `applicationRefNo` (do not put DS there) |
| `6` | Happy path | Full eKYC and cKYC success paths complete with no new failures |
---
### Do not retest as part of this story
---
| Id | Meaning | KYC engine (new) | Document upload |
| --- | --- | --- | --- |
| DS… | App tracking id | Use this | `filler1` |
| DSA… | Journey / app reference | Do not use here | Not sent |
| Bank ARN | Bank application id | Unchanged | `applicationRefNo` |
---
**TL;DR:** Confirm KYC engine gets DS (not DSA) for eKYC and cKYC; DSA journey and document upload stay unchanged.


## asst snippet 2
Found the DS→KYC-engine commit; checking the exact bank request field next.


## asst snippet 3
| Where to look | API | Key | Expected value |
| --- | --- | --- | --- |
| Bank KYC engine call (main proof) | Bank **KYC Initiate** (from banking-origination) | `externalRefNo` | Must be **DS…** (not DSA…) |
| Same call (sanity) | same | journey / lookup still DSA | DSA stays on our side; do not swap journey id |
---
| Hop | API | Key | Value |
| --- | --- | --- | --- |
| Agent / app | `initiateKycEngineForCCDSA` | `client_reference_code` | Still **DSA…** (unchanged) |
| CC → banking-origination | `kycInitiate` | `referenceNumber` | **DS…** |
| CC → banking-origination | `kycInitiate` | `clientReferenceNumber` | Still **DSA…** |
| Bank | KYC Initiate | `externalRefNo` | **DS…** ← this is the bank ask |
---
- Document upload `filler1` / `applicationRefNo` - out of scope  
- Poll / status APIs - they still look up by DSA (`clientReferenceNumber`)
---
**Bottom line:** On KYC Initiate to bank, verify `externalRefNo` is **DS…** for eKYC and cKYC.


## asst snippet 4
**No - for this story you do not need to retest filler1 as a new change.** The ticket mentions it only to say “leave it alone.”
---
### Two different “filler1”s (easy to mix up)
---
| Where | What `filler1` means | HDP-11579? |
| --- | --- | --- |
| Document upload to bank | Carries our **DS** tracking id | **No change** - already worked; only confirm it still does |
| KYC Engine **status/poll** response | Bank mobile match (`Y` / `N`) | **Unrelated** - not this ticket |
---
Bank already uses **DS** on document upload via `filler1` (same tracking idea). This story only aligns **KYC Initiate** so bank gets **DS** there too (as `externalRefNo`), not DSA.
---
- **Must check:** KYC Initiate → bank `externalRefNo` = **DS…** (eKYC + cKYC)
- **Optional smoke only:** document upload still has DS in `filler1`, and bank ARN still in `applicationRefNo` (regression, not a new mapping)
- **Do not check:** KYC status/poll `filler1` for this ticket
---
**Bottom line:** Filler1 in the ticket = document-upload regression note. The real verify key is still bank KYC Initiate `externalRefNo` = DS.


## asst snippet 5
I'll rewrite HDP-11579 so “do” vs “verify” is clear and filler1 isn’t mixed into the main change — then show the exact draft for your OK before updating Jira.


## asst snippet 6
Proposed rewrite for **[HDP-11579](https://novopay.atlassian.net/browse/HDP-11579)** (description only). Removes filler1 from the main path so QA is not confused.
---
### Summary (unchanged)
Send DS tracking id to KYC engine for eKYC / cKYC (bank request)
---
On DSA credit card **eKYC** and **cKYC**, send our **DS** tracking id to the bank KYC engine instead of the **DSA** journey id.
---
| Call | Field | Before | After |
| --- | --- | --- | --- |
| Bank KYC Initiate (eKYC and cKYC) | `externalRefNo` | DSA… | DS… |
---
| S.No. | Check | Pass when |
| --- | --- | --- |
| `1` | eKYC | Bank KYC Initiate has `externalRefNo` = DS… (not DSA…) |
| `2` | cKYC | Same as above |
| `3` | Journey continuity | Resume / status / agent flow still work with DSA |
| `4` | Happy path | eKYC and cKYC complete successfully |
---
## Out of scope (do not retest as this story)
---
- Document upload (`filler1`, `applicationRefNo`) - unchanged
- OTP / demog / dedupe / eligibility
- Changing or removing DSA generation
---
Attach one eKYC and one cKYC success proof showing bank KYC Initiate `externalRefNo` starts with **DS**.
