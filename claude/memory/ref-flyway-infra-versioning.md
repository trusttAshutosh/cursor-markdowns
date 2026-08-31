---
name: ref-flyway-infra-versioning
description: "Flyway migration versioning via common-script branch, and infra-* module version bump rules"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:32:17.539Z
---

### Flyway migration versions

Before creating/renaming a Flyway migration:
1. Resolve the org's common-script integration branch: `ddp-fea-common-script` or
   `ddp-fea-common-scripts` (verify with `git branch -a`).
2. Lock the next version against the **common branch**, not just the feature branch:
   `git ls-tree -r --name-only origin/<common-branch> -- <migrations-dir>` (e.g.
   `src/main/resources/sql/migrations/ddp/`). Pick the next unused `V<n>__`; never reuse a version that
   already exists on common, even if your feature branch lacks that file.
3. Land new scripts on the **common-script branch first** (reserves the version repo-wide), then
   cherry-pick/rebase onto the feature branch so the same filename/version is shared.
4. Per-repo, per-migrations-subfolder (`ddp/`, `product/`, tenant packs) - each microservice has its own
   Flyway history.

### TaskAlloc is not in the service repo

`trustt-platform-task-allocation` has `flyway_auto_update=0`. QA/UAT DDL is applied by FlywayMigrator
from **`novopay-platform-initial-setup/flyway/sql/task-allocation/product/`** (`localhost-task-allocation.sh`).

- Author new `V*.sql` there only (BKYC stack is on initial-setup `ddp-fea-bkyc`; org
  `ddp-fea-common-scripts` often has no `task-allocation/` folder).
- Do **not** add `src/main/resources/sql/migrations/` in TaskAlloc (removed; do not bring back).
- Next unused `V*` = max of that product folder **and** QA `ddp_task_allocation.flyway_schema_history`.
  HDP-8967 put journey-SMS ALTER in TaskAlloc as `V000021`; QA already had `V000021` as doc-upload
  retry, so columns never applied and `getTaskList` failed with `Unknown column sms_appointment_pending`.

### infra-* module version bump (`novopay-platform-lib`)

Full policy: `novopay-platform-lib/docs/infra-module-versioning.md`. Bump a module's `version` in its
`build.gradle` **once per push cycle**:
- Bump when the local `version` **equals** `origin/<branch>`'s version (first publishable change since
  the pushed version). Compare via `git show origin/<branch>:<module>/build.gradle`.
- Do **not** bump on further local commits while local version is already ahead of origin (one jar
  identity until pushed).
- Format: `{major}.{minor}.{patch}.{yyyyMMdd}.RELEASE` (4th number = IST date). Example jar:
  `infra-jtf-0.0.10.20260715.RELEASE-plain.jar`.
- major (breaking, reset minor/patch) and minor (feature, reset patch) require a `<module>/docs/changelog.md`
  entry; patch (hotfix) does not. Mention the expected jar version in the commit/handoff.

Related: [[pref-git-workflow]], [[proj-spring4-java25-upgrade]].
