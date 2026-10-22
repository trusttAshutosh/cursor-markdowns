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

### Jira / GitHub write goes out as Deepankar

- Atlassian MCP (and Chrome "Browser 1") is signed in as **Deepankar Sarkar**. A description edit on [HDP-11225](https://novopay.atlassian.net/browse/HDP-11225) already landed under his name. Cannot undo audit history.
- **Never** use Atlassian MCP for writes. Draft in Markdown; Ashutosh pastes from his Jira login. Confirm `gh api user` / git identity before any GitHub write.

### Approve corporate fails 12001 "Duplicate request found"

- Looks like UI double-click. It is nested `storeClientCodeAndClientKey` reusing parent `approveApplication` STAN. `generateNewStan=true` in XML does **not** mint a new STAN if the parent already has one (since 22 Apr 2026).
- Duplicate-check is STAN-global, not per API. Child may not even insert an RRL row.
- `X-Forwarded-For NOT FOUND` in the same log is noise.
- **Ref:** [DPB-2145](https://novopay.atlassian.net/browse/DPB-2145) (Closed; Hareesha). RCA `https://mdshare.trustt.com/md/s/Nj8z0Wjehd9p`

### Aadhaar-mobile timeout sent to bank as "not linked"

- Check failure (timeout / India-stack) is stored as N and the step still succeeds. Bank / VKYC FILLER4 treats non-Y as mismatch. In prod code since 7 May 2026.
- Correct error 4000178 already exists; CC swallows it.
- Not [HDP-7629](https://novopay.atlassian.net/browse/HDP-7629) / [HDP-7708](https://novopay.atlassian.net/browse/HDP-7708).
- **Ref:** [HDP-12870](https://novopay.atlassian.net/browse/HDP-12870)

### `getKycStatus` "Query did not return a unique result"

- `kyc_detail.client_reference_number` has **no unique key**. Two initiates at once both insert. Every later poll fails forever.
- Race since Sep 2025 BO code; became visible when KYC Engine routed CC through BO ([HDP-7350](https://novopay.atlassian.net/browse/HDP-7350)).
- Unique key is a **follow-up**, not this ticket. Prod PR [BO #5396](https://github.com/trusttai/trustt-platform-banking-origination/pull/5396) still open.
- **Ref:** [HDP-12080](https://novopay.atlassian.net/browse/HDP-12080)

### BKYC upload list stuck PROCESSING / download PENDING

- Ingest finished; UI listed **before** counts were written (no later list call). Download used original `storedFileName` (`...000`) not `responseDocumentCode` (`...002`).
- Preprod BANKMAKER user **19**, corporate 76 CSC. Open, unassigned.
- **Ref:** [HDP-12140](https://novopay.atlassian.net/browse/HDP-12140)

### BKYC QA upload missing `x-run-mode`

- Training [HDP-11081](https://novopay.atlassian.net/browse/HDP-11081) (7 Oct) narrowed admin-portal interceptor from `v2/` to `/api/novopay/v2/`. Document path `/document/novopay/v2/TASK-ALLOCATION/uploadTaskLeadFile` is skipped. List APIs on the same page still work.
- QA-only until Training is promoted. Gateway/TaskAlloc are fine. Fix is webapp interceptor. Uncommitted `.wt-webapp-hdp-12386`.
- **Ref:** [HDP-12386](https://novopay.atlassian.net/browse/HDP-12386)

### Assign SMS never sends on QA (13007)

- `NotificationsSmsClient` posted a flat body to Notifications v1 which requires `{request, headers}`. Every flush `sent=0`; backlog retried on each upload.
- Quiet hours are **config**, not the clock (`...sms.assign.window.start/end`). Narrowing the window holds SMS for the **whole tenant**.
- **Ref:** deferred PACK-114 in `proj-hdp-7636-deferred-qa-tests`

### Name-match "outage" test needs writes + a trap

- TASK-ALLOCATION has **no** `hdfc.soa.name.match.service.url` row, so it hits live HDFC UAT. BO/Actor already point at the QA simulator, whose canned response is **always 100%** - once TaskAlloc points there, mismatch cases die.
- Redis flush: `sudo -u tomcat`, not the normal SSH user (`Connection refused` on 6379).
- **Ref:** T17 same memory file

### UAT eKYC "Invalid OTP value" after generate succeeds

- Code matches preprod. Likely gen vs val URLs on different backends, or real UIDAI OTP vs "test OTP" on simulator.
- **Ref:** [HDP-11970](https://novopay.atlassian.net/browse/HDP-11970)

### BKYC prod Flyway rename will fail validate

- Gateway product `V4000032` -> `V4000046` rename: prod already applied `V4000032` and has no `ddp/V4000032`. Rename re-runs CREATE INDEX / breaks validate. Draft [PROD] pack step 6 PR #2500.
- ddp-prod is Jackson 3; BKYC branch `com.fasterxml.jackson.databind` imports fail after merge.

### Gateway common-scripts commit hook

- api-gateway pre-commit refuses commits when behind `ddp-prod-master`. `ddp-fea-common-scripts` has not tracked it since June 2026. Skip is `NOVOPAY_GIT_HOOK_SKIP_PROD_SYNC=1` **per commit**, with approval. Untracked `git-hooks/*.sh` also block `git switch`.

### Gradle/rm hang on this laptop is Seqrite

- ATSLAP-43 Seqrite EPS minifilter. Thread stuck in `DeleteFile0`; no handle to kill. Do not retry Gradle/Java/Git. RCA `docs/RCA_WINDOWS_FILE_HANG_SEQRITE_2026-09-02.md`.

### Claude artifact pin does not follow republish

- Viewers stay on the old pin until he moves it. Versions cannot be listed or deleted. BKYC run-sheet artifact URL is in `ref-artifact-sharing`.
