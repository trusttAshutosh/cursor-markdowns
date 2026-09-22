---
name: pref-end-with-summary
description: "Always close a reply with a short summary section - Deepankar reads the summary first"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-09-16T00:00:00.000Z
---

Every reply ends with a short summary of the answer, even when the body above is already
structured with tables and headings.

**Why:** Deepankar scans long analysis replies from the bottom. Investigations in this workspace
(multi-repo greps, Jira/UD digging, code-vs-spec comparisons) produce long answers with tables and
file citations, and the actual conclusion gets buried. He asked for this explicitly on 2026-09-16
after a BKYC template-vs-UD analysis that ran several screens with no closing recap.

**How to apply:**

- Close with a `## Summary` heading (or a bolded `Summary:` line for short replies).
- 2 to 5 lines or bullets. State the conclusion and the next action, not a re-listing of the detail.
- Applies to analysis, review, and investigation answers. A one-line factual reply does not need
  a summary appended to itself.
- Plain hyphens only, per [[pref-no-em-dashes]].

Related: [[pref-working-style]], [[pref-no-em-dashes]], [[pref-jira-tickets]].
