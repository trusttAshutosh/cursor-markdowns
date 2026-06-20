---
description: "Prod RCA - grep-only log command pack (never rg)"
---

# RCA log pack

User may explain the issue in **normal chat** after `/rca-logs` - ticket id, symptom, mobile, STAN, client_ref, api name, error code, date/time, service. **Extract** what you can from their message; do not make them fill a form.

**Only ask** for fields still missing to build useful greps (usually: service + date + at least one correlation id).

Rules:
- **grep only** (never rg) for `/apps/applogs/dsa/*-dsa.log*` and `/apps/applogs/common/*-common.log*`.
- Include rotated logs (`*.log*`).
- Blocks: txn correlation, request-out, response-in, crash/error, plus live `tail -F` with `grep --line-buffered`.
- Return JSON: status, command_pack, evidence_checklist (6 items), next_action.
- Tie commands to the issue they described (1-line recap at top).

If too little to grep (no date and no correlation id), return NEEDS_INPUT with **only** the missing fields listed - not a full template.

Do not run Bob validate-ticket. Do not open Glass automations.

**Example user message (valid):**
`/rca-logs PE-5678 customer 9876543210 failed submit LOC yesterday around 3pm on cc-mgmt`

**Example without slash (also valid):** user says "grep logs for mobile ..." - same behavior.
