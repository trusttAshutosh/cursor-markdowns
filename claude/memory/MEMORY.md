# Memory index

Migrated from `C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\rules` + `.cursor\mindmaps` (2026-08-13). Always-on operating rules
live in `C:\Users\ashutosh.kumar\Desktop\novopay\CLAUDE.md`; these files hold recalled-by-relevance detail.

## User & preferences
- [user-ashutosh](user-ashutosh.md) — user is Ashutosh Kumar (NOT Deepankar); git Ashutosh, gh trusttAshutosh; Atlassian connector is Deepankar's
- [pref-working-style](pref-working-style.md) — think-first, ask before token-heavy/subagent, manual steps, model right-sizing
- [pref-git-workflow](pref-git-workflow.md) — ddp-fea naming, protected-branch approval, bkup promotion, backward compat
- [pref-coding-standards](pref-coding-standards.md) — Java/Spring standards + Deepankar's developer clone + v2 REST
- [pref-jira-tickets](pref-jira-tickets.md) — tickets self-contained (full API/DDL/samples in description)
- [pref-no-em-dashes](pref-no-em-dashes.md) - never use em/en dashes, plain hyphen only, in replies and every file, PR/Jira comment and commit message written
- [pref-end-with-summary](pref-end-with-summary.md) - always close replies with a short summary section
- [pref-thermo-nuclear-review](pref-thermo-nuclear-review.md) — `/thermo-nuclear-code-review` = user's strict structure-first review skill at `~/.claude/skills/`; always run via Skill tool
- [feedback-verify-identity-before-external-updates](feedback-verify-identity-before-external-updates.md) — NEVER use the Jira/Atlassian connector (acts as Deepankar); Jira via browser login; ASK username confirmation before any Jira/GitHub write

- [feedback-bkyc-pr-template](feedback-bkyc-pr-template.md) - BKYC PR bodies must follow `.cursor/rules/bkyc-pr-description.mdc` (7 sections, mermaid, journey table with live Jira Done); not the style of recent PRs
- [pref-qa-bkyc-file-pincodes](pref-qa-bkyc-file-pincodes.md) — files/CSVs must use only Manipal 10 + RISL 166512 agent office pincodes; never invent one
- [feedback-bank-uat-bkyc-testdata](feedback-bank-uat-bkyc-testdata.md) - bank UAT BKYC test data comes only from pasted SELECT output; always ask the corporate code with BKYC enabled, default CORP0007

## Reference
- [ref-loc-hibvprd-layout](ref-loc-hibvprd-layout.md) — HDFC LOC HIBVPRD eligibility layout: spec xlsx in Downloads, code offsets, MEMO-LINE5 = savings account
- [ref-github-account](ref-github-account.md) — acts as `trusttAshutosh` on `trusttai` (deepankar-np is legacy)
- [ref-machine-commands](ref-machine-commands.md) — PowerShell blocked patterns → Git Bash / git substitutes; Gradle "Unable to establish loopback connection" fix (JAVA_TOOL_OPTIONS unixdomain.tmpdir); Java-21 gateway vs Java-25 lib init-script compile recipe
- [ref-qa-server-access](ref-qa-server-access.md) — QA app-server log paths + paramiko password SSH (key auth refused), QA DB tool works, agent/user/task join hints
- [ref-artifact-sharing](ref-artifact-sharing.md) — share pin must be moved by hand after every republish; artifact versions can't be deleted or listed; BKYC run-sheet URL
- [ref-workspace-tools](ref-workspace-tools.md) — `C:\Users\ashutosh.kumar\Desktop\novopay\tools` script inventory (reuse first)
- [ref-flyway-infra-versioning](ref-flyway-infra-versioning.md) — Flyway common-script + infra-* version bump rules
- [ref-bob-task-allocation-local](ref-bob-task-allocation-local.md) — bob validate-ticket vs local TaskAlloc (port 8022, Actor corporate stub, seed gaps, audit columns); status-matrix ticket HDP-7636-status-matrix
- [ref-qa-task-allocation-api-calls](ref-qa-task-allocation-api-calls.md) - QA curl recipes: api-gateway route (no SSH/login) + 8022/TLS route, flat body, unique x-stan, 429 in snake_case response_status, deployed-bundle diffing; login to corporate map; bankmaker (user 19) IS bank-wide since HDP-8930; QA ddp_BANKMKR UAM drift (HDP-11535)
- [ref-uat-task-allocation-api-calls](ref-uat-task-allocation-api-calls.md) - UAT gateway ddp-uat.trustt.com (enforces usecase perms, 11017), bank user 19 on role ddp_maker01, entitled corporates 43774/31981/31985 with users 44462/44248/32500 and test tasks
- [ref-windows-seqrite-file-hang](ref-windows-seqrite-file-hang.md) — Gradle clean/compile and rm hangs on ATSLAP-43 = Seqrite minifilter, not Gradle; jstack + HandleProbe + Bulk.java
- [ref-task-allocation-mmi-geocode-validation](ref-task-allocation-mmi-geocode-validation.md) - validate HDP-11732 customer geocoding on QA/UAT: deployed-jar check, trigger via getAgentTaskList, UAT gRPC-timeout MDC loss makes it fail open (check common log)

## Project / domain
- [proj-novopay-overview](proj-novopay-overview.md) — multi-repo map, docs convention, platforms
- [proj-task-allocation](proj-task-allocation.md) — task-allocation platform architecture decisions
- [proj-hdp-7636-bkyc](proj-hdp-7636-bkyc.md) — Manipal BKYC consent/OTP/Jira locked decisions
- [proj-hdp-7636-deferred-qa-tests](proj-hdp-7636-deferred-qa-tests.md) — T17 + PACK-114 deferred for QA DB write access; runbooks, Redis flush, and the final config values
- [proj-spring4-java25-upgrade](proj-spring4-java25-upgrade.md) — Spring Boot 4 / Java 25 / Gradle 9 fleet upgrade
