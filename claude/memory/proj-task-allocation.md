---
name: proj-task-allocation
description: "Task-allocation platform architecture decisions — service, domain, assignment, workflow, v2 APIs"
metadata: 
  node_type: memory
  type: project
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:33:11.189Z
---

Field task-allocation platform. SoT: `docs/task-allocation/solution-document.md` (architecture,
diagrams, DDL/seeds §4, §6), `development-plan-outline.md`; clarifications
`docs/task-allocation/clarifications-status.md`. Agent design: Figma node `1174-38810`, PDF
`docs/hdp-7636/source/BKYC-agent-flow-design-2808.pdf`. (Decisions current as of 2026-08-11.)

**Platform (locked):**
- Service **`trustt-platform-task-allocation`** (not product-specific). BKYC is a `task_type` plugin.
- Domain: `task` + `task_type`; `task_assignment` (soft history); `task_status_master` buckets;
  **`TaskStatusService`** is the sole status-transition path (row lock on status/assign); `TaskService`
  for create + query; type side-tables via plugin SPI, e.g. **`bkyc_task`** 1:1 (no eKYC/export columns
  on generic `task`).
- **In-service workflow** engine (definitions + runs + Spring step handlers, DB is SoT) — **no**
  Camunda/Temporal/Zeebe in Phase 1. Async same-JVM sticky run; Orchestration XML = APIs only (not step
  recipes); Kafka = edges, not step choreography; SCHEDULE needs a distributed lock across EC2s; version
  bump to insert steps. `workflow_run` + steps; `change_source` = real handler names.
- **v2 HTTP:** REST controllers per the v2 REST pattern — not orchestration XML / JTF `v2/`.

**Assignment:** modes **PINCODE / DISTANCE / HYBRID** (auto + corporate/manual).
- Auto: FIFO oldest-first, water-fill lowest open count, over all unassigned backlog; **cap 10** (pincode
  only), cron refills multiple times/day. Manual cap **15**. Caps configurable.
- Auto cascade: **pincode first** → still-unassigned → geocode + store customer lat/long → **distance**
  assign (open on [HDP-9252](https://novopay.atlassian.net/browse/HDP-9252) until re-frozen).
- Store `customer_lat`/`customer_lng` (and agent lat/long) on `task`; lazy-geocode via MMI only when
  distance is needed and lat/long null, then **persist** (don't re-geocode every list call).
- Distance via **Actor** (`getEligibleAgentsForTask`): geocode if needed → math shortlist
  (`DistanceCalculationUtil`) → **MapMyIndia road matrix**; if no lat/long for math → **MMI-only**. Same
  pattern as `getNearestBranchList`. TaskAlloc does not call MMI directly or do haversine-only.
- Agent UI: task **cards** show current road **`distance_km`** (device GPS on list → Actor), on-demand
  not background. Agent tabs API **NEW/REVISIT/DONE** (Figma ALL/PENDING conflict [HDP-9036]).
- Dedupe **ARN-only** ([HDP-9250](https://novopay.atlassian.net/browse/HDP-9250)).

**v2 APIs:** AGT1 list, AGT2 detail, AGT3 status, AGT10 submitBkyc; ADM1 list (nested taskList/
taskDetails, webapp envelope), ADM2 eligible (nested agentList/agentDetails), ADM3 assign, ADM4 reprocess
(not Phase-1 UAM), ADM5 workflow-run history, ADM6 getTaskActivityLog, ADM7 upload list (DMS
`downloadDocument` response). Audit = status + assignment only.

**Permissions (Phase 1):** BANK UPLOAD-VIEW + UPLOAD; CORP VIEW + ASSIGN; REPORT REPORT-VIEW (Superset);
Agent `PRDCT-SERVICEREQUEST-BKYC` ([HDP-8937] comment 396433; solution-doc §11).

**Clients:** Admin (tasks + workflow runs); App `digi-distribution-app`; Consents React (unchanged
contracts). **Sequencing:** PH-TA-1 core → 2 assign → 3 workflow → 4 BKYC plugin → 5 clients. SMS only via
`novopay-platform-notifications`. New branches `ddp-fea-*`.

**Flyway:** schema SoT is `novopay-platform-initial-setup/flyway/sql/task-allocation/product/` (BKYC
branch `ddp-fea-bkyc`). TaskAlloc JAR does not migrate. Do not put `V*.sql` under
`trustt-platform-task-allocation/src/main/resources/sql/migrations/`. See [[ref-flyway-infra-versioning]].

BKYC type-1 specialization (consent/Jira locks): [[proj-hdp-7636-bkyc]]. Ticket conventions:
[[pref-jira-tickets]]. Backward-compat before changing shared Actor/Consents: [[pref-git-workflow]].
