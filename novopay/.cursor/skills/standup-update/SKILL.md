---
name: standup-update
description: Builds Ashutosh's daily standup update (Yesterday / Today / Blocker) from Cursor chats, Claude Code / Claude desktop sessions and git commits made on this machine, plus any notes the user pastes. Use when the user asks "what did I do yesterday", "what did I do on Friday", "standup update", "short update for standup", or "what new to tell".
---

# Standup update

Commit-only skills (`what-did-i-get-done`) miss investigations, RCAs, env checks and Superset/config work, and Cursor-only views miss Claude work. This skill merges both tools + commits + user notes.

## Workflow

1. **Gather evidence** with the shared collector (same one Claude Code `/standup` and `/where-did-time-go` use - do not write a parallel parser):
   ```bash
   python ~/Desktop/worklogs/_tools/collect_day.py --date last-workday   # Mon -> Fri
   python ~/Desktop/worklogs/_tools/collect_day.py --date friday
   python ~/Desktop/worklogs/_tools/collect_day.py --date 2026-09-28
   ```
   Output: IST activity blocks from Cursor and Claude sessions (with asks + outcome) and commits made on this machine. If the sandbox blocks the shell, retry with `required_permissions: ["all"]` (read-only).
2. **Merge user notes.** Anything the user pastes (ticket handoff, "I started at 4, Superset was down") overrides chat guesses. Items the user says are still pending go under **Today**, not **Yesterday**.
3. **Group by ticket**, not by tool or repo. Merge the same topic worked in both Cursor and Claude. Fold Sonar/test follow-up commits into the parent item. Uncommitted work counts - say "in progress, not committed".
4. **Write the update** in the format below.

## Output format (default = short)

```
**Yesterday:**
- <Ticket/area>: <what was done, plain outcome> (verified on QA/UAT if true)
- ...

**Today:**
- <ticket>: <next concrete step>

**Blocker:** <one line, or "none">
```

Rules:
- Plain English a manager can read aloud; no class names, file paths, commit SHAs.
- 4-6 Yesterday bullets max; merge small investigations into one "Also looked into ..." bullet.
- State outcome and status honestly (fixed / partly fixed / blocked / started late).
- Include ticket ids (`HDP-xxxx`) when known; if none, name the area (CC, BKYC, KYC Engine).
- If the user asks "what new to tell", add a short **New to tell** section: corrected diagnoses, dates owed to stakeholders, asks from others.
- Longer version only if asked: add per-item detail and chat links (`[title](<uuid>)` for Cursor; name the Claude session title).

## Limits

- Only this machine's sessions and commits are included (the Claude account is shared; other users' work never lands here).
- Durations are estimates (45m idle split, 3h block cap); standup does not need them - use `/where-did-time-go` for the timed view.
