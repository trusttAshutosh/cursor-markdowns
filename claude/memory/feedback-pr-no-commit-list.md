---
name: feedback-pr-no-commit-list
description: "PR descriptions must not list commits - GitHub's Commits tab already shows them; no Claude Code footer either"
metadata:
  node_type: memory
  type: feedback
---

Never put a `## Commits` (or Files changed) section in a PR description. The user removed it from the
five HDP-7350 prod PRs on 2026-09-23: "no need to mention Commits in PR description as I can anyways
click on Commits and see all the commits... that's redundancy". Also drop the
`🤖 Generated with [Claude Code]` footer - same correction as on BKYC #83/#84 (2026-09-15).

**Why:** GitHub already renders the commit list on its own tab, and PR bodies are read by reviewers and
ops for what is NOT derivable from git: what lands, bugs fixed, deployment/manual steps, related PRs.

**How to apply:**
- Useful sections for a release PR: What -> Jira -> Bugs fixed (from lower-env testing) -> Related PRs
  (cross-link every repo in the release) -> Deployment steps -> manual SQL (collapsed `<details>`).
- Put per-repo applicability in one line above a shared script so each PR says which parts it owns.
- Generalises [[feedback-bkyc-pr-template]] (same rule, stated there for BKYC only). Related:
  [[pref-git-workflow]].
