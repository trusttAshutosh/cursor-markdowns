---
name: ashutosh-exit-kt
description: >-
  Maintains Ashutosh Kumar's exit knowledge-transfer folder on Desktop
  (ashutosh-exit-kt). Appends only what AI cannot reconstruct from git/Jira:
  unwritten bank/product/QA promises, landmines, unfinished threads, people/access,
  hand-run ops, and decision why. Use when Ashutosh says update my KT, exit KT,
  if I leave, handover notes, or when a session surfaces a verbal agreement,
  production landmine, unique access, or WIP missing from Jira/git.
---

# Ashutosh exit KT

Live folder: `C:\Users\ashutosh.kumar\Desktop\ashutosh-exit-kt`  
Backup: `Desktop/cursor-markdowns/ashutosh-exit-kt` (via `sync-cursor-backup.py`)

## When to run

- User says "update my KT", "exit KT", "if I leave", or similar
- End of a session that produced a **durable unwritten** fact (promise, landmine, access, unfinished thread, why-not-how)

Do **not** run for ordinary ticket coding, architecture explanations, or facts already in `AGENTS.md`.

## Rules

1. Append. Do not rewrite the folder. Do not dump architecture.
2. Never copy secrets (`.env`, passwords, webhooks, tokens). Point at the file path.
3. ASCII hyphen-minus only. No em/en dashes.
4. Put the bullet in the **one** matching file:

| File | What goes there |
| --- | --- |
| `01-ownership-map.md` | New silent ownership |
| `02-promises-unwritten.md` | Verbal agreements vs ticket text |
| `03-landmines.md` | Looks correct, still fails |
| `04-unfinished.md` | Alive / dead / waiting |
| `05-people-and-access.md` | Who to ping; access to transfer |
| `06-ops-hand-run.md` | SQL / flushes not in Flyway |
| `07-decision-journal.md` | Why + rejected alternative |
| `08-cursor-bob-os.md` | Agent OS / laptop restore |

5. Use the shape in `_template-entry.md` (or a one-line table row if that file is already a table).
6. Add one line at the top of `CHANGELOG.md`: `- YYYY-MM-DD - <what>`. Update `Last updated` in `README.md`.
7. After any skill/folder edit this session: run `python Desktop/cursor-markdowns/sync-cursor-backup.py`, then commit and push `cursor-markdowns` (user rule). Skip only if the user said not to.

## Do not

- Duplicate `AGENTS.md` / `BOB_GUIDE.md` / product onboarding
- Invent bank promises
- Commit this folder into a Novopay service repo
