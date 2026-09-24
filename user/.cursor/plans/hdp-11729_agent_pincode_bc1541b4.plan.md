---
name: HDP-11729 agent pincode
overview: Expose the assigned agent's office pincode on admin read APIs (and View History), without mutating customer `task.pincode`. Extend Actor `getAgentsByIds`, enrich ADM1/ADM6, then FE display.
todos:
  - id: actor-agents-by-ids-pincode
    content: "Actor: return OFFICE pincode on getAgentsByIds + unit test"
    status: completed
  - id: taskalloc-enrich-assigned-pin
    content: "TaskAlloc: AgentDirectoryEntry + TaskDetailsDto.assignedAgentPincode + ADM1/ADM6 mapping + docs/tests"
    status: completed
  - id: webapp-view-history-pin
    content: "Webapp: View History Agent Pincode + Assigned-to display; keep customer Pincode column"
    status: cancelled
  - id: qa-verify-scenarios
    content: Prove assign/reassign/unassign View History + list customer pin unchanged
    status: cancelled
isProject: false
---

# HDP-11729 - Show assigned agent office pincode

## Locked interpretation

- **Bug as written vs SoT:** List `Pincode` is **customer/lead** `task.pincode`. ADM3 assign/reassign correctly does **not** rewrite it.
- **Fix we will build:** Display the **current assigned agent’s office pincode** (Actor OFFICE address) after assign/reassign. Do **not** change `task.pincode`, auto-assign matching, map pin, or ADM2 prefill.
- **ASSUMPTION (UI):** Primary surface = **View History** header (ticket steps say View/View History). Keep list column `Pincode` = customer. Optionally show agent pin under **Assigned to** on Assigned / To Be Reassigned tabs (same API field) so the list also reflects the new agent after refresh.

## Current gap

```mermaid
sequenceDiagram
  participant FE as AdminWebapp
  participant TA as TaskAlloc
  participant Actor as Actor
  FE->>TA: getTaskList / getTaskActivityLog
  TA->>Actor: getAgentsByIds
  Actor-->>TA: agentId code name only
  TA-->>FE: assignedAgentCode Name no pincode
```

- [`AgentDirectoryEntry`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/integration/actor/dto/AgentDirectoryEntry.java): `agentId`, `agentCode`, `agentName` only.
- Actor [`GetAgentsByIdsResponse`](novopay-platform-actor/src/main/java/in/novopay/actor/agent/eligible/dto/GetAgentsByIdsResponse.java) / DAO rows: no office pincode today.
- Eligible agents already return `pincode` (office match) - reuse that source for by-ids.

## Implementation

### 1. Actor (`ddp-fea-bkyc`) - extend `getAgentsByIds`

- Add `pincode` (nullable String) to the directory row DTO returned by [`GetAgentsByIdsService`](novopay-platform-actor/src/main/java/in/novopay/actor/agent/eligible/GetAgentsByIdsService.java) / search DAO (same OFFICE address pincode used by eligible-agents PINCODE mode).
- Unit test on `GetAgentsByIdsServiceTest` only (`--tests` that class).
- Fail-open: missing address → `pincode` null (same as code/name miss today).

### 2. TaskAlloc (`ddp-fea-bkyc`) - enrich admin reads

- Extend [`AgentDirectoryEntry`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/integration/actor/dto/AgentDirectoryEntry.java) + parse path in [`ActorAgentsByIdsClient`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/integration/actor/ActorAgentsByIdsClient.java).
- Add `assignedAgentPincode` to [`TaskDetailsDto`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/dto/TaskDetailsDto.java); map in [`AdminTaskService`](trustt-platform-task-allocation/src/main/java/com/trustt/taskallocation/task/service/AdminTaskService.java) from the existing `getAgentsByIds` batch (null when unassigned / Actor miss).
- ADM6 View History header: include agent pincode alongside name/code in the activity-log response envelope FE already maps in [`bkyc-list.component.ts`](novopay-platform-webapp/src/app/bkyc-management/kyc/list/bkyc-list/bkyc-list.component.ts) (`agent_details`). Prefer enriching from the same Actor lookup used for list assigned agent (or reuse list row fields when opening history).
- Docs: one-line note in `FE_Integration_Doc_getTaskList.md` / solution ADM1 field table - customer `pincode` unchanged; new `assignedAgentPincode`.
- Tests: extend existing AdminTask / AgentsByIds client tests only.

### 3. Admin webapp (`ddp-fea-bkyc`)

- View History: add **Agent Pincode** in the header block of [`view-history.component.html`](novopay-platform-webapp/src/app/components/wizards/form-wizards/history-popup/view-history/view-history.component.html) when `isBkycRequest` (bind from `history.agent_details`).
- Wire `assignedAgentPincode` in `viewActivityLog` payload builder in `bkyc-list.component.ts`.
- Assigned to column (HDP-11731): append office pin in display when present, e.g. `Name (CODE) · 518302` - no new column; do **not** overwrite customer `Pincode` column.
- Assign modal: keep seeding from **customer** `taskDetails.pincode` (eligibility filter). No ADM3 contract change.

### 4. Out of scope

- No Flyway / no `task.pincode` mutation on ASSIGN/REASSIGN.
- No change to ADM3 request body.
- No APK / agent APIs.
- No gateway mapping unless a new public field needs OpenAPI only (internal TaskAlloc v2 already).

## Verify (QA)

1. Unassigned lead → Assign agent A (office pin P1) → View History shows Agent Pincode **P1**; list **Pincode** still customer pin.
2. Reassign to agent B (office pin P2 ≠ P1) → refresh list + View History → Agent Pincode **P2**; customer **Pincode** unchanged.
3. Unassign → Agent Pincode empty/hidden; customer pin unchanged.
4. Actor miss → Agent Pincode blank; no 500.

## Repos / branch

Same line: `ddp-fea-bkyc` on Actor, TaskAlloc, webapp (order: Actor → TaskAlloc → webapp).
