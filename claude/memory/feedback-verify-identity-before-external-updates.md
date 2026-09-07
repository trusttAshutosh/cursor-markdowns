---
name: feedback-verify-identity-before-external-updates
description: "NEVER use the Atlassian/Jira MCP connector (it acts as Deepankar); do Jira via the user's browser login. ALWAYS ask the user to confirm the acting username before ANY Jira or GitHub write."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 62ed8ae3-0712-4c25-a300-3f2262e53515
  modified: 2026-09-03T15:55:50.421Z
---

Two hard rules from the user (2026-09-03):

1. **Never use the Atlassian / Jira MCP connector** — not for writes, not for reads. It is signed in as
   **Deepankar Sarkar (deepankar@trustt.com)**, and the user is Ashutosh ([[user-ashutosh]]). A Jira
   description edit on HDP-11225 went out under Deepankar's name because of it. For Jira work use the
   user's **browser login** (Claude in Chrome against `novopay.atlassian.net`, or hand the user the text).
2. **Before any write to Jira or GitHub**, look up the identity that will be used, show it, and **wait
   for explicit confirmation**. Per write, not per session.

**Why:** the machine has several identities in play (migrated Deepankar rules, `trusttAshutosh` gh
login, a connector logged in as someone else). A silent write mis-attributes work to a colleague and
cannot be undone in the audit history.

**How to apply:**
- GitHub / git (commit, push, `gh pr create/edit`, issue comment): run `gh api user --jq .login` and
  `git config user.name` / `user.email` in the target repo; report both ("commit as Ashutosh
  <ashutosh.kumar@trustt.com>, push/PR as trusttAshutosh — proceed?") and wait.
- Jira: open the issue in the user's Chrome, read the logged-in profile (avatar / account menu), report
  the name, and wait for "yes" before editing or commenting. Never call `editJiraIssue`,
  `addCommentToJiraIssue`, `transitionJiraIssue`, `createJiraIssue` or any other Atlassian MCP tool.
- Read-only git/gh operations need no confirmation.
- If the identity is wrong, do not write; give the user the text/commands instead.
- State the identity used in the completion message for every external write.

Related: [[user-ashutosh]], [[ref-github-account]], [[pref-git-workflow]], [[pref-jira-tickets]].
