---
name: feedback-pr-conflict-check
description: "Check for conflicts the way GitHub does BEFORE raising a QA/UAT PR; on conflict raise it from ddp-bkup-qa/uat, never leave a conflicting PR"
metadata:
  type: feedback
---

Before `gh pr create` to `ddp-qa` / `ddp-uat`, check mergeability the way GitHub computes it, and if it
conflicts, resolve on the bkup mirror and raise the PR from `ddp-bkup-qa` / `ddp-bkup-uat` instead.

**Why:** Repeated. notifications #5333 (HDP-12336, 2026-10-12) and creditcard #2513 (AOC unique codes, 2026-10-15): "always check for conflicts before creating PR. remember this for future". Local `git merge-tree --name-only origin/ddp-qa HEAD` exited 0 (multiple merge bases); GitHub was `CONFLICTING`/`DIRTY` after create. The PR had to be closed.

**How to apply:**
- Check: `git merge-base --all origin/<base> origin/<head>`; if more than one, also run
  `git merge-tree --write-tree --merge-base=<each base> origin/<base> origin/<head>`. Treat any conflict as real.
  After creating a PR, confirm `gh pr view <n> --json mergeable` is `MERGEABLE`.
- On conflict follow [[pref-git-workflow]]: sync `ddp-bkup-qa` with `origin/ddp-qa`, merge the feature, resolve
  there, `compileJava`, push bkup (protected - ask first), raise `[QA]` from `ddp-bkup-qa`, note the head and
  the resolution in the PR body (like actor #18595), close the conflicting PR with a pointer.
- Related: [[feedback-bkyc-pr-template]], [[pref-git-workflow]].
