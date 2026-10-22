---
name: ashutosh-exit-kt
description: >-
  Maintains Ashutosh Kumar's exit KT folder at Desktop/ashutosh-exit-kt.
  Appends only what AI cannot rebuild from PR titles, PR bodies, commit
  messages, or existing docs: unwritten agreements, landmines, unfinished
  status, people/access, hand-run ops, decision why. Use when Ashutosh says
  update my KT, exit KT, if I leave, or when a session surfaces a verbal
  agreement, production landmine, unique access, or WIP missing from git.
  Also run after a ticket milestone (RCA done, env leftover, ops asked).
---

# Ashutosh exit KT

Live: `C:\Users\ashutosh.kumar\Desktop\ashutosh-exit-kt`  
Backup: `Desktop/cursor-markdowns/ashutosh-exit-kt`

## Filter (do not violate)

Include: why, rejected alternative, looks-correct-still-fails, env/data/ops not in Flyway, who actually answers, WIP status that is not in git.

Exclude (link only): PR title/description, commit message, Jira description, AGENTS.md / BOB_GUIDE / onboarding / TICKET_RESUME body. Volume metrics. How the code works.

If the fact is already in a numbered file, do not duplicate - maybe one changelog line.

## When

- User says "update my KT" / "exit KT" / "if I leave"
- Ticket milestone: RCA confirmed, leftover is ops/bank, access discovered, decision locked
- Do not run after ordinary coding

## How

1. Read `README.md` filter. Pick **one** file.
2. Append a table row or `_template-entry.md` block. Do not rewrite the whole folder unless the user asked to fill/rebuild (this request).
3. Top of `CHANGELOG.md`: `- YYYY-MM-DD - <what>`. Bump `Last updated` in `README.md`.
4. Never copy secrets.
5. ASCII hyphen-minus only.
6. After folder or this skill changes: `python Desktop/cursor-markdowns/sync-cursor-backup.py`, then commit and push `cursor-markdowns` (user rule). Skip only if the user said not to.

| File | What |
| --- | --- |
| `01-ownership-map.md` | New silent go-to area |
| `02-promises-unwritten.md` | Spec vs what was agreed |
| `03-landmines.md` | Looks correct, still fails |
| `04-unfinished.md` | Alive / dead / waiting |
| `05-people-and-access.md` | Who to ping; access |
| `06-ops-hand-run.md` | Not in Flyway |
| `07-decision-journal.md` | Why + rejected |
| `08-cursor-bob-os.md` | Agent OS / laptop |

## Do not

- Dump a PR list or "work done this month"
- Invent bank promises
- Commit this folder into a Novopay service repo
