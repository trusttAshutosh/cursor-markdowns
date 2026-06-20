# Ashutosh - Novopay workflow (one page)

**Flowchart legend:** `/command` = slash command (exact sample) | **Say "..."** boxes = type that phrase in chat

## Happy path (ticket to PR)

```mermaid
flowchart TD
  A[New ticket] -->|/ticket-kickoff PE-123| B[Plan scope repos questions]
  B --> C[Implement in chat]
  C --> D{Want proof?}
  D -->|No| C
  D --> S1["Say \"bob validate PE-123\""]
  S1 --> E[Bob E2E evidence]
  E --> F{Ready to ship?}
  C --> F
  F -->|/thermo-nuclear-code-quality-review| G[Code quality on diff]
  G -->|/pre-ship PE-123| H[PRE_SHIP md per repo]
  H --> S2["Say \"commit and push open PR\""]
  S2 --> I[Done]
```

## If you want this, use this

| I want to... | Do this |
|--------------|---------|
| Start a ticket | `/ticket-kickoff PE-123` |
| Explain scope / raw idea | Normal chat, or kickoff above |
| Prove it works (API + DB + logs) | Say **"bob validate PE-123"** or **"bob let's test"** |
| Big diff before merge | `/thermo-nuclear-code-quality-review` |
| PR description files (diagrams, UTs, cross-repo) | `/pre-ship PE-123` |
| Commit / push / PR | Say **"commit and push open PR"** |
| Prod logs grep pack | `/rca-logs` then describe issue in same message |
| Full incident doc (git history, when it broke) | Say **"root cause for PE-123"** |
| Unit tests for CC change | `/cc-backend-test-generation` (optional) |

## Prod incident (side path)

```mermaid
flowchart LR
  P[Prod symptom] -->|/rca-logs| Q[grep command pack]
  Q --> S1["Say \"root cause for PE-123\""]
  S1 --> R[Incident doc with git history]
  R --> S[Fix then happy path]
```

## Rules you do not need to remember

- Bob **never** auto-runs after a code fix - only when you ask to test.
- Hooks handle chat hygiene / memory - no commands for that.
- Glass automations under `novopay/.cursor/automations/` are optional - use `/` commands instead.

## Where config lives (this repo)

| Need | Path in cursor-markdowns |
|------|--------------------------|
| This cheat sheet | `WORKFLOW.md` |
| Slash commands | `novopay/.cursor/commands/` |
| Incident RCA format | `user/.cursor/rules/incident-analysis-format.mdc` |
| Orchestrator prefs | `user/.cursor/rules/novopay-orchestrator.mdc` |
| Sync backup | `python sync-cursor-backup.py` |
