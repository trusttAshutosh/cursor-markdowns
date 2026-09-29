---
name: where-did-time-go
description: Daily workflog across Cursor chats, Claude Code sessions and git commits - one chronological table with build/ops/meta tags, Total + Mix + Legend footer, saved to Desktop/worklogs. Rules live in the Cursor skill; this command only adds the Claude Code evidence.
argument-hint: "[today | yesterday | YYYY-MM-DD | weekday] [notes...]"
disable-model-invocation: true
allowed-tools: Bash(python C:/Users/ashutosh.kumar/Desktop/worklogs/_tools/collect_day.py:*) Bash(python C:/Users/ashutosh.kumar/.cursor/skills/where-did-time-go/scripts/save_workflog.py:*)
---

# /where-did-time-go (Cursor + Claude Code)

Arguments: `$ARGUMENTS` - optional day first (`today` default, `yesterday`, `YYYY-MM-DD`,
weekday name), then any notes.

## 1. Load the rules (single source of truth)

Read `C:/Users/ashutosh.kumar/.cursor/skills/where-did-time-go/SKILL.md` in full, every run.
Follow it exactly - output format, Work tags, Ticket column, Total / Mix / Legend footer,
optional spoken shape, persistence layout. Do not work from memory of an earlier run.

Only the points below override it.

## 2. Evidence - replaces its steps 2-3 and the "only ~/.cursor/projects" guardrail

Run (read-only, ~3 s):

```
python C:/Users/ashutosh.kumar/Desktop/worklogs/_tools/collect_day.py --date <day>
```

It prints, in IST, every activity block from **both** tools, already split on idle gaps
over 45 min and capped at ~3 h, with meta prompts removed, plus that day's commits from
all novopay repos (same subject on several branches collapsed):

- Cursor: `~/.cursor/projects/*/agent-transcripts/*/*.jsonl` (subagents skipped), times
  from `<timestamp>` tags, queries from `<user_query>`.
- Claude Code: `~/.claude/projects/*/*.jsonl`, human prompts only (tool results, `isMeta`,
  sidechain and injected system text skipped), UTC converted to IST.
- Git: commits in the workspace root, `bob-the-builder`, `novopay-platform-*`,
  `trustt-platform-*` that you authored **and** committed (your `user.email`) and that
  appear in the local reflog, i.e. were made on this machine. Colleagues' cherry-picks of
  your commits, GitHub merges and stashes are excluded.

Only work done on this machine counts: the Claude account is shared, so the collector
also skips any Claude session whose working folder is outside this Windows profile.

Notes the user gives (in `$ARGUMENTS` or the chat) override anything guessed from chats.
If the collector fails, say so and fall back to reading those paths yourself.

## 3. Merge rules

- Every block from both tools goes into **one** table sorted by start time. Never split
  the output by tool.
- Chat column: `Cursor: [title](uuid)` or `Claude: [title](session-id)`. Write a short
  functional title; do not paste the raw first prompt.
- Same topic running in both tools at overlapping times -> one row, minutes counted once,
  Chat cell lists both cites. Different topics overlapping -> separate rows with `(overlap)`,
  per the Cursor skill.
- A collector block that is clearly two topics may be split; adjacent blocks of the same
  topic in the same session may be joined if the gap is under 45 min.
- `single stamp` blocks -> `~15m` per the Cursor skill.
- Ignore meta prompts that slipped through (what did I do yesterday, standup update,
  continual-learning injections, this command itself). Standup/worklog tooling work that
  took real time can stay as a `meta:` row.
- Attach commits to the block they belong to (Ticket column from commit subjects too);
  do not add commit-only rows when a chat already covers the work.

## 4. Persist

Save the exact markdown shown to the user with the existing helper (it picks the
`YYYY-MM/YYYY-MM-DD/hh-mm_AM|PM.md` name and front matter):

```
python C:/Users/ashutosh.kumar/.cursor/skills/where-did-time-go/scripts/save_workflog.py --work-day <day> --person Ashutosh --input <tmp.md>
```

Write `<tmp.md>` first as `%TEMP%\workflog-<day>.md` (short path - the session scratchpad
path is longer than Windows MAX_PATH and Python cannot open it), delete it after saving,
then print `Saved: Desktop/worklogs/...` in one line.
