---
description: "Prod RCA - grep-only log command pack (never rg)"
---

# RCA log pack

User input after command: service (cc-mgmt|actor|gateway|all), date, from_time, optional mobile/stan/client_ref.

Rules:
- **grep only** (never rg) for `/apps/applogs/dsa/*-dsa.log*` and `/apps/applogs/common/*-common.log*`.
- Include rotated logs (`*.log*`).
- Blocks: txn correlation, request-out, response-in, crash/error, plus `tail -F` with `grep --line-buffered`.
- Return JSON: status, command_pack, evidence_checklist (6 items), next_action.

If inputs missing, return NEEDS_INPUT with template variables only. Do not run Bob validate-ticket.
