---
name: proj-novopay-overview
description: "Novopay workspace map — multi-repo layout, docs convention, key platforms and where knowledge lives"
metadata: 
  node_type: memory
  type: project
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:32:47.578Z
---

`C:\Users\ashutosh.kumar\Desktop\novopay` is a multi-repo workspace (not one git repo). Each `novopay-platform-*` / `trustt-platform-*`
subfolder is its own git repo on the `trusttai` GitHub org (see [[ref-github-account]]).

**Docs convention:** read a repo's own `docs/` (`project-overview.md`, `design-patterns.md`, plus
`<module>/docs/` for lib submodules) **before** broad code exploration. When you explore to answer a
non-trivial question and those files are missing/stale, create or update them (Mermaid diagrams + code
references; bump `Updated:`). Workspace-level `C:\Users\ashutosh.kumar\Desktop\novopay\docs\` = RCA / cross-cutting notes only.
Repos known to have docs: `api-gateway`, `infra-platform` (`docs/v2-rest-api-pattern.md`), `infra-cache`,
`infra-message-broker`, `digi-distribution-app`, `infra-ops-alerts`.

**infra-ops-alerts:** Google Chat ops alerts only (not customer notify) — `util-platform` API project;
HttpClient5 webhook to `chat.googleapis.com`; keys `novopay.ops.google-chat.enabled` / `webhook-url`;
env-gated (QA/UAT/PPD) via `novopay.service.environment`.

**Key platforms / programmes (deep-dives in their own memory files):**
- **Task-allocation platform** — service `trustt-platform-task-allocation`; work modeled as `task` +
  `task_type` (first type BKYC). → [[proj-task-allocation]]. (Legacy MFI `trustt-platform-task` is a
  different service.)
- **HDP-7636 Manipal BKYC** — first `task_type` under task-allocation; consent/Jira decisions. →
  [[proj-hdp-7636-bkyc]]. Note: credit-card `bkyc_*` tables ≠ this Manipal BKYC.
- **Spring Boot 4 / Java 25 upgrade** — branch `ddp-fea-spring4-java25-upgrade`. →
  [[proj-spring4-java25-upgrade]].

New v2 APIs follow the v2 REST pattern (see [[pref-coding-standards]]). New feature branches are
`ddp-fea-*` (see [[pref-git-workflow]]).
