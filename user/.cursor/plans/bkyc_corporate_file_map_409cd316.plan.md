---
name: BKYC corporate file map
overview: "Plan only (no code): implement corporate-to-file mapping under assumed Yes on HDP-8930 S.No. 12 / 11 / 22 plus Deepankar permission lock 401415 - upload stamps Actor corporate on task_file and leads; assign/jobs use permission + login corporate, not Manipal-only config."
todos:
  - id: ddl-task-file-corporate
    content: "initial-setup Flyway: task_file.corporate_id + TaskFileEntity"
    status: completed
  - id: api-entitled-corporates
    content: "TaskAlloc v2 list API: corporates with BKYC ASSIGN permission"
    status: completed
  - id: upload-ingest-close
    content: Require corporateId on upload; ingest/close from task_file; history fields/filter
    status: completed
  - id: admin-jobs-scope
    content: Admin lists = login corporate; refill/SMS = all entitled corporates
    status: completed
  - id: fe-upload-page
    content: "webapp upload-bkyc-list: dropdown + FormData + history column/filter"
    status: completed
  - id: ops-uam-map
    content: "Env UAM: map ASSIGN onto BLS/Manipal roles; no new permission codes"
    status: completed
isProject: false
---

# BKYC corporate-to-file mapping plan

## Assumptions (treat as locked until product says otherwise)

- **`12` Yes:** corporate comes from **upload-screen dropdown only**. CSV `CLIENT_NAME` stays annexure display/search; does **not** set `task.corporate_id`.
- **`11` Yes:** one upload file = exactly one corporate; all leads from that file get that corporate.
- **`22` Yes:** close file does **not** close an ARN that belongs to a different corporate than the one selected on close upload.
- **Deepankar `401415`:** no masterdata BKYC corporate allowlist. Entitled corporates = Actor corporates whose roles already have **BKYC assignment permission**. Assign screens = **login corporate** (no picker). Refill / SMS loop **every** assignment-permission corporate (supersedes Manipal-only `BkycAssignConfig` scope).

If product reverts differently, adjust only the disagreed S.No. rows; do not rebuild the whole design.

## Product rules (Phase 1)

```mermaid
sequenceDiagram
  participant Bank as BankMaker
  participant FE as AdminWebapp
  participant TA as TaskAllocation
  participant Actor as Actor_UAM
  participant DB as task_file_task

  Bank->>FE: Open upload
  FE->>TA: List entitled corporates
  TA->>Actor: Corporates with ASSIGN permission
  Actor-->>TA: id plus name
  TA-->>FE: Dropdown options
  Bank->>FE: Select corporate plus CSV
  FE->>TA: uploadTaskLeadFile corporateId file
  TA->>DB: task_file.corporate_id plus ingest tasks
  Note over TA,DB: Close upload same corporateId; ARN match scoped
```

| Rule | Behaviour |
| --- | --- |
| Upload | Required `corporateId` (Actor `corporate.id`). Reject missing / not entitled. |
| File | Persist on `task_file`; immutable after upload. |
| Leads | Every accepted row uses **file** corporate (not config, not CSV). |
| History | Show Actor corporate name; optional filter by same entitled list. Legacy rows: blank name. |
| Close | Same required corporate; match ARN **only** within that corporate; mismatch = not found / invalid row. |
| Assign UI | No new FE; BE scopes lists/actions to **login corporate** if it has ASSIGN permission. |
| Jobs | Auto-assign for file corporate; scheduled refill/SMS for each entitled corporate. |
| Permissions | Existing UAM codes only; ops map ASSIGN onto BLS/Manipal roles per env. No new menus. |

## Repos and tickets

| Repo | Branch line | Work |
| --- | --- | --- |
| [novopay-platform-initial-setup](novopay-platform-initial-setup/flyway/sql/task-allocation/product/) | `ddp-fea-bkyc` | DDL `task_file.corporate_id` only (separate seed file if any seed needed - prefer none) |
| [trustt-platform-task-allocation](trustt-platform-task-allocation) | `ddp-fea-bkyc` | Upload, ingest, close, list API, admin scope, jobs |
| [novopay-platform-webapp](novopay-platform-webapp) | active admin `ddp-*` BKYC line | Upload page dropdown + history only |
| Authorization / Actor | usually **no code** | Ops/UAM map existing `TASK-ALLOC-BKYC-*` onto BLS/Manipal roles; reuse Actor name/id APIs |

