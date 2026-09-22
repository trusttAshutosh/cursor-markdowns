---
name: pref-no-em-dashes
description: "Never use em dashes or en dashes - always a plain hyphen, in chat replies and in every file, comment or draft written"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-09-16
---

Use a plain hyphen `-` instead of an em dash `—` or en dash `–`. Applies to
chat replies, Jira comment drafts, GitHub PR and issue comments, PR bodies,
commit messages, docs and code comments.

**Why:** stated three times now - twice on 2026-09-08 (HDP-11082 comment draft)
and again on 2026-09-16 after a GitHub PR comment on
`trusttai/trustt-platform-banking-origination` PR 5241 went out full of em
dashes. It is a standing style rule, not a one-off edit to a single file. Em
dashes also do not survive cleanly into Jira, GChat and GitHub pastes.

**How to apply:** write hyphens from the start rather than converting afterwards.
Before posting or handing over any draft, scan it for `—` and `–` and replace
with `-`. Where a dash separates clauses, ` - ` with spaces reads best.
Existing memory files (including MEMORY.md) still contain em dashes from earlier
sessions - leave them unless asked, but do not add more.

**Watch out:** this rule is easy to miss when a session starts outside the
workspace (for example in a scratch workspace) and only moves into a repo later,
because workspace memory is not recalled at session start. Apply it from the
first reply after the session lands in a `novopay` or `trustt` repo.

Related: [[pref-jira-tickets]], [[pref-working-style]], [[pref-end-with-summary]]
