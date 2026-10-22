# 03 - Landmines

Symptom, wrong fix, real fix. Code how-it-works is in the linked resume / AGENTS.md.

Written-in-AGENTS.md traps (visit owner, SHA-256 checksum, merge-tree --name-only, move_agent_to_root, TaskAlloc V000021, preprod=`ddp-prod`): **read AGENTS.md**. Do not copy them here.

---

### DIY same-second client ref looks like "wrong DSE on the card"

- **Symptom:** Bank sees Ajith / Valueleaf on Praveen's application. Snapshot mixed (`dse_id` vs owner).
- **Wrong fix:** Unique-index on generated code; rewrite login store; SQL `dse_id <> assistor_id` (that is ~20k **legitimate** owner-moved rows).
- **Real cause:** Unassisted DIY ref was `DSA` + epoch **seconds** with empty userId. Two starts in the same second share a ref; CC reuses the case with no owner check and stitches the second agent's fields. Since DIY ~27-28 Apr 2026, not a later regression.
- **Fingerprint:** snapshot `dse_code` <> `corporate.code` of snapshot `dse_id`. Prod = **5 rows / 2 ARNs**, not 20k.
- **Hidden constraint:** `dsa_banking_origination.kyc_detail.client_reference_number` is VARCHAR(20). A 28-char DIY ref would break DIY KYC. Server ref is 19 chars.
- **Wrong follow-up:** FE change. DIY page already stores the API's returned ref.
- **Still open:** bank remap 2 ARNs; close 3 in-flight; leaked HDFC token on the Jira attachment (rotate). Fix on QA, **not** UAT/prod as of 15 Oct.
- **Ref:** [DPB-2148](https://novopay.atlassian.net/browse/DPB-2148) `docs/tdd-runs/DPB-2148/TICKET_RESUME.md`

### "Only N records per agent" / auto-assign "broken"

- **Wrong ticket:** [HDP-11075](https://novopay.atlassian.net/browse/HDP-11075) - system was on spec.
- **Real:** Auto cap counts **non-terminal** tasks. `KYC_FAILED`, `REASSIGNMENT_REQUESTED`, `CUSTOMER_UNREACHABLE`, `CALLBACK_REQUESTED`, `APPOINTMENT_RESCHEDULED` never free a slot. Agent APK **Closed** tab is wire `DONE`. A failed KYC sits on Closed and still holds the cap.
- **Test-file trap:** Invented pincodes (`999999`) never match an office pin, so leads never auto-assign and never show in ADM2. QA Manipal corp `10` already has a backlog of unmatchable pins. Use only the QA pins in `pref-qa-bkyc-file-pincodes` memory. Spread tests need a **shared** pin (RISL `560103` is the only one with 3 agents).
- **Cap drift:** QA was 10/15; on 2026-09-09 `QA_SETUP` set auto **20** / manual **30**. Docs that still say 10 are stale.
- **Prove:** count open non-terminal by `agent_id`, not "is there an agent on this pincode".
- **Ref:** [HDP-11241](https://novopay.atlassian.net/browse/HDP-11241) comment 403349

### Bank UAT is not trustt UAT

- ddp UAT host `172.31.2.22` is readable. **Bank UAT is not.** Build files only from SELECT output Ashutosh pastes.
- `CORP0007` on bank UAT = Motwanihero **625**. Same code on ddp UAT = Pavan Solutions **43606**. Mixing ids silently entitles the wrong company.
- Bank UAT: corp-2 users can upload but cannot assign; corp-625 users can assign but cannot upload. Role `QA_BKYC_TASK` (337) is the only one with `PRDCT-TASKREQUEST-BKYC` there.

### Encrypted PAN in an API response is often not a code bug

- [HDP-12874](https://novopay.atlassian.net/browse/HDP-12874): UAT `agentLeadSignUp` returned hex PAN. Code identical on qa/uat/prod. `platform_master.decrypt` returns the **input** on wrong key / missing function - no Java error.
- UAT flipped 2026-10-14 10:42. Function recreated by hand 2026-10-15 12:46 by `rprabhakar@%`. Rows encrypted **before** that stay undecryptable; newer rows are fine. QA unaffected.
- Diagnose by PAN **shape** in actor response logs (masked `XXXXX9999A` vs 32-hex). Do not SELECT the key table.
- **Ref:** `docs/tdd-runs/HDP-12874/TICKET_RESUME.md`

### Resume Demog `50003` / `IPA0=N` overwrites ETB to NTB

- Parsed as NTB `4000185`, `postReal` wrote `NEW`. CIF at Final DAP did not come from that Demog body.
- **Rule:** IPA0=N is NTB only for D101/D106. `50003` stays `50003`; keep `EXISTING`.
- **Ref:** [HDP-12387](https://novopay.atlassian.net/browse/HDP-12387)

### HDFC Salesforce JSON: null becomes `""`

- `CustomObjectMapper` serializes null as empty string. To **drop** a tag, `@JsonInclude(NON_NULL)` and leave null. HDP-12000 HDIM/JSC uses a config switch.
- `ExecuteFinalDAPSalesforceServiceTest` T4 already fails on clean `ddp-prod` (pre-existing).

### Map pin / MMI fail-open

- Only NULL lat/long get geocoded. UAT often has **no** `hdfc.map.my.india.*` TaskAlloc config. gRPC config miss + `LoggingClientInterceptor` `MDC.clear()` -> tenant null -> `redisTemplatenull` -> fail open to a wrong city (Udupi for pin 580001).
- Check `/apps/applogs/common/` as well as tenant logs.
- Thin deploys omit MMI templates under `templates/bankIntegration*`.
- **Ref:** [HDP-11732](https://novopay.atlassian.net/browse/HDP-11732), [HDP-11477](https://novopay.atlassian.net/browse/HDP-11477)

### New `service_master` row, batch calls `http://[{endpoint=...`

- `ServiceRegistry` cache-miss does `resultList.toString()`. Restart **batch** after registering a new service. Fixed only on `ddp-bkup-uat`, still on `ddp-prod`.

### Partner API 401 after a "successful" deploy

- [HDP-8768](https://novopay.atlassian.net/browse/HDP-8768): Flyway + CC jar on QA, 13/13 direct CC pass. Gateway 401 `10017` because **box** `application.properties` skip-list was not updated. Not in git.

### Report dropdown shows CC Report instead of Agent Lead

- [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) On Hold. Pre-prod `dsa_masterdata` has **three active duplicate** `CC_REPORT` rows (9450, 9451, 9452). Data, not code. Reopened once.

### CC0005 "same network"

- [HDP-6421](https://novopay.atlassian.net/browse/HDP-6421): stale / wrong **agent** IP on gateway-fronted calls vs customer IP.

### Download report "wrong" for old BKYC files

- [HDP-11733](https://novopay.atlassian.net/browse/HDP-11733): report is built **at upload time**. Pre-fix files stay wrong. Expected.

### BKYC menu missing after entitlement hide

- [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743): corporate users of non-entitled corps. **FE** change, not another BE hide.

### Add-on CASE-NBR blank

- [HDP-12325](https://novopay.atlassian.net/browse/HDP-12325) (Gowtham): blank CASE-NBR is missing **cust id** on the add-on lead, not mobile. Comment 414992.

### LOC HIBVPRD account empty

- Spec workbook is only on Ashutosh's Downloads (`LOC APIs mapping v 0.1 (2).xlsx`) - **not in git**. MEMO-LINE5 last 14 chars are the account; bank UAT fills a CASA / `MEMOLINE05` prefix. Dropping the product because the whole field looks non-blank is wrong.
- **Ref:** [HDP-8565](https://novopay.atlassian.net/browse/HDP-8565)

### Masters-mgmt port of CC Excel JAR

- `CompanyMasterService` today **deletes and re-inserts** (ids change). JAR **upserts in place**. Port must update in place.
- masters-mgmt has **no `ddp-prod`**. SoT is `origin/ddp-qa` (last product commit Jan 2025 until onboarding PRs).
- **Ref:** [HDP-12841](https://novopay.atlassian.net/browse/HDP-12841)
