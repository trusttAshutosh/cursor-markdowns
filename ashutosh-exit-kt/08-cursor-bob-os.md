# 08 - Cursor / Bob / laptop

Do not re-teach Bob. `BOB_GUIDE.md` is the team KT.

## 15-minute successor brief

1. Human is orchestrator. Agent codes. Bob **proves** only.
2. SoT: `Desktop/novopay/AGENTS.md`. Skills: `Desktop/novopay/.cursor/skills/`.
3. This exit folder is the unwritten layer. Personal skill `~/.cursor/skills/ashutosh-exit-kt/`.
4. Laptop migrate: `Desktop/cursor-markdowns` → `trusttAshutosh/cursor-markdowns`. `python sync-cursor-backup.py` then commit/push.
5. Secrets stay on the laptop. `novopay-remote-db.env` is **excluded** from that sync.

## Intentional, do not "fix"

| Tempting cleanup | Why it stays |
| --- | --- |
| Re-enable Continual Learning stop hook | Plugin updates restore it; he disables it |
| `move_agent_to_root` | Cursor 3.21.x kills the agent |
| Auto `bob validate-ticket` | Explicit-only |
| TaskAlloc Flyway in the JAR | HDP-8967 collision |
| Rank people by Cursor co-author % | He disables trailers; % != usage |
| Use Atlassian MCP because it "works" | Signed in as Deepankar; HDP-11225 already mis-attributed |

## Restore if the laptop dies

1. Clone cursor-markdowns (this folder is `ashutosh-exit-kt/`).
2. Restore `user/.cursor` minus secrets. Recreate `novopay-remote-db.env` from ops.
3. Open `novopay.code-workspace`.
4. Read AGENTS.md, then BOB_GUIDE.md.
5. Copy LOC workbook from whoever still has `LOC APIs mapping v 0.1 (2).xlsx` - it is not in git.

## Tools easy to lose

| Tool | Path |
| --- | --- |
| Remote DB / SSH / Superset | `%USERPROFILE%\.cursor\novopay-remote-db-readonly.py` (and ssh / superset siblings) |
| MarkItDown shim | `%USERPROFILE%\.cursor\tools\markitdown-shim\cli.py` |
| PR cadence | `Desktop/novopay/tools/pr_cadence_refresh.py` |
| Work evidence | `Desktop/novopay/tools/personal_work_evidence_refresh.py` |
| Standup collector | `Desktop/worklogs/_tools/collect_day.py` |
| BKYC Jira comment pull | `docs/tdd-runs/HDP-7636/pull_bkyc_jira_comments.py` |

## Not in git (ask him)

- Bank UAT has no agent DB access - discovery is pasted SQL only
- mdshare PAT in Cursor MCP config (Grafana docs HDP-11496)
- Worktrees `.wt-*` that still hold a ticket
- Who may push cursor-markdowns after he leaves: [FILL]
- Seqrite hang on ATSLAP-43: do not "fix Gradle"; RCA `docs/RCA_WINDOWS_FILE_HANG_SEQRITE_2026-09-02.md`
- Gradle loopback: `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Users/ashutosh.kumar/tmpnio`
- Gateway common-scripts hook: `NOVOPAY_GIT_HOOK_SKIP_PROD_SYNC=1` per commit only, with approval
- Claude artifact share pin must be moved after every republish
- Worktrees still in play: `.wt-webapp-hdp-12386`, `.wt-11796*`, `.wt-dpb-2148*`, `.wt-lib-bkyc`
