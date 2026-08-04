# Novopay workspace

## Quick start (agents)

- Open `novopay.code-workspace`. Workflows: `.cursor/WORKFLOWS.md`. Skills: `.cursor/skills/`.
- Bob: `python bob.py` / `bob.cmd`. `bob validate-ticket` only when asked to prove.
- Scoped check: `npm run validate -- <service-dir>` (README). No full monorepo rebuild.
- SQL: fully qualified `schema_name.table_name`. Prefer `.cursor/memory/prod-ddl/`. No `/actuator/health`.

## Orchestrator model (fixed - do not let Continual Learning edit this section)

**You (human):** approve or reject at four gates only - Plan, Build, Prove, Ship.

**Agent:** everything else - workspace, memory, skills, Bob runs, boot fixes, hygiene.

**Bob:** proof engine. Agent implements; Bob produces `REPORT.md` evidence.

Do not ask the human to pin files, switch workspace, or run memory chores.

### Gate checklist for the human

1. **Plan** - scope right?
2. **Build** - diff matches plan?
3. **Prove** - Bob `GATE_SUMMARY.md` PASS for the ticket?
4. **Ship** - OK to commit/PR?

### Agent self-check (fixed - do not let Continual Learning edit this section)

1. **Scope** - Diff matches plan/ticket; no drive-by edits.
2. **Compile** - `npm run validate -- <touched-dir>` when feasible.
3. **SQL / DB** - Fully qualified names; prefer ticket verify SQL.
4. **No actuator health** - Use Bob / boot logs / real API answers.
5. **Bob stays explicit** - No `bob validate-ticket` unless asked to prove.
6. **Risk spot-check** - Read riskiest changed files once.
7. **Report briefly** - What was self-checked; what still needs Prove.

---

Plain bullets below are for Continual Learning. Keep section names exactly as named.
Add only durable, cross-ticket guidance. Ticket-specific rules belong in `docs/tdd-runs/<ticket-id>/`, not here.

## Learned User Preferences

- No commit/push unless asked; paste-ready commit when asked (`/babysit` may ship scoped PR fixes).
- Subjects: `fix: ...` — no service-name scopes. Bob only when asked; E2E proof default; autoboot.
- One ticket per chat. Prove vulns before/after. Prefer test fixes; port from `ddp-qa`/`ddp-uat` when present.
- Surgical reuse; constants classes; gateway stays generic. CodeAnt + RCA rules under `~/.cursor/rules/`.
- SQL fully qualified; call out env drift; lock Flyway seq from common-scripts. Log greps: `grep` on `/apps/applogs/...` only.
- Sync backend on `ddp-qa`; frontend `dsa-qa` when needed. `/thermo-nuclear-code-quality-review` on big diffs. Prefer source-of-truth rules over FE copies.

## Learned Workspace Facts

- Root `Desktop/novopay`; skills `.cursor/skills/`; `novopay.code-workspace`; orchestrator `novopay-orchestrator.mdc`.
- Bob artifacts `docs/tdd-runs/<id>/`. Local DB often `root`/`root`. Tenants `ddp,dsa,kp,ra,rbg,bb`; schema `{tenant}_{service}` (confirm DDL).
- Logs `/apps/applogs/{common|tenant}/`. Branches: backend `ddp-*`, frontend `dsa-*`. Lib via CC `includeBuild`.
