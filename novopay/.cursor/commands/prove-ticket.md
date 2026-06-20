---
description: "Prove gate - Bob E2E validate-ticket (only when user explicitly asks to test)"
---

# Prove ticket (Prove gate)

User input after command: ticket id (required).

Run `bob validate-ticket <id>` with autoboot from novopay workspace. Summarize `docs/tdd-runs/<id>/GATE_SUMMARY.md` and `REPORT.md` (5 lines max).

Do not commit or push unless user asks in the same message.

This is the **only** Bob command the user needs for day-to-day proof. Do not suggest other Bob CLI commands unless blocked.