Story: [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930). Implement under BE [HDP-9694](https://novopay.atlassian.net/browse/HDP-9694) (reopen/extend) and FE [HDP-9695](https://novopay.atlassian.net/browse/HDP-9695). Assign scope + refill/SMS permission loop is part of this lock (touches HDP-8953 / HDP-8956 behaviour), not a new product screen.

## 1. Schema (initial-setup)

- Next unused `V*` under `flyway/sql/task-allocation/product/` (check folder **and** QA `ddp_task_allocation.flyway_schema_history`).
- `ALTER TABLE \`task_file\` ADD \`corporate_id\` BIGINT NULL` + index; backtick all identifiers.
- Nullable for legacy uploads; new uploads always set it.
- Entity: [TaskFileEntity.java](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/entity/TaskFileEntity.java) - today no corporate column ([V000011](novopay-platform-initial-setup/flyway/sql/task-allocation/product/V000011__task_file_table.sql)).

## 2. Backend - TaskAlloc

### 2a. Entitled-corporate list API (new v2)

- New `@RestController` endpoint (same v2 + `BaseController` pattern): returns `{ corporateId, corporateName }` for corporates that have **BKYC assignment permission** on a role (Actor corporate.id + display name).
- FE must not hardcode BLS/Manipal.
- Fail closed: empty list => bank cannot upload until UAM is mapped.
- Concrete discovery: TaskAlloc integrates with existing Actor/UAM reads (same identity model as visit owner = `corporate.id`); do **not** invent a masterdata config list.

### 2b. Upload API

- Extend [TaskFileUploadController](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/upload/controller/TaskFileUploadController.java) / [TaskFileUploadService.accept](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/upload/service/TaskFileUploadService.java): require multipart `corporateId`.
- Validate id is in entitled set; reject otherwise (no silent Manipal default).
- Persist on `task_file` before queueing workflow.
- Lead and close uploads share the same rule.
- Checksum duplicate stays **global** (unchanged).

### 2c. Ingest

- [BkycIngestService](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/plugin/bkyc/service/) / [BkycRowWriter](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/plugin/bkyc/service/BkycRowWriter.java): take corporate from **`task_file.corporate_id`**, not `BkycAssignConfig.getCorporateId()`.
- Do not map `CLIENT_NAME` to corporate.
- Auto-assign after ingest: agents for **that** corporate only (permission-eligible).

### 2d. Close

- [BkycCloseService](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/plugin/bkyc/service/BkycCloseService.java): resolve corporate from close `task_file`; ARN lookup **filtered by `task.corporate_id`**. Cross-corporate ARN => treat as not found / invalid for this file (assumed Yes on `22`).

### 2e. Upload history API

- [TaskFileListService](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/upload/service/TaskFileListService.java) / summary DTO: add corporate id + Actor name; support optional corporate filter.
- Null corporate_id => blank name (legacy).

### 2f. Admin assign / activity (no FE picker)

- Replace `BkycAssignConfig` single-id scope in [AdminTaskService](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/service/AdminTaskService.java) and [AdminTaskActivityService](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/service/AdminTaskActivityService.java):
  - Resolve login corporate from `X-User-Id` → employee → `corporate_id` (same Actor corporate.id model as agent visit owner).
  - Require that corporate has BKYC ASSIGN permission; else empty/fail closed.
- No request-body corporate picker.

### 2g. Scheduled refill / SMS

- [BkycWorkflowCorporateIdResolver](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/plugin/bkyc/handler/BkycWorkflowCorporateIdResolver.java) and refill/SMS handlers: stop Manipal-only config fallback for scheduled runs; loop **entitled** corporates (assignment permission).
- File-triggered runs keep corporate from file / task context.
- Document that this supersedes prior HDP-8953 / HDP-8956 “single configured corporate” locks.

### 2h. Config sunset for scope

- Keep `trustt.taskallocation.bkyc.corporate.id` unused for new upload/assign/job scope (or remove callers only). Do **not** add a new masterdata multi-corporate list.

## 3. Frontend - admin webapp only

Touch [upload-bkyc-list](novopay-platform-webapp/src/app/bkyc-management/kyc/list/upload-bkyc-list/) (component already has corporate column / dropdown stubs).

| Screen | Change |
| --- | --- |
| Lead upload | Required corporate dropdown from entitled-list API; block submit if empty |
| Close upload | Same |
| FormData | Append `corporateId` with file + `fileType` |
| History grid | Corporate name column (from list API) |
| History filter | Optional corporate filter (same options) |
| Download / date / name / status | Unchanged |
| Assign / agent APK / PWA / reports | **No** new corporate UI in this story |

## 4. Out of scope

- Mapping corporate from CSV `CLIENT_NAME`
- New permission codes or menus
- Bank maker assign / corporate user upload
- Backfill rewrite of old `task_file` rows
- Hardcoded BLS/Manipal in BE or FE
- PWA/APK corporate picker

## 5. Build order

1. Flyway `task_file.corporate_id` + entity
2. Entitled-corporate list API
3. Upload accept + history list fields/filter
4. Ingest from file corporate + close ARN scope
5. Admin login-corporate scope
6. Refill/SMS multi-corporate loop
7. FE upload page wire-up
8. Unit tests only for **new/changed** classes (`--tests`); compile TaskAlloc; FE manual on upload page
9. Ops: map ASSIGN on BLS + Manipal roles on target env before bank UAT

## 6. Verify (after build - not now)

- Upload without corporate / with non-entitled id → reject
- BLS upload → tasks only on BLS login assign list; Manipal login does not see them
- Close ARN under other corporate → not closed
- Duplicate checksum still rejects across corporates
- History shows name; filter works; legacy blank
- Refill runs for both permission-mapped corporates
- Assign / APK screens: no new corporate control

## 7. Contingency

| If product changes | Adjust |
| --- | --- |
| `12` = use `CLIENT_NAME` | Add CSV→Actor map; dropdown may become validation-only or removed; close still needs screen corporate |
| `11` = allow mix | Per-row corporate from CSV; reject entitlement failures per row |
| `22` = close anyway | Drop corporate filter on ARN close match |

No code in this chat until Plan gate approval and product reply is treated as Yes (or you explicitly say proceed on assumption).
