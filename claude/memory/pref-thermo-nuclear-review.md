---
name: pref-thermo-nuclear-review
description: "/thermo-nuclear-code-review = the user's strict code-quality review skill (Claude port of their Cursor skill); always run it via the Skill tool when invoked"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d9860180-f87c-4b3a-a68c-c9b7d3aecca0
  modified: 2026-09-04T02:09:24.037Z
---

The user ported their Cursor "Thermo-Nuclear Code Quality Review" skill to Claude Code on 2026-09-04. It lives at
`C:\Users\ashutosh.kumar\.claude\skills\thermo-nuclear-code-review\SKILL.md` (user-level, so it works in every repo).

**Why:** they want one command for an unusually strict, structure-first review: code-judo simplifications,
1000-line file ceiling, no spaghetti branching, boundary/type cleanliness, canonical-layer reuse - not a
"looks fine, ships" review.

**How to apply:** whenever the user types `/thermo-nuclear-code-review` (optionally with a PR number, branch,
or path), invoke that skill through the Skill tool and follow it exactly: scope from `origin/ddp-prod` in
platform repos, read whole files not just hunks, report Verdict + prioritised findings + file-size table, do
not apply fixes unless asked afterwards. Also use it when they ask for a "thermo-nuclear" / "no-mercy" /
"brutal" quality review in prose. Related: [[pref-coding-standards]], [[pref-working-style]].
