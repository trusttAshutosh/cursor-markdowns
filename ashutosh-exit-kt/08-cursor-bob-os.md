# 08 - Cursor / Bob / laptop OS

This is the piece that is most "Ashutosh" and least in any product ticket. Do **not** re-teach Bob from scratch. Point at `BOB_GUIDE.md`.

---

## What the successor must understand in 15 minutes

1. Ashutosh is the orchestrator. The agent does the work. Bob only **proves**.
2. Four gates: Plan, Build, Prove, Ship. Human approves those only.
3. Canonical agent rules: `Desktop/novopay/AGENTS.md` (not a parallel preference list).
4. Canonical skills: `Desktop/novopay/.cursor/skills/` (not copies in service repos, except CC junction).
5. Personal skills: `%USERPROFILE%\.cursor\skills\` (this exit-KT skill lives here).
6. Laptop migrate backup: `Desktop/cursor-markdowns` → GitHub `trusttAshutosh/cursor-markdowns`. Run `python sync-cursor-backup.py` then commit/push.
7. Secrets stay on the laptop: `novopay-remote-db.env` is in the sync **exclude** list on purpose.

## Do not "fix" these; they are intentional

| Tempting cleanup | Why it is on purpose |
| --- | --- |
| Re-enable Continual Learning stop hook | Plugin updates restore it; he disables it (`disable-continual-learning-stop.py`) |
| Call `move_agent_to_root` to tidy workspace | Cursor 3.21.x kills the agent (`abortReasonMessage: migration`) |
| Auto-run `bob validate-ticket` after every edit | Explicit-only |
| Put TaskAlloc Flyway back in the service JAR | Boot `flyway_auto_update=0`; HDP-8967 collision |
| Rank people by Cursor co-author trailers | He disables co-authored; trailer % != usage |

## Restore path if the laptop dies tomorrow

1. Clone `trusttAshutosh/cursor-markdowns` (this exit-KT folder is synced there as `ashutosh-exit-kt/`).
2. Restore `user/.cursor` (minus secrets). Recreate `novopay-remote-db.env` from ops, not from git.
3. Open `novopay.code-workspace`.
4. Read `AGENTS.md`, then `BOB_GUIDE.md`.
5. Do not expect BKYC Chat posts to be running.

## Tools he owns that are easy to lose

| Tool | Path |
| --- | --- |
| Remote DB helper | `%USERPROFILE%\.cursor\novopay-remote-db-readonly.py` |
| Remote SSH helper | `%USERPROFILE%\.cursor\novopay-remote-ssh.py` |
| MarkItDown shim | `%USERPROFILE%\.cursor\tools\markitdown-shim\cli.py` |
| PR cadence | `Desktop/novopay/tools/pr_cadence_refresh.py` |
| Standup collector | `Desktop/worklogs/_tools/collect_day.py` |
| BKYC Jira comment pull | `docs/tdd-runs/HDP-7636/pull_bkyc_jira_comments.py` |

## [FILL]

- [ ] Any MCP / plugin he paid for or configured that is not in cursor-markdowns
- [ ] Who is allowed to push `cursor-markdowns` after he leaves
