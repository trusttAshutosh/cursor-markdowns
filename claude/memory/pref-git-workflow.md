---
name: pref-git-workflow
description: "How Deepankar wants git handled — ddp-fea naming, protected-branch approval, bkup promotion, backward compat"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:31:15.287Z
---

Git conventions for Novopay/trustt repos (core summary is in CLAUDE.md; full detail here).

**Why:** these branches map to real QA/UAT/prod environments and Jenkins pipelines; a wrong push or an
un-flagged breaking change can hit production.

**How to apply:**

- **Feature branch naming:** always `ddp-fea-<short-kebab>` (base `origin/ddp-prod`). Never `ddp-fix-*`,
  `ddp-bug-*`, `fix-*`, `feature/*` — GitHub rejects non-`ddp-fea` creations. If the user proposes another
  name, rename to `ddp-fea-*` and say why.
- **Protected branches — ask before any merge/push/checkout-for-merge:** `ddp-bkup-qa`, `ddp-bkup-uat`,
  `ddp-qa`, `ddp-uat`, `ddp-prod`. Read-only inspection (`log`/`diff`/`status`/`fetch`) is fine. Approval
  is per-action only.
- **QA/UAT promotion via bkup mirror (never push env branches directly):**
  1. `git fetch origin ddp-qa ddp-uat ddp-bkup-qa ddp-bkup-uat <feature>`
  2. Checkout `ddp-bkup-qa` (QA) or `ddp-bkup-uat` (UAT).
  3. Merge the env tip **into bkup first** (`origin/ddp-qa`→bkup-qa), resolve on bkup.
  4. Merge `origin/<feature>` into bkup; resolve conflicts on bkup only.
  5. `.\gradlew.bat compileJava --no-daemon` — must pass before push.
  6. Push **only** `origin/ddp-bkup-qa|uat`. Jenkins/user merges bkup → env.
- **Fix on feature first:** when on a `ddp-bkup-*` branch and the change belongs to a `ddp-fea-*` line,
  fix on the `ddp-fea-*` branch first, then cherry-pick (preferred) or merge into bkup. Don't fix only on
  bkup unless it's pure env-conflict resolution or the user says so.
- **Backward compatibility:** before changing **existing** behavior (APIs, contracts, config defaults,
  cache/session keys, DB reads, filter/gateway routing, response shape) ask "need backward compat with
  prod?" Baseline is always `origin/ddp-prod`. If yes → preserve behind flags / v1-v2 / additive changes.
- **No bulk/heavy git without approval:** `tools/sync-bkup-branches-with-prod.ps1`, multi-repo loops, full
  `gradlew build`/`test`. Prefer manual steps or single-repo commands (see [[ref-machine-commands]]).
- **Commits:** conventional subject; full technical body when committing (see CLAUDE.md); never commit
  without an explicit request.

Related: [[ref-github-account]], [[ref-machine-commands]], [[ref-workspace-tools]], [[ref-flyway-infra-versioning]], [[pref-coding-standards]].
