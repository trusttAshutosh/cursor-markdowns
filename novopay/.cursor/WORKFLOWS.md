# Ashutosh - Novopay workflow (one page)

**Type `/` in Agent chat** for commands. Everything else is normal chat.

## Happy path (ticket to PR)

```mermaid
flowchart TD
  A[New ticket] -->|ticket-kickoff| B[Plan scope repos questions]
  B --> C[Implement in chat]
  C --> D{Want proof?}
  D -->|No| C
  D -->|bob validate| E[Bob E2E evidence]
  E --> F{Ready to ship?}
  C --> F
  F -->|thermo-nuclear review| G[Code quality on diff]
  G -->|pre-ship| H[PRE_SHIP md per repo]
  H --> I[commit push open PR]
```

## If you want this, use this

| I want to... | Do this |
|--------------|---------|
| Start a ticket | `/ticket-kickoff PE-123` |
| Explain scope / raw idea | Normal chat, or kickoff above |
| Prove it works (API + DB + logs) | **Only when you choose:** "bob validate PE-123" or `/prove-ticket PE-123` |
| Big diff before merge | `/thermo-nuclear-code-quality-review` |
| PR description files (diagrams, UTs, cross-repo) | `/pre-ship PE-123` |
| Commit / push / PR | Ask explicitly - agent never auto-commits |
| Prod logs grep pack | `/rca-logs` + service, date, mobile/stan |
| Full incident doc (git history, when it broke) | Ask: "root cause for ..." (incident rule applies) |
| Unit tests for CC change | `/cc-backend-test-generation` (optional) |

## Prod incident (side path)

```mermaid
flowchart LR
  P[Prod symptom] -->|rca-logs| Q[grep command pack]
  Q --> R[Ask root cause]
  R --> S[Incident doc with git history]
  S --> T[Fix then happy path]
```

## Rules you do not need to remember

- Bob **never** auto-runs after a code fix - only when you ask to test.
- Hooks handle chat hygiene / memory - no commands for that.
- Ignore `novopay/.cursor/automations/` unless you saved Glass webhooks yourself.

## Backup copy

Same file mirrored in `Desktop/cursor-markdowns/WORKFLOW.md`.
