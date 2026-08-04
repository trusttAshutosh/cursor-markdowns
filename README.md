# Cursor markdowns (full agent migrate backup)

Personal git backup of **every agent-facing config** used for Novopay work (global + local).
Use this repo to restore Cursor/Bob habits on a new laptop.

**Start here:** [WORKFLOW.md](WORKFLOW.md) - one-page visual cheat sheet (ticket -> Bob -> review -> pre-ship -> PR).

**Mobile approvals:** [MOBILE_RELAY.md](MOBILE_RELAY.md) - view/approve Cursor from phone ($0, local relay).

**Workspace cold start (live mirror):** [novopay/README.md](novopay/README.md) + [novopay/AGENTS.md](novopay/AGENTS.md).

## New laptop (double-click)

1. Install Git + Python 3 on the new machine.
2. Clone this repo to Desktop:

```bat
git clone https://github.com/trusttAshutosh/cursor-markdowns.git %USERPROFILE%\Desktop\cursor-markdowns
```

3. Double-click **`SETUP-NEW-LAPTOP-NOVOPAY.bat`**

That script will:
- create `%USERPROFILE%\Desktop\novopay`
- clone every repo listed in [`novopay-repos.tsv`](novopay-repos.tsv) (stable branches like `ddp-qa` / `dsa-qa` / `main`)
- restore Cursor rules/hooks/skills + workspace `.cursor`, `AGENTS.md`, validate tooling, Bob overlays from this backup

Repo list + restore logic: `novopay-repos.tsv` and `scripts/setup_new_laptop.py`.

Run sync after any hooks/rules/skills/commands/agent-entrypoint change:

```bash
python sync-cursor-backup.py
```

See `SYNC_MANIFEST.md` for last run file counts.

## Layout

| Backup path | Live source |
|-------------|-------------|
| `user/.cursor/` | `~/.cursor/` (rules, hooks, skills-cursor, plugins, plans, mcp.json, ...) |
| `novopay/.cursor/` | `Desktop/novopay/.cursor/` (commands, skills, automations, hooks, rules, mcp.json, ...) |
| `novopay/AGENTS.md` | Workspace orchestrator memory |
| `novopay/README.md` | Cold-start + scoped validate docs |
| `novopay/package.json` | Root `npm run validate/lint/format` entrypoints |
| `novopay/Makefile` | Optional Make wrappers for validate/lint |
| `novopay/scripts/validate-change.py` | Scoped per-service validation script |
| `novopay/novopay.code-workspace` | Multi-root workspace file |
| `novopay/bob-boot-remediation.yaml` | Bob boot failure patterns |
| `cc/.cursor/` | `novopay-platform-creditcard-management/.cursor/` |
| `agent-webapp/.cursor/` | `novopay-platform-agent-webapp/.cursor/` (FE skills/rules) |
| `bob/.cursor/` | `bob-the-builder/.cursor/` |
| `bob/skills/` | `bob-the-builder/skills/` (builder-analyst/implementer/verifier/...) |
| `bob/README.md` | Bob engine README |
| `bob/CURSOR_PLUGINS.md` | Recommended Cursor plugins |
| `bob/docs/` | KT / BOB_GUIDE / MCP_TOOL_BRIDGE / onboarding / cheatsheet |
| `bob/config/` | `mcp-servers.yaml`, `tool-bridge.yaml` (agent MCP wiring) |
| `bob-templates/host-cc/.cursor/` | Bob onboarding template (host CC) |
| `bob-templates/novopay/.cursor/` | Bob onboarding template (novopay) |
| `bob-templates/onboarding-cursor/` | Bob user-level hook template (`templates/onboarding/cursor/`) |
| `actor/.cursor/` | `novopay-platform-actor/.cursor/` |
| `gateway/.cursor/` | `novopay-platform-api-gateway/.cursor/` |
| `WORKFLOW.md` | Mirror of `novopay/.cursor/WORKFLOWS.md` |

## What is included (all `.cursor` file types)

- `hooks.json`, `hooks/**` (Python, shell, state JSON)
- `rules/**` (`.mdc`)
- `skills/**`, `skills-cursor/**` (`SKILL.md`, templates, README)
- `commands/**` (slash commands)
- `automations/**` (Glass JSON drafts)
- `agents/**`, `mcp.json`, plugin caches under `plugins/`
- `plans/**` (Cursor plan files)
- Top-level docs: `WORKFLOWS.md`, `CURSOR_PLUGINS.md`, `NOVOPAY_AGENT_PLAYBOOK.md`, etc.
- Workspace agent entrypoints: `AGENTS.md`, root `README.md`, validate script/package/Makefile, code-workspace

Symlinks (e.g. CC `skills` junction) are copied as **resolved file content**.

## New laptop restore (checklist)

**Preferred:** double-click [`SETUP-NEW-LAPTOP-NOVOPAY.bat`](SETUP-NEW-LAPTOP-NOVOPAY.bat) after cloning this repo to Desktop (see above).

Manual fallback:

1. Clone/copy this backup to `Desktop/cursor-markdowns`.
2. Run `SETUP-NEW-LAPTOP-NOVOPAY.bat` (or `python scripts/setup_new_laptop.py`).
3. Install recommended plugins from `novopay/.cursor/CURSOR_PLUGINS.md` (or `bob plugins`).
4. Open `Desktop/novopay/novopay.code-workspace`, run `python bob.py --help`, then `npm run validate -- <service-dir>` smoke.

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
- Do not commit secrets from `user/.cursor` plans/mcp if they contain tokens - review before push.
