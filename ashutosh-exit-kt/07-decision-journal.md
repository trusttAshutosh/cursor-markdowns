# 07 - Decision journal

Why + what he refused. Implementation is in git.

| Decision | Why | Rejected / do not do |
| --- | --- | --- |
| BKYC entitled list by **corporate code** | Bank ops see codes in admin portal, not Actor ids | Id-only config (forces a developer lookup each onboard). Thermo-nuclear said delete legacy id/label fallback - **kept** for env compat |
| Actor `getCorporatesByCodes` internal v2, not on public gateway | TaskAlloc-only lookup | Gateway change |
| Fail closed if Actor down or codes set + old Actor | Empty entitled list + error log, no cache of failure | Fail open to "all corporates" |
| Auto cap counts non-terminal including `KYC_FAILED` | Status master `is_terminal=0` is the spec | Treat APK Closed as "slot free" ([HDP-11075](https://novopay.atlassian.net/browse/HDP-11075) was invalid) |
| Pin match = office `address.pincode` | No agent-pincode column | Agent home pin |
| Visit owner = field-agent `corporate.id` | What Assign stores | `user.id` / `actor.id` / office id (seed comments lie) |
| Bank EMPL default: UPLOAD / UPLOAD-VIEW / REPORT-VIEW only | Flyway never seeds VIEW/ASSIGN to bank | Treat QA bank-maker VIEW/ASSIGN as catalog ([HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) is drift) |
| DIY: server issues 19-char ref; ignore request ref | Same-second collision; KYC column VARCHAR(20) | FE uniqueness; 28-char actorId ref; uniqueness index on generated code |
| DIY owner check: reject CREATE on someone else's ref; snapshot mismatch **keeps** snapshot (no throw) | Legacy reassign / bulk ingest must not 400 | Fail the update on mixed snapshot |
| DPB-2148: no FE PR | DIY page already uses returned `client_reference_code` | agent-webapp change |
| [HDP-8768](https://novopay.atlassian.net/browse/HDP-8768): pull API, same auth as txn details, off `ddp-prod` | Bank UAT 15 Oct; Rohit HDP-10810 is QA-only and misses EKYC_OTP_CONFIRM | Webhook; wait on 10810 |
| [HDP-12387](https://novopay.atlassian.net/browse/HDP-12387): `50003` stays `50003`; IPA0=N is NTB only D101/D106 | Resume Demog was demoting ETB | Treat all IPA0=N as NTB |
| HDIM/JSC Final DAP behind a switch, default off | Bank payload toggle without code | Always send or always drop |
| Salesforce: `@JsonInclude(NON_NULL)` to omit a tag | Mapper writes null as `""` | Set field null and expect the key gone |
| HDP-12027: drop corp_id 1/2 filter; drop user 19/20; exclude DSE_Agent + LOCANDCC; leave ONLYLOC | Prod role dump; id 20 is a real bank-UAT employee | Copy QA dummy excludes to prod |
| HDP-12841: `fileName` is a **server disk path**; company loader **update in place**; masters-mgmt SoT `ddp-qa` | JAR upsert vs current delete-reinsert; no masters-mgmt `ddp-prod` | Multipart upload in this ticket; `java -jar` on box |
| Bank KYC evidence = real applogs | Sample XML misleads the bank | Invented payloads |
| Continual Learning stop-hook off | It rewrote AGENTS.md unasked | Auto-mine every chat |
| `bob validate-ticket` explicit only | Boot cost | Auto after every edit |
| Feature branches `ddp-fea-*` only | GitHub rejects other names | `ddp-fix-*` |
| Common-scripts Flyway before feature | Version collisions (HDP-8967) | Author Flyway on feature branch |
| TaskAlloc DDL only in initial-setup | Boot `flyway_auto_update=0` | Bring back JAR migrations |
| BKYC Chat weekday post stopped | User request 2026-08-24 | Post to prod BKYC channel |
| BKYC consent = existing `consent_code`; bio only if AGREED | Locked with Deepankar | `consent_session_id`; gate on SUCCESS |
| OTP = `submitOtpConsent` INITIATE/CONFIRM | Locked | GENERATE/VALIDATE |
| Decline reasons in `code_master` `BKYC_DECLINE_REASON` | Locked | New `bkyc_decline_reason_master` |
| Failed Aadhaar-mobile check fails the step | Do not tell the bank "not linked" | Swallow 4000178 and store N |
| Concurrent KYC: claim row before bank call | At most one initiate wins | Unique key first (that is a later cleanup) |
| Firestore: consents flag default on, actor default off | Soak actor | New error code; break 6-arg lib overloads |
| Add-on submit: Novopay not Net-banking | [HDP-12325](https://novopay.atlassian.net/browse/HDP-12325); DPB-2154 Not An Issue | Re-open DPB-2154 |
| Never write Jira via Atlassian MCP | It is Deepankar | "The connector is logged in, so it is fine" |
