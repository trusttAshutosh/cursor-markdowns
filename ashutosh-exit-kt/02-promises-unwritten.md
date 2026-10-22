# 02 - Promises / spec vs reality

Ticket text is not always what was agreed. AI will implement the ticket.

| When | Who | What was actually agreed | Must not do | Written? |
| --- | --- | --- | --- | --- |
| 2026-10-07 | Ashutosh (ops need) | Enable BKYC for a corporate by **admin-portal code** (e.g. `CORP0007`), not Actor id. Bank ops cannot see ids. | Keep asking ops for numeric ids as the only way | Code + config key exist; why is here. [HDP-12336](https://novopay.atlassian.net/browse/HDP-12336) |
| 2026-09-16 | Bank UAT | Only one entitled corporate: **`CORP0007` = id `625` Motwanihero**. ddp UAT `CORP0007` is a **different** company (Pavan Solutions 43606) - never reuse those ids | Copy QA/ddp-UAT agent ids or pincodes into bank UAT files | Not in product docs. Discovery SQL: `qa-bkyc-lead-files/BKYC-NEW-ENV-DISCOVERY.sql` |
| 2026-10-14 | Ashutosh + product | [HDP-8768](https://novopay.atlassian.net/browse/HDP-8768) Blostem status API is **pull**, not webhook. Auth same as `getCreditCardTransactionDetails`. Independent of Rohit's [HDP-10810](https://novopay.atlassian.net/browse/HDP-10810) (QA-only, ekyc read misses EKYC_OTP_CONFIRM) | Wait on HDP-10810; invent a push | Draft mapping comment still awaiting **bank product sign-off** |
| 2026-10-09 | Product on [HDP-12027](https://novopay.atlassian.net/browse/HDP-12027) | Exclude profiles `DSE_Agent` and `LOCANDCC` from UAM reports. **`ONLYLOC` is not excluded** unless product asks | Silently drop ONLYLOC | Comment [413312](https://novopay.atlassian.net/browse/HDP-12027?focusedCommentId=413312). SQL is not in git |
| 2026-10-05 | Ashutosh on HDP-12027 | Drop `u.id NOT IN (19,20)` - bank UAT user 20 is a real employee | Copy the QA exclude onto prod | Same ticket |
| 2026-10-12 | Ashutosh to FE (Manohar, Ranesh) | DIY server-issued client ref: **no FE change**. DIY page already uses the returned `client_reference_code` | Open an agent-webapp PR for DPB-2148 | [DPB-2148](https://novopay.atlassian.net/browse/DPB-2148) comment 414213 |
| 2026-08-24 | Ashutosh | BKYC weekday Google Chat posts **stopped on purpose** | Resume into the prod BKYC channel | `bkyc-tracker-schedule.json` `gchat_enabled` false |
| 2026-10-06 | Ashutosh on [HDP-10501](https://novopay.atlassian.net/browse/HDP-10501) | Bank rejected BKYC lead-closure document - clarification asked of Abhishek; empty/config-driven Salesforce payload | Assume bank wants a full payload because "upload" | Abhishek's ticket; get his KT |
| ongoing | Bank-facing KYC | Evidence packs use **real env applogs**. No sample XML, no internal class names | Invent payloads for the bank | `AGENTS.md` KYC Engine note |
| ongoing | Jira FE asks | Describe UI behaviour only. No file names, constants, branches | "change is already prepared" | `.cursor/rules/jira-comment-format.mdc` |
| 2026-08 | Product / Deepankar on BKYC consent | Identity is existing `consent_code`. Gate bio only on `AGREED`. OTP is `submitOtpConsent` INITIATE/CONFIRM. Decline reasons live in `code_master` `BKYC_DECLINE_REASON` | Invent `consent_session_id`, GENERATE/VALIDATE, or a new decline table | Claude memory `proj-hdp-7636-bkyc` |
| 2026-10-12 | Bank vs tickets | [DPB-2154](https://novopay.atlassian.net/browse/DPB-2154) (Net-banking / Wallet on add-on submit) closed **Not An Issue**. Real work is [HDP-12325](https://novopay.atlassian.net/browse/HDP-12325) pass **Novopay** instead of Net-banking | Re-open DPB-2154 as the spec | Two tickets; Gowtham owns 12325 |
| 2026-09-28 | Ashutosh on Firestore | Consents hardening flag default **on**; actor geo flag default **off**; no new wire error code (keep 13014); lib 6-arg overloads stay legacy | Turn actor flag on without soak; change error code | [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) |
| 2026-10-22 | Ashutosh (needs approval) | Failed Aadhaar-mobile check must **fail the step** (4000178), not store N | Leave journey continuing with N | [HDP-12870](https://novopay.atlassian.net/browse/HDP-12870) Open, unassigned |

Add rows when a verbal agreement contradicts the ticket. Do not invent.
