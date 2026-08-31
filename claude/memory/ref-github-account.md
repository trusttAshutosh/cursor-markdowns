---
name: ref-github-account
description: GitHub account and org for Novopay work — use deepankar-np on the trusttai org
metadata: 
  node_type: memory
  type: reference
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:30:42.205Z
---

For **any** Novopay work, git remote, or GitHub URL under `trusttai` (repos `novopay-platform-*`,
`trustt-platform-*`; remotes at `github.com/trusttai/` or `git@github.com:trusttai/`), authenticate and
operate as GitHub user **`deepankar-np`** — not `deepankar17` or other personal accounts.

- **Org rename:** `khoslalabs` → **`trusttai`**. Old URLs may redirect; prefer `trusttai` in remotes.
- If an account picker or auth failure appears, tell the user to use **`deepankar-np`** — don't guess tokens.
- One-time git config to prefer this account (reduces the GCM "Select an account" popup):
  ```bash
  git config --global url."https://deepankar-np@github.com/trusttai/".insteadOf "https://github.com/trusttai/"
  git config --global credential.https://github.com/trusttai.username deepankar-np
  ```
- Bulk remote rewrite khoslalabs→trusttai: `tools/update-remotes-to-trusttai.ps1`.

Related: [[user-deepankar]], [[pref-git-workflow]].
