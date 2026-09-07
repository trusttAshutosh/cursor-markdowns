---
name: ref-github-account
description: "GitHub account and org for Novopay work — this machine acts as trusttAshutosh on the trusttai org (deepankar-np is legacy from Deepankar's setup)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 62ed8ae3-0712-4c25-a300-3f2262e53515
  modified: 2026-09-07T03:00:00.000Z
---

For Novopay work under the `trusttai` GitHub org (repos `novopay-platform-*`, `trustt-platform-*`):

- **Acting account on this machine: `trusttAshutosh`** (gh CLI login, verified `gh api user`
  2026-09-03). Commits are authored `Ashutosh <ashutosh.kumar@trustt.com>`.
- `deepankar-np` was the account in the migrated Cursor rules (Deepankar's machine) — **not** the user's
  account here. Do not configure or suggest it unless the user asks.
- **Always confirm the acting account with the user before any GitHub write** —
  [[feedback-verify-identity-before-external-updates]].
- **Org rename:** `khoslalabs` → **`trusttai`**. Old remote URLs (`github.com/khoslalabs/...`) still
  redirect; prefer `trusttai` in remotes. Bulk rewrite: `tools/update-remotes-to-trusttai.ps1`.
- **Repo renames too:** on push (2026-09-07) GitHub reported `khoslalabs/novopay-platform-api-gateway`
  moved to **`trusttai/trustt-platform-api-gateway`** (repo name changed, not just the org). Pushes via the
  old URL still succeed through the redirect; check `gh repo view <old>` before assuming other
  `novopay-platform-*` repos kept their names.
- Push via Git Bash + plain `git`; if GCM prompts for an account, hand the command to the user.

Related: [[user-ashutosh]], [[pref-git-workflow]], [[ref-machine-commands]].
