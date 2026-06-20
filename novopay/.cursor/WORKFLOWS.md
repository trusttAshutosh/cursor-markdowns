# Novopay workflows

**Type `/` in Agent chat** - pick a command. Each shows a one-line description in the menu.

| Command | When to use |
|---------|-------------|
| `/ticket-kickoff` | Start a ticket (Plan gate) |
| `/prove-ticket` | Run Bob E2E when you want proof |
| `/pre-ship` | Ship - per-repo PR packs under `docs/tdd-runs/<id>/PRE_SHIP_*.md` |
| `/rca-logs` | Prod log grep pack for RCA |

That is the full day-to-day menu. Bob hygiene (`chat-hygiene`, `memory-budget`, etc.) runs via agent hooks - you do not need to remember those.

Optional skills (only if you need them): `/cc-backend-test-generation`, `/generate-test-plan-change-flow-based`.

Glass Automations under `.cursor/automations/` are optional webhook drafts - not required for normal work.
