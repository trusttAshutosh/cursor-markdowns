# Cursor user rules snapshot

Re-add these in **Cursor Settings -> Rules -> User rules** after a new laptop setup.
Cloud sync may restore them automatically; this file is the offline backup.

---

## Paste logs as-is - agent shrinks

Paste logs directly into chat as you do today. Agent runs `bob shrink-logs`, answers from the digest, and if that is not enough automatically reads the matching full.log (via `.cursor/evidence/logs/latest.json`) - you never need to know or type any path.

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
