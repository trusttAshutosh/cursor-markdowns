# Backup policy (skills, rules, hooks, commands)

Whenever agent-facing config changes on the live machine, mirror it here **before the task is done**.

## Triggers (any create/edit)

| Live location | Examples |
|---------------|----------|
| `~/.cursor/rules/` | novopay-orchestrator, codeant guardrails |
| `~/.cursor/hooks/` | session hygiene, stop hooks |
| `Desktop/novopay/.cursor/` | skills, rules, commands, WORKFLOWS |
| Service `*/.cursor/` | CC, agent-webapp, bob overlays |
| Cursor Settings user rules | Also update `user/CURSOR_USER_RULES.md` |
| Bob agent config | shrink-logs, boot-remediation, builder patches |

## Agent workflow (automatic)

```bash
cd Desktop/cursor-markdowns
python sync-cursor-backup.py
git add -A   # review diff; exclude secrets if any
git commit -m "feat: <what changed>" -m "<why / which workflow it supports>"
git push origin main
```

**Commit message:** state what changed and why (not just "update files"). Example:

```
feat: backup token hygiene workflow (shrink-logs, prompt-hygiene)

Agent shrinks pasted logs automatically; full.log via latest.json.
```

## Skip push only when

User explicitly says no commit/push for that task.

## Restore

New laptop: `SETUP-NEW-LAPTOP-NOVOPAY.bat` applies everything synced here.
