---
name: ref-workspace-tools
description: Inventory of reusable scripts in C:\Users\ashutosh.kumar\Desktop\novopay\tools — reuse before writing new ones
metadata: 
  node_type: memory
  type: reference
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:32:32.295Z
---

Reusable scripts live in **`C:\Users\ashutosh.kumar\Desktop\novopay\tools\`** (decided location — do not move under `.cursor/`). Read
this before writing a new `tools/*` script or a large one-off shell block; extend an existing tool rather
than duplicate. Heavy/destructive scripts still need approval (see [[pref-git-workflow]]).

| Need | Script |
|---|---|
| Forbidden legacy ref ages (release / ddp-prod-v tips) | `check-forbidden-branch-age.sh` |
| Commit/push hook changes across many repos | `commit-push-git-hooks.ps1` / `.sh` |
| Disable hooks for one git op | `empty-git-hooks` + `core.hooksPath` |
| Branch status of named feature branches | `check-branch-status.ps1` |
| QA/UAT/prod merge readiness | `check-plan-branches-qa.ps1` |
| Feature containment graph | `scan-feature-branch-graph.ps1` (+ `feature-merge-graph*.mmd/.txt`) |
| Bkup ↔ env/prod sync (heavy, **ask first**) | `sync-bkup-branches-with-prod.ps1` (→ `sync-bkup-branches-results.txt`) |
| Merge ddp-prod into plan feature branches | `merge-ddp-prod-to-feature-branches.ps1` |
| Hard reset all repos to ddp-prod (**destructive**) | `reset-all-repos-to-ddp-prod.ps1` / `.sh` |
| Create leftover plan branches | `create-remaining-branches.ps1` |
| Extend unified feature tips | `extend-unified-branches.ps1` |
| Cherry-pick fix-prod / session-cache / JTF-hygiene commits | `apply-fix-prod-commits.ps1`, `apply-session-fix-cache.ps1`, `apply-jtf-template-hygiene.ps1` |
| khoslalabs → trusttai origin URLs | `update-remotes-to-trusttai.ps1` |
| Feature branch & Jenkins plan | `ddp-fea-branch-plan.md` |
| Release wave → commit mapping | `release-buckets.md` (+ `release-buckets-graph.mmd`) |
| W1 redis-fix preprod regression checklist | `w1-redis-fix-preprod-regression.md` |
| File delete/create hang diagnosis (Seqrite filter) | `windows-file-hang/HandleProbe.cs`, `Bulk.java` (+ README) — see [[ref-windows-seqrite-file-hang]] |

`*-results.txt` / `*.txt` scan dumps are outputs, not entry points. Many `.ps1` here are blocked on this
machine — see [[ref-machine-commands]] and prefer manual git steps.

Related: [[pref-git-workflow]], [[ref-machine-commands]].
