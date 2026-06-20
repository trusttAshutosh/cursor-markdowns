---
name: novopay-cursor-automations
description: Deprecated - use slash commands in novopay/.cursor/commands/ instead (/ticket-kickoff, /prove-ticket, /pre-ship, /rca-logs).
disable-model-invocation: true
---

# Deprecated

Use **`/` commands** instead (see `novopay/.cursor/WORKFLOWS.md`):

| Command | Replaces |
|---------|----------|
| `/ticket-kickoff` | Ticket Kickoff |
| `/prove-ticket` | Proof / Bob validate |
| `/pre-ship` | Pre-Ship Evidence Pack |
| `/rca-logs` | RCA Log Pack Runner |

Do not open Glass Automations for these unless the user explicitly wants webhooks.
