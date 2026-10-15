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
- [feedback-pr-common-scripts-link](feedback-pr-common-scripts-link.md) - PR body links the common-scripts commit ONLY when the PR adds/deletes/renames a Flyway script
- [feedback-pr-no-commit-list](feedback-pr-no-commit-list.md) - no Commits/Files-changed section and no Claude Code footer in PR descriptions; GitHub Commits tab covers it
- [feedback-pr-jira-link](feedback-pr-jira-link.md) - every Jira key in a PR description is a full novopay.atlassian.net/browse link, never a bare key
- [feedback-pr-conflict-check](feedback-pr-conflict-check.md) - always prove GitHub-style mergeability BEFORE `gh pr create`; never trust `merge-tree --name-only`; on conflict use bkup and close CONFLICTING PRs
- [pref-qa-bkyc-file-pincodes](pref-qa-bkyc-file-pincodes.md) — files/CSVs must use only Manipal 10 + RISL 166512 agent office pincodes; never invent one
- [feedback-flyway-manual-history-insert](feedback-flyway-manual-history-insert.md) - manual flyway_schema_history insert = ONE guarded INSERT ... SELECT line (WHERE NOT EXISTS, backticks, manual-ops); always remind to verify checksum
- [feedback-bank-uat-bkyc-testdata](feedback-bank-uat-bkyc-testdata.md) - bank UAT BKYC test data comes only from pasted SELECT output; always ask the corporate code with BKYC enabled, default CORP0007

## Reference
- [ref-loc-hibvprd-layout](ref-loc-hibvprd-layout.md) — HDFC LOC HIBVPRD eligibility layout: spec xlsx in Downloads, code offsets, MEMO-LINE5 = savings account
- [ref-github-account](ref-github-account.md) — acts as `trusttAshutosh` on `trusttai` (deepankar-np is legacy)
- [ref-machine-commands](ref-machine-commands.md) — PowerShell blocked patterns → Git Bash / git substitutes; Gradle "Unable to establish loopback connection" fix (JAVA_TOOL_OPTIONS unixdomain.tmpdir); Java-21 gateway vs Java-25 lib init-script compile recipe
- [ref-gateway-common-scripts-hook](ref-gateway-common-scripts-hook.md) - api-gateway pre-commit hook blocks ddp-fea-common-scripts commits (behind prod-master); one-off NOVOPAY_GIT_HOOK_SKIP_PROD_SYNC=1 only with per-commit approval
- [ref-qa-server-access](ref-qa-server-access.md) — QA app-server log paths + paramiko password SSH (key auth refused), QA DB tool works, agent/user/task join hints
- [ref-artifact-sharing](ref-artifact-sharing.md) — share pin must be moved by hand after every republish; artifact versions can't be deleted or listed; BKYC run-sheet URL
- [ref-env-branch-mapping](ref-env-branch-mapping.md) - preprod AND prod both run ddp-prod (dsa-prod for PWA); ddp-preprod branches are stale, never diff against them
- [ref-preprod-db-access](ref-preprod-db-access.md) - preprod read-only DB (no ddp_task_allocation/platform_master grant); batch ServiceRegistry toString bug needs batch restart after new service_master row
- [ref-workspace-tools](ref-workspace-tools.md) — `C:\Users\ashutosh.kumar\Desktop\novopay\tools` script inventory (reuse first)
- [ref-flyway-infra-versioning](ref-flyway-infra-versioning.md) — Flyway common-script + infra-* version bump rules
- [ref-hdfc-salesforce-json-nulls](ref-hdfc-salesforce-json-nulls.md) - Salesforce JSON writes null as "" (use NON_NULL to drop a tag); Salesforce Final DAP test T4 already red on ddp-prod
- [ref-bob-task-allocation-local](ref-bob-task-allocation-local.md) — bob validate-ticket vs local TaskAlloc (port 8022, Actor corporate stub, seed gaps, audit columns); status-matrix ticket HDP-7636-status-matrix
- [ref-qa-task-allocation-api-calls](ref-qa-task-allocation-api-calls.md) - QA curl recipes: api-gateway route (no SSH/login) + 8022/TLS route, flat body, unique x-stan, 429 in snake_case response_status, deployed-bundle diffing; login to corporate map; bankmaker (user 19) IS bank-wide since HDP-8930; QA ddp_BANKMKR UAM drift (HDP-11535)
- [ref-uat-task-allocation-api-calls](ref-uat-task-allocation-api-calls.md) - UAT gateway ddp-uat.trustt.com (enforces usecase perms, 11017), bank user 19 on role ddp_maker01, entitled corporates 43774/31981/31985 with users 44462/44248/32500 and test tasks
- [ref-windows-seqrite-file-hang](ref-windows-seqrite-file-hang.md) — Gradle clean/compile and rm hangs on ATSLAP-43 = Seqrite minifilter, not Gradle; jstack + HandleProbe + Bulk.java
- [ref-task-allocation-mmi-geocode-validation](ref-task-allocation-mmi-geocode-validation.md) - validate HDP-11732 customer geocoding on QA/UAT: deployed-jar check, trigger via getAgentTaskList, UAT gRPC-timeout MDC loss makes it fail open (check common log)

## Project / domain
- [proj-novopay-overview](proj-novopay-overview.md) — multi-repo map, docs convention, platforms
- [proj-task-allocation](proj-task-allocation.md) — task-allocation platform architecture decisions
- [proj-hdp-7636-bkyc](proj-hdp-7636-bkyc.md) — Manipal BKYC consent/OTP/Jira locked decisions
- [proj-hdp-7636-bkyc-prod-pr-pack](proj-hdp-7636-bkyc-prod-pr-pack.md) - 10 draft [PROD] BKYC PRs to ddp-prod (2026-10-06): numbers, conflicts, api-gateway V4000032 rename blocker, next steps
- [proj-hdp-8768-cc-app-status](proj-hdp-8768-cc-app-status.md) - Blostem CC app status API: QA PRs cc #2504, gateway #2522, initial-setup #5557 merged+deployed 2026-10-14; QA external gateway application.properties lacks skip-list entry (ops fix pending)
- [proj-bkyc-entitlement-by-corporate-code](proj-bkyc-entitlement-by-corporate-code.md) - BKYC entitlement by admin-portal corporate code: new codes config key, Actor getCorporatesByCodes, TaskAlloc BkycEntitledCorporateService, masterdata V4000878; 9 PRs open 2026-10-07 (TA 118-120, actor 18591 + 18595/18596 via bkup, masterdata 8456-8458)
- [proj-hdp-7636-deferred-qa-tests](proj-hdp-7636-deferred-qa-tests.md) — T17 + PACK-114 deferred for QA DB write access; runbooks, Redis flush, and the final config values
- [proj-spring4-java25-upgrade](proj-spring4-java25-upgrade.md) — Spring Boot 4 / Java 25 / Gradle 9 fleet upgrade
- [proj-hdp-11796-firestore-hardening](proj-hdp-11796-firestore-hardening.md) - Firestore keepalive/timeout/retry fix: 6 PRs open (lib #6785/#6786, consents #3268/#3269, actor #18539/#18540), branch bases, prod-master moved, prod heads in .wt-11796-pm, compat rules
- [PR conflict check](feedback-pr-conflict-check.md) - check conflicts GitHub-style (each merge base) before raising QA/UAT PRs; on conflict raise from ddp-bkup-*
