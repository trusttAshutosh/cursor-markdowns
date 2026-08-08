---
name: prompt-hygiene
description: Route Ashutosh's usual prompts (paste logs, RCA, merge conflicts, compile, bob validate) with minimal token use. Auto-run bob shrink-logs on log blobs. Use when user pastes logs, asks what happened, reports prod issues, merge conflicts, or compile errors.
---

# Prompt hygiene (Ashutosh workflow)

User should **not** change habits. Agent adapts to these patterns automatically.

## Pattern map

| User does this | Agent does this (no asking) |
|----------------|----------------------------|
| Pastes logs / "what happened" / prod symptom | **Shrink first** (below), then RCA - no fix until asked |
| `/rca-logs` or grep request | Grep commands only; no Bob validate |
| "merge conflict" / conflict markers | Read conflict hunks only; no full-file @ |
| "compile fails" / Gradle error | Read last ~80 lines of error output; scoped `./gradlew` or `npm run validate` |
| "bob validate X" / "bob let's test" | `bob validate-ticket X` only |
| Ticket id + short symptom | `bob context --ticket X` once; link paths, no CONTEXT_PACK dump |
| "fix it" after RCA | Implement |

## Log paste - mandatory shrink (agent-owned, zero user paths)

When chat contains a **log blob** (>=40 lines, or timestamps + ERROR/Exception/STAN/4000xxx):

1. Save blob to `.cursor/evidence/logs/incoming-<ts>.log` (or user file path).
2. Run: `bob shrink-logs <path> [--ticket ID if known]`
3. Record paths from shrink output. Bob also writes `.cursor/evidence/logs/latest.json` (always the most recent paste).
4. Read **digest first** (`digest.log`). Reply from digest; do **not** quote or re-paste full logs into chat.
5. **If digest is not enough** (journey gap, missing step, user asks follow-up on same logs): read `full.log` automatically - **never ask the user for a path**.
   - Same chat / just pasted: use `full_path` from this shrink (or `latest.json`).
   - Follow-up later in chat: read `.cursor/evidence/logs/latest.json` then open its `full_path`.
   - Grep targeted slices from `full.log` on disk (STAN, CRN, processor, time window) - still never paste full log into chat.
6. User never runs scripts or memorizes paths unless they want to.

## RCA (existing user rule)

Deliver RCA + timeline + "recent regression?" before fix. Summarize in <=15 lines; evidence paths not walls of text.

## Model discipline

Hygiene tasks (merge, compile, grep pack): prefer fast/cheap model. RCA/architecture: frontier ok.

## One ticket per chat

New ticket or context feels fat -> new chat + `TICKET_RESUME.md`. Link Bob `GATE_SUMMARY.md` (~5 lines), never full REPORT.
