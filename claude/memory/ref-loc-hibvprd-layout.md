---
name: ref-loc-hibvprd-layout
description: HDFC LOC product-eligibility (HIBVPRD) fixed-width layout source and how code offsets map to it; MEMO-LINE5 = savings account
metadata:
  type: reference
---

Bank spec for the LOC APIs is the workbook `C:\Users\ashutosh.kumar\Downloads\LOC APIs mapping v 0.1 (2).xlsx`
(sheets: Product_eligibility, Insta Loan, Jumbo Loan, card_summary, Account_Info). Not in any repo.

Product_eligibility response: 242-char fixed header, then `HIBVPRD-REC` blocks of 860 chars from absolute
position 243 (1-based). Code (`ProductEligibilityService.extractLoanProductDetails`, lib
`infra-transaction-hdfc`) uses 0-based block-relative offsets = spec start - 243:
PRO-CODE 0-3, PROD-DESC 8-48, MAX-ELIG-AMT 66-83, ELIGIBLE 84, MEMO-LINE1 85-125 (processing fee),
MEMO-LINE2 125-165 (PE-PQ dummy-jumbo marker), MEMO-LINE5 245-285 = **savings account number** per spec,
DETAILS x5 from 285 (115 each: PERIOD 0-3, INTEREST 3-8, TID 9-18).

Code reads the account only from the last 14 chars of MEMO-LINE5 (271-285, commit 2226a8c72e 2025-09-18)
and drops any product whose slice is blank (324ada6cc4). Bank UAT fills the first 26 chars with prefix text
("CASA", or the literal placeholder "MEMOLINE05") and the account right-aligned. Context: HDP-8565.
Decode helper: `python decode.py rec.txt` pattern lives in this memory's session notes; rebuild if needed.
Related: [[pref-git-workflow]], [[proj-novopay-overview]].
