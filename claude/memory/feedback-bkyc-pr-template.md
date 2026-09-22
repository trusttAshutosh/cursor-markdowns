---
name: feedback-bkyc-pr-template
description: "BKYC PR bodies must follow .cursor/rules/bkyc-pr-description.mdc (not the style of the last merged PRs); titles [QA]/[UAT]"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 934764bb-50ec-484d-b1fa-7f0a798faced
  modified: 2026-09-15T14:48:29.227Z
---

Every PR for a BKYC ticket (HDP-7636 tree: task-allocation, auth, gateway, actor, masterdata) must use the
template in `C:\Users\ashutosh.kumar\Desktop\novopay\.cursor\rules\bkyc-pr-description.mdc`. Copying the format
of recent PRs (e.g. task-allocation #81/#82) is NOT the template - the user corrected this on HDP-11535 (#83/#84,
2026-09-15).

**Why:** the template is the team's reviewer contract (plain-English flowchart, journey table with live Jira Done,
decisions, handoff codes). It lives in `.cursor/rules/` and `AGENTS.md`, which a Claude session does not load by
default, so it is easy to miss.

**How to apply:**
- Required order: ticket / what lands -> PR pack -> Verify / Test plan -> How this fits (mermaid, plain English, no
  API/permission/class names) -> Where this PR sits (full canonical journey table, `This PR` / `(upstream)` /
  `(not this PR)`, Done = `✅` only if Jira Done - query Jira live) -> Decisions / tradeoffs -> Knowledge handoff.
- Verify: numbered scenarios with the result on the right (`✅` / `❌`, blank when pending deploy, never `❌` for
  pending); use the full proven QA pack list for the touched area (`docs/tdd-runs/HDP-7636/BKYC_QA_TEST_PACK.md`).
- ASCII hyphen-minus only (no en/em dashes or arrows). Titles start with `[QA]` / `[UAT]` per target branch.
- Follow the template STRICTLY: only the 7 required sections (plus the template's own optional items:
  common-scripts links, rename callouts, sign-off links). No Commits / Files changed / Technical details
  sections and no "Generated with Claude Code" footer - the user removed both on #83/#84 (2026-09-15).
- Example pack: `docs/tdd-runs/HDP-8937/PR_DESCRIPTION.md`. Related: [[proj-hdp-7636-bkyc]], [[pref-git-workflow]].
