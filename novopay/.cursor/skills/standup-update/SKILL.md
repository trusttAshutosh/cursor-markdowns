---
name: standup-update
description: Builds Ashutosh's daily standup update (Yesterday / Today / Blocker) from git commits across all Novopay repos plus that day's Cursor chats and any notes the user pastes. Use when the user asks "what did I do yesterday", "what did I do on Friday", "standup update", "short update for standup", or "what new to tell".
---

# Standup update

Commit-only skills (`what-did-i-get-done`) miss investigations, RCAs, env checks and Superset/config work. This skill merges commits + chats + user notes.

## Workflow

1. **Gather evidence** (run, do not read):
   ```bash
   python .cursor/skills/standup-update/scripts/gather.py              # last workday (Mon -> Fri)
   python .cursor/skills/standup-update/scripts/gather.py --date friday
   python .cursor/skills/standup-update/scripts/gather.py --date 2026-09-28
   ```
   Run from `Desktop/novopay`. If the sandbox blocks the shell, retry with `required_permissions: ["all"]` (read-only).
2. **Merge user notes.** Anything the user pastes (ticket handoff, "I started at 4, Superset was down") overrides chat guesses. Items the user says are still pending go under **Today**, not **Yesterday**.
3. **Group by ticket**, not by repo. One line per ticket; collapse duplicate commits (same subject on several branches) and Sonar/test follow-ups into the parent item.
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
- Longer version only if asked: add per-item detail and chat links as `[title](<chat-uuid>)`.

## Limits

- Chats are picked by transcript last-modified date, so a chat continued today will not show for yesterday - ask the user if an expected item is missing.
- Commits match author `shutosh`; edit `AUTHOR` in the script if the git identity changes.
