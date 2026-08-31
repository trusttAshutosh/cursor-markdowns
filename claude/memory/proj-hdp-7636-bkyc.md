---
name: proj-hdp-7636-bkyc
description: HDP-7636 Manipal BKYC — locked consent identity/status/OTP decisions and Jira ticket-split conventions
metadata: 
  node_type: memory
  type: project
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:33:31.817Z
---

**HDP-7636** ([epic](https://novopay.atlassian.net/browse/HDP-7636)) — Manipal BKYC, the **first
`task_type`** under the task-allocation platform ([[proj-task-allocation]]). Product story
[HDP-7637](https://novopay.atlassian.net/browse/HDP-7637) (BKYC Agent Flow). Docs:
`docs/hdp-7636/solution-document.md`, `development-plan.md`, `gap-analysis.md`, `source/`. Assisted-only;
unassisted full KYC out of scope; bio reuses existing **india-stack** (no new KYC bio microservice);
Phase-1 SFTP, Phase-2 SF API. All new BKYC APIs are **v2 only**. (Current as of 2026-08.)

**Consent identity (locked):** use existing **`consent_code`** (`consent_audit`) — never invent
`consent_session_id`. Deep link `?consentCode=`. Gate bio **only when `consent_status = AGREED`** (not
on SUCCESS/FAILED). Consent TTL 30 min, configurable ([HDP-9249]).
**Consent statuses:** `PENDING | AGREED | DISAGREED | ERROR | EXPIRED | INPROGRESS`.

**OTP (locked):** existing **`submitOtpConsent`** with `function_sub_code = INITIATE | CONFIRM` (+ `otp`
on CONFIRM). INITIATE = generate/resend OTP SMS; CONFIRM success → `AGREED`. Do **not** invent
`action=GENERATE/VALIDATE`.

**Masters (locked):** keep `bkyc_lead_status_master` for journey statuses. Decline reasons (6 UD codes)
go in masterdata **`code_master` / `code_master_details`** with `data_type = BKYC_DECLINE_REASON` —
**do not** create `bkyc_decline_reason_master`.

**Ownership & Jira split (locked):**
| Layer | Owner | Ticket family | Repos |
|---|---|---|---|
| Consents APIs + KYC glue + journey SMS | **Java** | `ST-BE-39…44` (incl. HDP-9060=BE-42 create page-data, HDP-9061=BE-43 OTP, HDP-9062=BE-44 disagree) | `novopay-platform-consents`, `novopay-platform-kyc-management`, notifications |
| Consent web UI (CUS) | **React** | `ST-CNS-01…06` | Consent web app |
- Summaries `Java — …` / `React — …`; labels java/backend vs react/frontend.
- React and any client Sub-task (Android/Admin/Consent FE) that calls a BKYC API still carries the full
  `Field | Type | Required | Sample | Notes` table + samples — FE doesn't implement Java. See
  [[pref-jira-tickets]].
- Clarifications: create with **parent/Epic Link = HDP-7636** (Clarification is same level as Story), and
  always **Relates**-link to HDP-7637. Never set parent = HDP-7637 (API rejects — wrong hierarchy).

**SQL/Flyway/audit (locked):** SQL examples MySQL only; nest under "Implementation steps";
`change_source`/audit strings = real job/API names (e.g. `sendCustomerConsent`, `runBkycInboundIngestJob`)
- not placeholders. TaskAlloc DDL/seeds only in initial-setup `flyway/sql/task-allocation/product/`
(not the TaskAlloc service repo). New Flyway versions per [[ref-flyway-infra-versioning]].

**Jira body SoT (local):** `docs/hdp-7636/jira-subtask-bodies.json` (canonical),
`docs/hdp-7636/_mcp_payloads/<KEY>.json` (push payloads), generators `_gen-*.mjs` / `_api-contracts.mjs`
/ `_enrich-*.mjs` (regenerate then enrich before push; avoid bare `|` in Jira table cells).

Do not invent fields, statuses, tables, or ticket shapes that contradict the above — prefer existing
platform contracts. Related: [[proj-task-allocation]], [[pref-jira-tickets]], [[pref-git-workflow]].
