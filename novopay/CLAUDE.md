# Novopay / trustt workspace — operating rules for Claude Code

> Migrated from `.cursor/rules/` + `.cursor/mindmaps/` (2026-08-13). Deep domain knowledge
> lives in memory files at `~/.claude/projects/C--Users-ashutosh-kumar-Desktop-novopay/memory/` (see MEMORY.md index).
> The original `.cursor/` folder is retained as the source of truth for these facts.

## Orientation

- **Workspace root:** `C:\Users\ashutosh.kumar\Desktop\novopay` — a multi-repo mono-workspace, **not** a single git repo. Each
  `novopay-platform-*` / `trustt-platform-*` subfolder is its own git repo.
- **Org:** GitHub `trusttai` (renamed from `khoslalabs`). Push/fetch as user **`deepankar-np`**.
- **Docs convention:** each repo has its own `docs/` (`project-overview.md`, `design-patterns.md`).
  Read `docs/` **before** broad code exploration. Workspace-level `C:\Users\ashutosh.kumar\Desktop\novopay\docs\` holds RCA /
  cross-cutting notes — not a substitute for per-repo docs.
- **Shared tools:** reusable scripts live in `C:\Users\ashutosh.kumar\Desktop\novopay\tools\` — reuse before writing new ones
  (see `ref-workspace-tools` memory).
- **Ticket handoff (Cursor <-> Claude):** when a ticket id is named, read `docs/tdd-runs/<id>/TICKET_RESUME.md` first if it
  exists, and update it (header + session log) at every milestone.

## Working style (think first)

1. Restate intent in one sentence; identify gaps (repo, branch, env, scope, compat).
2. Ask 1–3 focused questions only when the answer changes the approach. Don't ask what you can read
   from open files, the request, or memory.
3. Propose a short plan (2–5 bullets) for non-trivial work, then act. Simple questions → answer directly.
4. Pause and re-confirm on scope creep. Prefer the smallest next step that validates direction.
5. Be concise and direct; prefer code citations over pasted blocks.

## Token / cost guardrails — ask before large work

- **Token-heavy tasks** (many repos, wide search, multi-service builds, long merge chains): describe
  scope and **ask before starting**. Re-confirm if scope grows mid-task.
- **Subagent delegation** (Explore/review/CI agents): say what and why, then **ask** — unless the user
  already requested that delegation this turn. Offer manual commands as the cheaper default.
  - Parallel subagents OK only when work is **independent** (different repos/files, no overlapping writes).
    Never let two agents edit the same repo/file/class — serialize instead.
- **Slow/heavy tasks** (first-run tool downloads, full builds, bulk scripts): give **manual steps first**;
  automate only if the user says "run it" or the command is known-good on this machine.
- **Model selection:** right-size before heavy execution. Simple → fast/Auto; complex (multi-repo,
  architecture, prod debug, security) → a thinking model. Recommend in the plan; flag if the user is on a
  heavy model for simple work. (Detail: `pref-working-style` memory.)

## Machine constraints (Windows) — PowerShell vs git

- This machine has execution-policy / permission constraints. **`powershell -File tools\*.ps1`** and bulk
  multi-repo `.ps1` loops often **fail** — do not default to them.
- **After any PowerShell failure** (permission, execution policy, `cannot spawn`, GCM, empty exit 128):
  **stop** — do not retry the same job with more PowerShell (`Set-Content`, here-strings, `cmd /c git`,
  `Tee-Object`). Switch to **Git Bash** (`C:\Program Files\Git\bin\bash.exe`) + plain `git`, or hand the
  user copy-paste commands.
- Read-only `git -C "<repo>" status|log|diff|fetch` one-liners are fine.
- **Broken git symptom:** `BUG (fork bomb)` means `mingw64\bin\git.exe` is missing (broken Git for
  Windows) — **not** a hook loop. Stop retrying; repair via `winget install --id Git.Git -e` (Admin) and
  verify `mingw64\bin\git.exe` exists.
- Full blocked/working command table: `ref-machine-commands` memory.

## Git workflow & approvals

- **Feature branches must be named `ddp-fea-<short-kebab>`** — never `ddp-fix-*`, `ddp-bug-*`, `fix-*`,
  `feature/*` (GitHub rejects non-`ddp-fea` creations). Base off `origin/ddp-prod` unless told otherwise.
- **Protected branches — always ask before merge/push/checkout-for-merge:**
  `ddp-bkup-qa`, `ddp-bkup-uat`, `ddp-qa`, `ddp-uat`, `ddp-prod`. Read-only inspection needs no ask.
  Approval is **per-action** — not a blanket for follow-on pushes, other repos, or bulk scripts.
- **QA/UAT promotion:** never resolve merges or push directly to `ddp-qa`/`ddp-uat`. Use the bkup mirror:
  feature → `ddp-bkup-qa|uat` (sync env tip first, then merge feature, `gradlew compileJava --no-daemon`,
  then push `origin/ddp-bkup-*`). Jenkins/user promotes bkup → env. (Detail: `pref-git-workflow` memory.)
- **Fix on `ddp-fea-*` first, then merge into `ddp-bkup-*`** — don't fix only on bkup when a
  feature line owns the change. Never cherry-pick onto bkup: first merge latest `origin/ddp-qa|uat` into
  `ddp-bkup-qa|uat`, then merge (pull) the whole feature branch.
- **Backward compatibility:** when changing **existing** behavior (APIs, contracts, config defaults,
  cache/session keys, DB reads, filter/gateway routing, response shape), **ask before coding**:
  "does this need backward compat with production?" Baseline is always **`origin/ddp-prod`**. Skip only for
  greenfield features, docs/tests, or when the user already stated compat.
- **Commits:** conventional subject (`fix(scope):`, `feat(scope):`, `refactor(scope):`). When asked to
  commit, put full technical detail in the **body** (why / what / files / symbols / technical details /
  affected flows / testing / compat), evidence-only against the staged diff. One logical change per commit.
  Never commit without an explicit request.

## Flyway & infra-lib versioning

- **Flyway:** before creating/renaming a migration, resolve the common-script branch
  (`ddp-fea-common-script[s]`), pick the next unused `V<n>__` against that branch (not just the feature
  branch), land on common-script first, then cherry-pick to the feature branch. Per-repo, per-migrations-folder.
- **TaskAlloc exception:** DDL/seeds go only in `novopay-platform-initial-setup/flyway/sql/task-allocation/product/`
  (BKYC on `ddp-fea-bkyc`). Service boot does not auto-migrate (`flyway_auto_update=0`). Never add
  `src/main/resources/sql/migrations/` in `trustt-platform-task-allocation`. Next `V*` against that
  folder **and** QA `ddp_task_allocation.flyway_schema_history` (HDP-8967 `V000021` was reused; columns
  never landed on QA). Detail: `ref-flyway-infra-versioning` + `proj-task-allocation` memory.
- **infra-* modules** (`novopay-platform-lib`): bump `version` in `build.gradle` **once per push cycle**
  when the local version equals `origin`'s. Format `{major}.{minor}.{patch}.{yyyyMMdd}.RELEASE`; changelog
  required for major/minor only. (Detail: `ref-flyway-infra-versioning` memory.)

## SQL

- **Manual `flyway_schema_history` insert:** give exactly ONE one-line statement, never `SET @rank` + `INSERT ... VALUES`: ``INSERT INTO `schema`.`flyway_schema_history` (`installed_rank`,`version`,`description`,`type`,`script`,`checksum`,`installed_by`,`installed_on`,`execution_time`,`success`) SELECT COALESCE(MAX(`installed_rank`),0)+1,'<version>','<description>','SQL','<script>',<checksum>,'manual-ops',NOW(),0,1 FROM `schema`.`flyway_schema_history` WHERE NOT EXISTS (SELECT 1 FROM `schema`.`flyway_schema_history` WHERE `version`='<version>');`` The `WHERE NOT EXISTS` guard is mandatory (only `installed_rank` is the PK, `version` is not unique). Backtick every identifier (CodeAnt quote_identifiers). `installed_by`='manual-ops'. Always remind the user to confirm the checksum matches the Flyway checksum of the built script (a wrong one fails validation at boot). Detail: `feedback-flyway-manual-history-insert` memory.

## Coding standards

- Senior-level, modular, single-responsibility; DRY and KISS; production-ready with edge cases.
- No deprecated methods/libraries. Consider performance & scalability; optimize DB queries (no N+1,
  select only needed columns). Centralized error handling — never swallow exceptions; log with context.
  Validate inputs, handle nulls. Structured logging with correct levels.
- RESTful APIs: resource URLs, correct HTTP methods, stateless, proper status codes. New **v2** APIs use
  Spring `@RestController` + `BaseController` on the service — **not** orchestration XML / JTF v2 packs
  (SoT: `novopay-platform-lib/infra-platform/docs/v2-rest-api-pattern.md`).
- Java stack per repo (mostly Spring Boot, Java 21 baseline / Java 25 on the upgrade branch). Adhere to
  SonarQube rules; Javadoc on public APIs; explain the "why" in comments; keep OpenAPI specs current.
- **Match Deepankar's coding voice** (developer clone): base classes + thin v1/v2 variants, constructor
  injection of platform abstractions (`ICacheClient`, config props), Redis-first for cache/session/rate
  limit, JUnit+Mockito tests riding with behavior changes. Propose a different approach only with a clear
  trade-off. (Detail: `pref-coding-standards` memory.)

## Jira tickets

- Tickets must be **self-contained for developers** — full API `Field | Type | Required | Sample | Notes`
  tables, request/response samples, DDL/seed/status maps in the **description**. Developers don't have the
  workspace `docs/**`; don't ship "see solution-document §X" as the only contract. (Detail: `pref-jira-tickets`.)

## Keep memory current

- After a session where you learn durable facts (architecture, an explicit preference/correction, a
  command that failed or worked, a repeatable workflow), **update the memory files** and MEMORY.md index.
- **Suggest** (don't silently create) a new operating rule when you spot durable, repeated, actionable
  guidance not already covered — wait for approval.
- Don't capture secrets/credentials/customer data, one-off details, or long transcripts.
- **Recurring tasks** are tracked in `C:\Users\ashutosh.kumar\Desktop\novopay\TASKS.md` — notably the weekly *developer-clone
  refresh* (mine Deepankar's recent solo commits, update the `pref-coding-standards` memory). Surface it
  when we're already working in a repo, or when the user asks what's pending.

## Domain deep-dives (memory files)

- **Task-allocation platform** (`trustt-platform-task-allocation`) → `proj-task-allocation` memory
- **HDP-7636 Manipal BKYC** (consent/Jira decisions) → `proj-hdp-7636-bkyc` memory
- **Spring Boot 4 / Java 25 upgrade** (`ddp-fea-spring4-java25-upgrade`) → `proj-spring4-java25-upgrade` memory
