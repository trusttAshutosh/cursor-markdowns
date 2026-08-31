---
name: pref-working-style
description: "How Deepankar wants work done — think-first, ask before token-heavy/subagent work, manual steps, model right-sizing"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:31:30.744Z
---

Deepankar's working-style preferences (core summary in CLAUDE.md).

**Why:** he values understanding before execution, keeps token/machine cost under control, and wants to
stay in the loop on scope and approach.

**How to apply:**

- **Think first:** restate intent, identify gaps, ask 1–3 focused questions only when they change the
  approach, propose a short plan for non-trivial work, then act. Don't ask what's answerable from open
  files/request/memory. Simple "what does X do?" → answer directly, no ceremony.
- **Discuss optional ideas before coding** them; pause and re-confirm on scope creep.
- **Token-heavy work** (many repos, wide search, multi-service builds, long merges): describe scope and
  ask before starting; re-confirm if scope grows.
- **Subagent delegation:** say what/why and ask first (unless the user requested it this turn). Offer
  manual commands as the cheaper default. Parallel agents only for independent work; never two agents
  writing the same repo/file/class — serialize.
- **Slow/heavy tasks:** give manual steps first (numbered, copy-paste), do the fast part (e.g. write the
  `.md`), automate only if the user says "run it" or it's known-good on this machine.
- **Model right-sizing:** simple → fast/Auto; medium → mid thinking model; complex (multi-repo,
  architecture, prod debug, backward compat, security, big merges) → a high thinking model. Recommend in
  the plan; if the user is on a heavy model for simple work, say a lighter one may save tokens.
- **For fixes, he often pastes Gradle/runtime logs** — use them; target root cause, not surface patches.
- **Ops/alert copy:** short startup/recovered messages; no log-file paths in success messages.

Related: [[ref-machine-commands]], [[pref-coding-standards]], [[pref-git-workflow]].
