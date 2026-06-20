---
description: "Plan gate - ticket scope, repos, bob context (no code, no Bob validate)"
---

# Ticket kickoff (Plan gate)

User input after command: ticket id (required), optional title.

1. Run `bob context --ticket <id>` from novopay workspace (or read `docs/tdd-runs/<id>/CONTEXT_PACK.md`).
2. If folder missing, note `bob init-ticket <id> "title"`.
3. Output Plan checklist: scope, assumptions, impacted repos (CC/lib/gateway/actor), open questions.
4. Do NOT implement code or run `bob validate-ticket`.

One ticket per chat. Workspace root: Desktop/novopay.
