---
name: Submit addon corrupt fix and PR
overview: "Fix the corrupt submit response by aligning request &lt;data&gt; with the bank's 38-char format (root cause: we send 100 chars), provide a single corrected curl, verify code matches working XML, and update the PR description with tested scope, how tested, results, and notes."
todos: []
isProject: false
---

# Submit add-on corrupt response fix, code alignment, and PR description

## 1. Why submit response is corrupt and the fix

**Root cause:** The bank’s **working** BBIADN request uses a **38-character** `<data>` segment (e.g. `901049036 001eCSF 0001011920002182826` ). Our code (and Curl A in [BANK_ADDON_CARD_CURLS.md](novopay-platform-creditcard-management/BANK_ADDON_CARD_CURLS.md)) send **100-character** `<data>`. The bank likely parses by fixed length/positions; the extra 62 bytes cause misalignment, so they build a malformed response (request rec ends up inside response “data”, real HIBVADN rec missing/empty).

**Fix:**

- **Curl:** The **correct** submit curl is the one that matches the bank sample exactly: **38-char `<data>`**, **400-char `<rec>`** with `00400`, **single-line** inner XML inside CDATA, **ns1/ns2** namespaces. That is already in [BANK_ADDON_CARD_CURLS.md](novopay-platform-creditcard-management/BANK_ADDON_CARD_CURLS.md) as **“0. Bank official sample (BBIADN)”**. No change to that curl body is needed; it is the corrected reference. In the doc, make section 0 the **primary** “use this for submit” curl and state that Curl A (100-char data) can produce a corrupt response and is for reference only unless the bank accepts 100-char data.
- **Code (lib):** Default the request to the **38-char data** format so the app sends the same as the working XML. In [SubmitAddOnCardApplicationService.java](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationService.java), change the default of `hdfc.soap.addon.card.data.format` from `STANDARD` to `BANK_SAMPLE` so that by default we send 38-char data. Optionally keep `STANDARD` for backward compatibility and document that 100-char data may result in corrupt response until the bank confirms support.

**Corrected curl (reference):** Use the exact bank sample from [BANK_SAMPLES_ADDON_CARD.md](novopay-platform-creditcard-management/BANK_SAMPLES_ADDON_CARD.md) / section 0 of BANK_ADDON_CARD_CURLS.md (single-line, 38-char data, 400-char rec). No new curl needed; promote that one as the canonical submit curl and add one sentence: “If you see corrupt or empty response , ensure the request  is 38 chars (this curl); 100-char data can cause corrupt response.”

---

## 2. Code alignment with working XML

**Working XML (bank BBIADN request):**

- SOAP: `ns1:requestAddOnCard`, `ns2` for arg0, `arg0` + `arg1` with `requestXML` in CDATA.
- Inner emsg: one line; `<data>` = 38 chars (`transactingPartyCode` 9 +  `` + `001eCSF` +  `` + AAN 19 +  ``); `<rec>` = 400 chars, starts with `BBIADN`  and `00400`.

**Current code (lib):**

- [SubmitAddOnCardApplicationService](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationService.java): SOAP shape and ns1/ns2/CDATA are correct. `buildRecString` is aligned (BBIADN, 00400, 400 chars, AddonCardFields). `buildDataStringBankSample` produces 38 chars: `nineChar(9) + " " + "001eCSF" + " " + aanPadded(19) + " "` = 38 chars, matching the bank. `buildDataString` (100 chars) does not match the working sample.
- **Alignment fix:** Default `data.format` to `BANK_SAMPLE` so the payload matches the working XML. No change to rec-building logic. Optionally add a unit test that with `BANK_SAMPLE` the generated `<data>` length is 38 and layout matches `XXXXXXXXX 001eCSF YYYYYYYYYYYYYYYYYYY`  (9 + 1 + 7 + 1 + 19 + 1).

**Summary:** Code is aligned with working XML **when** 38-char data is used (`BANK_SAMPLE`). Making that the default completes alignment.

---

## 3. PR description – what to add

Update [PR_DESCRIPTION_ADDON_SUBMIT.md](novopay-platform-creditcard-management/PR_DESCRIPTION_ADDON_SUBMIT.md) so the PR clearly states what was tested, how, results, and notes.

**Add or adjust:**


| Section             | What to add                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **What was tested** | Submit with **38-char data** (bank sample format) vs **100-char data**; **direct curl** using bank sample body (section 0) vs Curl A (100-char data); that **code** sends 38-char data when `hdfc.soap.addon.card.data.format=BANK_SAMPLE` (or by default after fix).                                                                                                                |
| **How tested**      | (1) Direct curl to bank with exact BBIADN sample body (38-char data, 400-char rec) from BANK_ADDON_CARD_CURLS.md section 0. (2) App submit with tenant + seeded data, with config set so lib uses 38-char data; optionally with 100-char data to reproduce corrupt response.                                                                                                         |
| **Results**         | With **38-char data** (corrected curl / BANK_SAMPLE): bank returns **clean response** with `<rec>` = HIBVADN 00200... (200 chars). With **100-char data**: bank returns **corrupt** response (request rec in wrong place, empty/useless rec). Root cause: **data segment length** (38 vs 100).                                                                                       |
| **Notes**           | **Corrected submit curl:** Use section 0 (bank sample) in BANK_ADDON_CARD_CURLS.md; 38-char data required for non-corrupt response. **Code:** Default or config to 38-char data (`BANK_SAMPLE`) so request matches working XML. **Lib:** `SubmitAddOnCardApplicationService` default `hdfc.soap.addon.card.data.format=BANK_SAMPLE`; STANDARD (100-char) kept only if bank confirms. |


Keep existing items (tenant NPE fix, transaction audit LIMIT 1, seed, docs, checklist) and add the above so the PR is self-contained: cause, fix, how to test, and expected results.

---

## Implementation summary


| #   | Task                                                                                                                                                                                                                    | Where                                                                                                                                                                                             |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Set default `hdfc.soap.addon.card.data.format` to `BANK_SAMPLE` so submit uses 38-char data by default                                                                                                                  | Lib: [SubmitAddOnCardApplicationService.java](novopay-platform-lib/infra-transaction-hdfc/src/main/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationService.java)         |
| 2   | In BANK_ADDON_CARD_CURLS.md: state section 0 is the **correct submit curl**; add one line that 100-char data (Curl A) can cause corrupt response                                                                        | [BANK_ADDON_CARD_CURLS.md](novopay-platform-creditcard-management/BANK_ADDON_CARD_CURLS.md)                                                                                                       |
| 3   | Update PR description: add tested scope (38 vs 100-char data, curl vs app), how tested (curl + app with config), results (38-char = clean rec, 100-char = corrupt), notes (corrected curl = section 0, default 38-char) | [PR_DESCRIPTION_ADDON_SUBMIT.md](novopay-platform-creditcard-management/PR_DESCRIPTION_ADDON_SUBMIT.md)                                                                                           |
| 4   | (Optional) Unit test: with BANK_SAMPLE, assert `<data>` length 38 and pattern matches bank layout                                                                                                                       | Lib: [SubmitAddOnCardApplicationServiceTest.java](novopay-platform-lib/infra-transaction-hdfc/src/test/java/in/novopay/infra/hdfc/api/loanoncard/util/SubmitAddOnCardApplicationServiceTest.java) |


No new curl body is required; the corrected curl is the existing bank sample (section 0). Code alignment is achieved by defaulting to 38-char data.