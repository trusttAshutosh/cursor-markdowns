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

## Post to Jira (weekday standup work log)

- Home ticket: [HDP-11991](https://novopay.atlassian.net/browse/HDP-11991) "DAILY UPDATES - Ashutosh Kumar" (team pattern: one DAILY UPDATES story per person).
- After sharing the short update, ask whether to post it. Post only after the user approves that day's text (approval is per day, never standing).
- Post as a Jira **work log** (Atlassian MCP `addOrEditJiraIssueWorklog`), not a comment: `timeSpent` `15m`, description = `**Standup - <Ddd DD Mon YYYY>**` heading, then a `**TL;DR:**` line (1-2 sentences: yesterday's main outcomes + today's top priorities, linked), then the approved update in Cloud Markdown. Every day's work log has the TL;DR; refresh it whenever the work log is edited (e.g. a newly assigned ticket goes into Today).
- **Always hyperlink, every mention, in every section (Yesterday, Today, Blocker), in chat and in Jira:** tickets as `[HDP-x](https://novopay.atlassian.net/browse/HDP-x)`, PRs as `[<repo> #<n>](https://github.com/trusttai/<repo>/pull/<n>)`, docs as their mdshare URL. Repeats get linked again. If a PR number is unknown (e.g. "draft PR", "the fix"), look it up with `gh pr list --repo trusttai/<repo> --author trusttAshutosh --state all` before writing - never leave a bare "#649" or "the PR".
- One work log per weekday: before posting, list that day's work logs on HDP-11991 and edit the existing one instead of adding a duplicate.
- Reminder: Windows task `Standup-Reminder` pops at 09:59 on weekdays (`tools/standup_reminder.vbs`, `tools/standup_reminder.task.xml`, UTF-16).

## Limits

- Only this machine's sessions and commits are included (the Claude account is shared; other users' work never lands here).
- Durations are estimates (45m idle split, 3h block cap); standup does not need them - use `/where-did-time-go` for the timed view.
