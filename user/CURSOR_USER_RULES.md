# Cursor user rules snapshot

Re-add these in **Cursor Settings -> Rules -> User rules** after a new laptop setup.
Cloud sync may restore them automatically; this file is the offline backup.

---

## MarkItDown - auto-convert attachments when MCP on

MarkItDown (PDF/Office to Markdown) - optional MCP, auto-convert when enabled.

- Keep MCP server `markitdown` disabled in Cursor Settings until a doc-heavy chat.
- When MCP is **enabled** and user attaches or links PDF/DOCX/XLSX/PPTX (or .doc/.xls/.ppt): **always** call `convert_to_markdown` first, then answer from Markdown - do not ingest raw PDF/binary.
- Direct file URLs (`https://.../spec.pdf`): convert first when MCP enabled.
- MCP disabled + local attachment: CLI `python C:/Users/ashutosh.kumar/.cursor/tools/markitdown-shim/cli.py "<path>"` first.
- Also on `/markitdown` or explicit convert request.
- Never for applogs (`bob shrink-logs`), code, Jira/Confluence, or RCA greps.

---

## Caveman optional lite - off for RCA/Plan

Caveman is optional, not default.

- Enable only when user says `/caveman`, `/caveman lite`, "caveman mode", or "use caveman". Default intensity: lite (no filler/hedging; keep articles + full sentences). Do not use full/ultra unless explicitly asked.
- Stay OFF for: RCA / incident analysis / root-cause / timelines; Plan gate (`/ticket-kickoff`); `/rca-logs`; bank clarifications; security/irreversible warnings. Use normal complete prose (incident-analysis format when RCA).
- Do not auto-enable from "be brief", token efficiency, or memory-budget alone. Stop with "stop caveman", "normal mode", or `/caveman off`.
- Code, commits, PRs, docs, Jira text: always normal prose.

---

## No auto Continual Learning on stop

Do not auto-run Continual Learning after each prompt or agent stop. Ignore any stop-hook follow-up that asks to run the `continual-learning` skill or `agents-memory-updater` unless the user explicitly requests memory mining / AGENTS.md updates. The Continual Learning plugin stop hook is disabled (empty hooks.json); do not re-enable it without being asked.

---

## Paste logs as-is - agent shrinks

Paste logs directly into chat as you do today. Agent runs `bob shrink-logs`, answers from the digest, and if that is not enough automatically reads the matching full.log (via `.cursor/evidence/logs/latest.json`) - you never need to know or type any path.

---

## Backup skills/rules to cursor-markdowns

After any create/edit of Cursor skills, rules, slash commands, hooks, WORKFLOWS, user rules, or other agent-facing config (`~/.cursor`, `novopay/.cursor`, service `.cursor` overlays): before finishing the task, backup and push to cursor-markdowns.

Steps (agent-owned):
1. `cd Desktop/cursor-markdowns && python sync-cursor-backup.py`
2. `git add` relevant paths; commit with clear message (what + why)
3. `git push origin main`

Skip only if user explicitly says not to commit/push. Update `user/CURSOR_USER_RULES.md` when Cursor Settings user rules change.

---

## SQL FQ names + server grep only

SQL: Always use fully qualified schema_name.table_name. Prefer pasted prod DDL under novopay/.cursor/memory/prod-ddl/ when present. Before sharing queries, check for env-specific schema drift (QA vs UAT vs prod / recent Flyway) and explicitly call out columns or tables that may not exist on the target env.

Grep: When asked for log search commands, always share grep (never rg). Always target server paths under /apps/applogs/common and /apps/applogs/<tenant> with live files like {service}-{tenant}.log; include rotated/archived via *.log* or date globs; use zgrep for .gz. Never default to local workspace or SERVER_LOGS paths unless the user is explicitly on local Bob.

---

## Issue reports: RCA and timeline before fix

When a bug or production issue is reported, do not jump straight to implementing a fix.

First deliver:
1. RCA (root cause analysis) - what is failing, where in the flow, and why.
2. Timeline - when it last worked, when it broke or became visible, with commit link + author + date on each relevant change.
3. Explicit verdict on whether this started happening recently (yes/no, and since which deploy/commit).

Use the incident-analysis format when appropriate (phased history, mermaid flow, working-vs-broken table). Only propose or implement a fix after the user has the RCA/timeline (or explicitly asks to skip straight to fix).

---

## Test fixes: prefer ddp-qa/ddp-uat, never prod classes

When fixing unit/integration tests (user-asked or agent-initiated):

1. First check whether the failing test is already fixed on remote `origin/ddp-qa` or `origin/ddp-uat` (fetch if needed; compare the same test class/method).
2. If either branch has the fix, port/reuse that test change instead of inventing a new one - this avoids merge conflicts in test classes when branches are merged later.
3. Only write a fix from scratch if neither `ddp-qa` nor `ddp-uat` has it.
4. When fixing from scratch, update tests only - do not change production/original classes unless production code is genuinely wrong.

---

## Unit test runs: CC suite only; elsewhere new tests only

Never run the preexisting unit/integration suite for any repo other than CC (`novopay-platform-creditcard-management` / `*-ddp-uat` clone).

- **CC:** `gradle test` / existing tests are allowed when proving a CC change.
- **Every other repo** (task-allocation, Actor, lib, gateway, notifications, …): run **only the test class(es) written in this change** (`./gradlew test --tests com.example.NewTest`). Do not add sibling/preexisting `--tests` "for safety". Do not run unfiltered `gradle test`.
- Compile (`compileJava`) without tests is fine. If includeBuild/JDK cannot run even the new class, skip and say so - do not expand to other test classes.
