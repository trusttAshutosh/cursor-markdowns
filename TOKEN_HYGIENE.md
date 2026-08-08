# Token hygiene - paste logs without thinking

Backup of the Aug 2026 token-saving workflow. User habit stays the same: **paste logs, ask questions**.

## What it does

| Piece | Purpose |
|-------|---------|
| `bob shrink-logs` | Compress pasted logs for chat; full original preserved on disk |
| `prompt-hygiene` skill | Agent routes paste-logs / RCA / merge / compile patterns cheaply |
| `memory-budgeting.mdc` | Always-on: shrink first; agent reads full.log when digest is not enough |
| `latest.json` | Pointer to most recent shrink - agent never asks user for paths |
| User rule | Paste logs as-is; agent owns shrink + full.log lookup |

## User workflow (zero change)

1. Paste logs + "what happened?"
2. Agent runs `bob shrink-logs`, answers from digest
3. Follow-up questions -> agent reads `full.log` via `.cursor/evidence/logs/latest.json`
4. User never runs scripts or types paths

## Digest keeps (not errors-only)

- ERROR/WARN/exceptions/STAN/CRN/4000xxx
- Journey markers: request-out, response-in, SUCCESS, processor names, TransactionAudit
- Context window around signals; gap bridges for long silent spans
- Full log always at `<timestamp>/full.log`

## Bob command

```bash
cd Desktop/novopay
python bob.py shrink-logs path/to.log
python bob.py shrink-logs -   # stdin
```

Output folder: `novopay/.cursor/evidence/logs/<timestamp>/` plus `latest.json`.

## One-time machine hygiene (not daily)

```bash
python bob.py prune-overhead --apply   # reload Cursor after
python bob.py chat-hygiene --auto      # also runs on Cursor session start
```

## Files in this backup

| Path | Live source |
|------|-------------|
| `novopay/.cursor/skills/prompt-hygiene/` | `Desktop/novopay/.cursor/skills/prompt-hygiene/` |
| `novopay/.cursor/rules/memory-budgeting.mdc` | same |
| `novopay/.cursor/commands/rca-logs.md` | same |
| `novopay/.cursor/WORKFLOWS.md` | same (mirrored to `WORKFLOW.md`) |
| `bob/runner/lib/shrink_logs.py` | `bob-the-builder/runner/lib/shrink_logs.py` |
| `bob/runner/tests/test_shrink_logs.py` | `bob-the-builder/runner/tests/test_shrink_logs.py` |
| `bob/runner/patches/builder_cli-shrink-logs.md` | Notes for wiring `shrink-logs` in builder_cli.py |
| `user/CURSOR_USER_RULES.md` | Cursor Settings user rules snapshot |

## Restore on new laptop

1. Run `SETUP-NEW-LAPTOP-NOVOPAY.bat` (restores `.cursor` trees **and** `bob shrink-logs`)
2. Re-add user rules from `user/CURSOR_USER_RULES.md` in Cursor Settings (4 rules)
3. Once: `python bob.py prune-overhead --apply` then reload Cursor

`setup_new_laptop.py` copies `shrink_logs.py` + tests and wires `builder_cli.py` automatically when upstream bob lacks the command.
