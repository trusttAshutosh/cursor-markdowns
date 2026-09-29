---
name: standup
description: Short standup update (Yesterday / Today / Blocker, grouped by ticket) from Cursor chats, Claude Code sessions, git commits and pasted notes. Use for "standup update", "what did I do yesterday / on Friday", "short update for standup", "what new to tell". Rules live in the novopay Cursor skill standup-update.
argument-hint: "[last-workday | yesterday | YYYY-MM-DD | weekday] [notes...]"
allowed-tools: Bash(python C:/Users/ashutosh.kumar/Desktop/worklogs/_tools/collect_day.py:*)
---

# /standup (Cursor + Claude Code)

Arguments: `$ARGUMENTS` - optional day first, then any notes. Default day = **last workday**
(Monday -> Friday, weekend -> Friday).

## 1. Load the rules (single source of truth)

Read `C:/Users/ashutosh.kumar/Desktop/novopay/.cursor/skills/standup-update/SKILL.md` in full,
every run. Follow its workflow steps 2-4, output format and rules exactly (short Yesterday /
Today / Blocker, grouped by ticket, plain English, 4-6 Yesterday bullets, "New to tell" only
when asked, longer version only when asked).

Only the points below override it.

## 2. Evidence - replaces its step 1 (`gather.py`)

`gather.py` only sees Cursor chats. Run this instead (read-only, ~3 s):

```
python C:/Users/ashutosh.kumar/Desktop/worklogs/_tools/collect_day.py --date <day>
```

`<day>` = `last-workday` unless the user named one (`yesterday`, `friday`, `2026-09-28`).
It returns, in IST, the day's activity blocks from **Cursor and Claude Code** (meta prompts
removed) plus commits across all novopay repos with duplicate subjects collapsed. Judge chats
by their timestamps in the output, not by file modified date.

## 3. Merge rules

- Treat Cursor and Claude blocks as one pool of evidence; the same ticket worked in both
  tools is one bullet. Never split the update by tool.
- Group by ticket (`HDP-xxxx`), else by area (CC, BKYC, KYC Engine, Superset...). Fold Sonar /
  test follow-up commits into the parent item.
- Notes the user pastes override chat guesses. Items the user says are still pending go
  under **Today**, not Yesterday.
- **Today** = pending items from notes, plus unfinished state seen in the last blocks
  (uncommitted changes, draft PRs awaiting review, fixes waiting to be verified on QA/UAT).
- Ignore meta prompts (what did I do yesterday, standup update, continual-learning) and
  worklog/skill tooling unless it was the day's main work.
- Longer version only if asked: chat cites as `Cursor: [title](uuid)` / `Claude: [title](session-id)`.

Do not save a file; the standup is chat-only.
