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

- Continual Learning must not auto-run after each prompt/stop; mine chats / update `AGENTS.md` only when explicitly asked. No commit/push unless asked (confirm with user before any commit); when asked to stage/commit, prefer paste-ready commit command with message + description (`/babysit` may ship scoped PR fixes).
- Never comment on Jira or make any Jira update (status, fields, links, etc.) without explicit user approval. When drafting Jira text: ASCII hyphens only, copy-pastable, hyperlink ticket/comment IDs, and readable by product/QA (not only engineers).
- After code-quality / Bugbot / thermo-nuclear (or similar) reviews: present findings only - **do not implement review fixes until the user has reviewed and asked to apply them**.
- Subjects: `fix: ...` - no service-name scopes. One ticket per chat; Bob only when asked; E2E proof default; autoboot. Prove vulns before/after. Prefer test fixes; port from `ddp-qa`/`ddp-uat` when present.
- **Unit tests:** run `gradle test` / the existing suite **only** in CC (`novopay-platform-creditcard-management` and the `*-ddp-uat` clone). For every other repo (task-allocation, Actor, lib, gateway, …): run **only the test class(es) written in this change** (`--tests com.example.NewTest`); never the preexisting suite, sibling tests, or `gradle test` with no filter. Compile (`compileJava`) is fine without tests. Skip even the new-class run when the environment cannot resolve that repo (missing includeBuild / JDK). Bob E2E is unchanged (explicit-only).
- Postman collections for QA/API packs: embed all variables in the collection; do not ship a separate environment file.
- Prefer cleaner/minimal solutions; if another approach is clearly better, mention it briefly then proceed with the cleaner default. Surgical reuse; constants classes; gateway stays generic. **Always avoid CodeAnt antipatterns while authoring:** (1) `java:S1192` duplicate string literals - extract constants at 3+ uses; (2) SQL `quote_identifiers` - backtick every table/column in Flyway. See `~/.cursor/rules/codeant-sonar-guardrails.mdc`.
- SQL fully qualified; call out env drift. **Flyway (normal process - no worktrees):** in the main repo clone, checkout latest remote **common-scripts** (often `ddp-fea-common-scripts`; discover via `git branch -r`), `git pull`, author migration there, take next unused tip seq - never invent seq from feature/`ddp-prod-master` alone. Stage for review; do not commit unless asked. User commits on common-scripts then cherry-picks to the feature branch. Log greps: `grep` on `/apps/applogs/...` only.
- Backend plan/branch from latest remote `origin/ddp-prod-master` (fetch first; task-allocation BKYC work uses `origin/ddp-fea-bkyc`); do not plan off stale local feature/`ddp-qa` checkouts. Frontend sync `dsa-qa` when needed. For UAT vs prod issues, compare latest remote `ddp-prod`/`ddp-uat` and, when UI may be involved, `dsa-prod`/`dsa-uat`. `/thermo-nuclear-code-quality-review` on big diffs. Prefer source-of-truth rules over FE copies.
- Pasted logs: run `bob shrink-logs`, answer from the digest, and if needed auto-read `full.log` via `.cursor/evidence/logs/latest.json` - never ask the user for log paths.
- After any create/edit of skills, rules, hooks, slash commands, workflows, or other agent-facing Cursor config: backup and push to `Desktop/cursor-markdowns` (sync script + clear commit message); skip only if the user says not to.
- Bank-facing emails and docs: use only bank-visible API keys/values and agreed mappings; omit Novopay-internal implementation details. Prefer concise clarifications with exact API key name + current value + expected value. When clarifying pre vs post behavior for the bank, reason from committed code only (not uncommitted local changes).
- BKYC PR descriptions (any HDP-7636-tree / TaskAlloc BKYC ticket): follow `.cursor/rules/bkyc-pr-description.mdc` on **all** associated PRs. Minimally include: (1) mermaid **How this fits the whole BKYC solution** in plain-English functionality (no API/permission codes in the chart), (2) **Step in the journey** table with plain-English outcome labels (no jargon like seed/wire/persist without saying what / from where / why) and a **Done** column (`✅` if Jira is Done, blank otherwise), (3) **Decisions / tradeoffs for reviewers**, (4) **Knowledge handoff** with exact codes. Append the journey table to existing PR bodies - never overwrite the rest. When asked to **update the table**, rewrite it on **all** HDP-7636 BKYC PRs (old or new) by Ashutosh (`trusttAshutosh`), Abhishek (`trustt-abhishek`), Harini (`Harini-Trustt`), or Deepankar (`deepankar-np`) - do not skip PRs that already have the table. First-time add for an author: only PRs still missing `Step in the journey`. Example pack: `docs/tdd-runs/HDP-8937/PR_BODY_*.md`.

## Learned Workspace Facts

- Root `Desktop/novopay`; skills `.cursor/skills/`; `novopay.code-workspace`; orchestrator `novopay-orchestrator.mdc`.
- Bob artifacts `docs/tdd-runs/<id>/`. Local DB often `root`/`root`. Tenants `ddp,dsa,kp,ra,rbg,bb`; schema `{tenant}_{service}` (confirm DDL).
- Logs `/apps/applogs/{common|tenant}/`. Branches: backend `ddp-*`, frontend `dsa-*`. Lib via CC `includeBuild`. Flyway common-scripts branch often `ddp-fea-common-scripts` but name can differ per repo - always discover. Prefer main-clone checkout of common-scripts over worktrees for Flyway.
- Cursor personalization backup/restore: `Desktop/cursor-markdowns` (clone + sync restores skills/rules/user-rules across machines).
- BKYC is a product/journey, not a corporate. Local context/docs under `Desktop/BKYC`; service `trustt-platform-task-allocation` on `origin/ddp-fea-bkyc`; permission matrix SoT `trustt-platform-task-allocation/docs/task-allocation/solution-document.md` §11; Jira tree export `docs/tdd-runs/HDP-7636/bkyc-comments-full-latest.md` (`pull_bkyc_jira_comments.py`). DDP task-allocation auth uses `TASK-ALLOC-BKYC-*` (not Excel/DSA `BKYC-UPLD-*`). `Role and Permission Management.xlsx` is the UAM template - add rows per sign-off separately from Flyway. PR template `.cursor/rules/bkyc-pr-description.mdc`. GitHub authors: Ashutosh `trusttAshutosh`, Abhishek `trustt-abhishek`, Harini `Harini-Trustt`, Deepankar `deepankar-np`.
- Daily BKYC Google Chat status at 09:59 AM IST weekdays only (not weekends, not PM): three separate BE / FE (PWA) / APK messages via `docs/tdd-runs/HDP-7636/post_bkyc_be_status_gchat.py` (Windows task `BKYC-BE-Status-GChat`). Prod webhook `GCHAT_WEBHOOK_URL` in `%USERPROFILE%\.cursor\bkyc-jira.env` only (BKYC channel; never Cursor ops or cursor-mobile-relay). Manual test channel: same script `--test` / `run_bkyc_be_status_gchat_test.cmd` using `GCHAT_WEBHOOK_URL_TEST` (does not stop or retarget the weekday job). Each table stops when all its rows are Jira Done. Rolling ETA is recomputed each weekday from remaining work + pace; highlight that date once in the card (do not put "not a committed date" in the Chat disclaimer). Colored group headers mark independent E2E slices, not a full-journey test. Tables cover major journey components, not every ticket. Progress percentages are effort-based (not ticket count); always label them as done vs leftover.
