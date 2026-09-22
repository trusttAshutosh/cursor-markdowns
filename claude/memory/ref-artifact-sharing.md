---
name: ref-artifact-sharing
description: Artifact share pin must be moved by hand after every republish; versions cannot be deleted
metadata: 
  node_type: memory
  type: reference
  originSessionId: d9860180-f87c-4b3a-a68c-c9b7d3aecca0
  modified: 2026-09-07T14:53:45.404Z
---

Two facts about Claude Code artifacts that have cost repeated back-and-forth (7 Sep 2026):

**The share pin does not follow a republish.** Publishing a new version does NOT update what viewers
see. The read-back says it plainly: *"viewers currently see this version, but will not see future
publishes until the share pin is moved."* Ashutosh must move the pin from the artifact's share menu
after every republish, or the team keeps reading a stale version. So: batch edits into one publish
rather than republishing repeatedly, and always end by telling him to move the pin.

**Versions cannot be deleted, and cannot even be listed.** The Artifact tool exposes publish, read,
list, watch, comments, resolve, and the db/asset actions — there is no version-management action.
`action: "list"` returns only title, URL, favicon and last-updated; no version data. The only route to
a single-version artifact is republishing to a brand-new URL (starts at v1), which changes the link
the team already has — usually not worth it, because **viewers never see version history anyway**;
they only ever get the pinned version. Say that rather than retrying.

Long-running QA report artifact: `BKYC QA Run Sheet`
https://claude.ai/code/artifact/617717fe-b05b-4456-a234-02123fdbb968 — see
[[proj-hdp-7636-bkyc]] and [[ref-qa-task-allocation-api-calls]].
