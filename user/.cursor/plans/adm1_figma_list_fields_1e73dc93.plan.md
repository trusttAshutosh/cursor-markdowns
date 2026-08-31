---
name: ADM1 Figma list fields
overview: "Keep Figma as-is. Extend ADM1 `getTaskList` so `taskDetails` carries the list columns the admin grid already expects, reading them from `task_bkyc.annexure_json` (P10: do not widen `task`). Bind those keys on the webapp. No commit."
todos:
  - id: annexure-helper
    content: Add AnnexureJsonFields reader (CLIENT_NAME, PRODUCT_NAME, DISTRICT, STATE, AREA/LOCALITY/LANDMARK)
    status: completed
  - id: adm1-dto-service
    content: Extend TaskDetailsDto + AdminTaskService batch-load task_bkyc and map fields
    status: completed
  - id: adm1-search
    content: Alias FE searchField ids; EXISTS/LIKE on task_bkyc.annexure_json for client/product/geo
    status: completed
  - id: tests
    content: AnnexureJsonFieldsTest + AdminTaskServiceTest for new keys and search aliases only
    status: completed
  - id: fe-bind
    content: Fix entities.config.ts apiKeys (clientName, productName, district, state, area) and Last Update On label
    status: completed
isProject: false
---

# ADM1 list fields for Figma (no Figma change, no commit)

Recommended Jira structure: **one sub-task under [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930)** (same ADM1 API as [HDP-9003](https://novopay.atlassian.net/browse/HDP-9003)). Additive response fields; existing keys stay.

## Locked

- Figma Unassigned columns stay: Reference Number, Client Name, Product Name, Customer Name, Pincode, District, State, Area, Created On, Last Updated On, Assign.
- Do not add city/district/state columns on `task` (P10). Values already live in `task_bkyc.annexure_json` from ingest ([`ParsedLead`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/plugin/bkyc/ingest/ParsedLead.java), [`README-bkyc-lead-csv.md`](trustt-platform-task-allocation/README-bkyc-lead-csv.md)).
- Do not commit.

## Why BE must change (and a 5-line FE bind)

Figma and the live grid expect **two names** and a **bank product**, not `taskType=BKYC`. CSV already has `CLIENT_NAME` / `PRODUCT_NAME` / `DISTRICT` / `STATE`. Current [`TaskDetailsDto`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/dto/TaskDetailsDto.java) omits them.

Webapp still maps District/State/Area to `updated_on` in [`entities.config.ts`](novopay-platform-webapp/src/app/bkyc-management/kyc/entities.config.ts). If we only ship JSON, the grid still shows `(no data)`. That bind is **not** a Figma change.

```mermaid
flowchart LR
  csv[Lead CSV]
  json[task_bkyc.annexure_json]
  list[getTaskList taskDetails]
  grid[Admin BKYC List]
  csv --> json
  json --> list
  list --> grid
```

## Field contract (additive on `taskDetails`)

| Figma column | JSON key | Source |
| --- | --- | --- |
| Client Name | `clientName` | annexure `CLIENT_NAME` |
| Product Name | `productName` | annexure `PRODUCT_NAME` (blank if missing; do **not** use SMS fallback "Credit Card") |
| District | `district` | annexure `DISTRICT` / `CITY` / `DISTRICT_CITY` via `AnnexureColumn.DISTRICT_CITY` |
| State | `state` | annexure `STATE` / `STATE_NAME` |
| Area | `area` | bank `AREA` / `LOCALITY` / `LANDMARK` if present; else see Area below |
| (keep) | `taskType`, `customerName`, `pincode`, `externalRef`, dates | unchanged |

Existing rows work with no backfill: parse JSON at list time.

## Area (your rule: bank first, else pincode)

1. Read `AREA` / `LOCALITY` / `LANDMARK` from `annexure_json` (unmapped headers are already preserved).
2. TaskAlloc has **no pincode-to-area directory**. A 6-digit pin also does not uniquely mean Figma's "Yadav Nagar".
3. **Do not** call MapMyIndia per list row.
4. If annexure has no area/locality/landmark: `area` is `null` unless an **existing** pincode lookup is found in Actor/masterdata during impl (post-office name only). No new table in this slice.

District/state still come from the CSV (mandatory on Annexure 1).

## Search (FE already sends these)

[`bkyc-list.component.ts`](novopay-platform-webapp/src/app/bkyc-management/kyc/list/bkyc-list.component.ts) `searchField` ids: `referenceNumber`, `clientName`, `productName`, `customerName`, `pincode`, `district`, `state`, `area`.

Today [`AdminTaskListConstants`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/AdminTaskListConstants.java) only allows `customerName`, `externalRef`, `pincode`, `customerMobile`. Unknown field → empty list (`disjunction`).

Map aliases and search annexure-backed fields via `EXISTS` on `task_bkyc` (LIKE on `annexure_json` is enough for page size 10; keys vary by bank header spelling). Map `referenceNumber` → `externalRef`. No new sort API (request DTO has none).

## Implementation (TaskAlloc on `ddp-fea-bkyc`)

1. Small `AnnexureJsonFields` helper next to ingest (same key-resolve idea as [`AssignSmsProductName`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/assignment/sms/AssignSmsProductName.java)). Do not change SMS fallback behaviour.
2. [`AdminTaskService`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/service/AdminTaskService.java): after the page load, `taskBkycDaoService.listByTaskIds` (same batch pattern as [`IntakeResponseService.loadBkyc`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/plugin/bkyc/response/IntakeResponseService.java)); fill new DTO fields. No N+1.
3. Extend [`TaskDetailsDto`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/dto/TaskDetailsDto.java) + search constants + [`AdminTaskListSpecifications`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/dao/AdminTaskListSpecifications.java) subquery join to `TaskBkycEntity`.
4. Tests **only** for classes this change writes: `AnnexureJsonFieldsTest` + extend [`AdminTaskServiceTest`](trustt-platform-task-allocation/src/test/java/com/trustt/taskallocation/task/service/AdminTaskServiceTest.java). No full suite.

## Webapp (bind only)

[`entities.config.ts`](novopay-platform-webapp/src/app/bkyc-management/kyc/entities.config.ts) `singleLeadsListSearchModels`:

- Client Name → `clientName`
- Product Name → `productName` (not `taskType`)
- District / State / Area → `district` / `state` / `area` (not `updated_on`)
- Header `Lat Update On` → `Last Update On` (copy only)

No Figma / layout / column-set change.

## Out of scope

- Figma
- Flyway / widening `task`
- MMI / new pincode master
- Commit / PR unless you ask later
- Assigned-agent name enrich (already null by design)

## Compat

Additive JSON. Old clients ignore new keys. Baseline `origin/ddp-fea-bkyc` (BKYC stack), not a leftover HDP-9003 branch.
