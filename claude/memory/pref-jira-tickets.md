---
name: pref-jira-tickets
description: "Jira tickets must be self-contained — full API/DDL/samples in the description, not doc-md pointers"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:32:03.072Z
---

When creating or editing Jira issues (Stories, Sub-tasks, implementable Clarifications), the **ticket
description is the developer's source of truth**.

**Why:** developers don't have Deepankar's clone of `C:\Users\ashutosh.kumar\Desktop\novopay` or its `docs/**/*.md`; a ticket that
only says "see solution-document §X" can't be built.

**How to apply:**
- Put **full** implementable detail in the description: API `Field | Type | Required | Sample | Notes`
  tables, request/response samples, DDL/seed/status-mapping tables when the ticket owns schema.
- Same bar for **client tickets** (Android / Admin / React) that call APIs — they carry the full API
  contract even though FE doesn't implement the Java.
- Keep local `.md`/mdshare as **author** SoT; link published mdshare/Confluence only *in addition to* the
  inline contract.
- Don't rely on local `docs/` paths or private mind maps as the only contract.

Related: [[proj-hdp-7636-bkyc]] (BKYC ticket conventions), [[proj-task-allocation]].
