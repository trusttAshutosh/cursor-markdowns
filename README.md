# Cursor markdowns (full .cursor backup)

Personal git backup of **every `.cursor` config tree** used for Novopay work (global + local).

**Start here:** [WORKFLOW.md](WORKFLOW.md) - one-page visual cheat sheet (ticket -> Bob -> review -> pre-ship -> PR).

Run sync after any hooks/rules/skills/commands change:

```bash
python sync-cursor-backup.py
```

See `SYNC_MANIFEST.md` for last run file counts.

## Layout

| Backup path | Live source |
|-------------|-------------|
| `user/.cursor/` | `~/.cursor/` (rules, hooks, skills-cursor, plugins, plans, mcp.json, ...) |
| `novopay/.cursor/` | `Desktop/novopay/.cursor/` (commands, skills, automations, hooks, rules, ...) |
| `cc/.cursor/` | `novopay-platform-creditcard-management/.cursor/` |
| `bob/.cursor/` | `bob-the-builder/.cursor/` |
| `bob-templates/host-cc/.cursor/` | Bob onboarding template (host CC) |
| `bob-templates/novopay/.cursor/` | Bob onboarding template (novopay) |
| `bob-templates/onboarding-cursor/` | Bob user-level hook template (`templates/onboarding/cursor/`) |
| `actor/.cursor/` | `novopay-platform-actor/.cursor/` |
| `gateway/.cursor/` | `novopay-platform-api-gateway/.cursor/` |
| `novopay/AGENTS.md` | Workspace orchestrator memory |
| `novopay/bob-boot-remediation.yaml` | Bob boot failure patterns |

## What is included (all `.cursor` file types)

- `hooks.json`, `hooks/**` (Python, shell, state JSON)
- `rules/**` (`.mdc`)
- `skills/**`, `skills-cursor/**` (`SKILL.md`, templates, README)
- `commands/**` (slash commands)
- `automations/**` (Glass JSON drafts)
- `agents/**`, `mcp.json`, plugin caches under `plugins/`
- `plans/**` (Cursor plan files)
- Top-level docs: `WORKFLOWS.md`, `CURSOR_PLUGINS.md`, `NOVOPAY_AGENT_PLAYBOOK.md`, etc.

Symlinks (e.g. CC `skills` junction) are copied as **resolved file content**.

## Excluded (IDE runtime only - not config)

These live under `~/.cursor/` but are **not** backed up:

| Path | Why |
|------|-----|
| `extensions/` | VS Code extension installs |
| `projects/` | Agent transcripts, MCP tool cache (regenerated) |
| `ai-tracking/` | Local usage DB |
| `debug-logs/`, `snapshots/` | Ephemeral |
| `ide_state.json` | Session UI state |

Hook throttle timestamps (e.g. `posttool-nudge-ts`) **are** backed up when present.

## Policy

- Canonical skills: edit only `novopay/.cursor/skills/`; CC uses a junction on disk.
- Re-run `sync-cursor-backup.py` before committing this repo.
