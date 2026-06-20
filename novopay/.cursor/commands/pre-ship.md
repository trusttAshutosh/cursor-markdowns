---
description: "Ship gate - per-repo PR .md files with diagrams, tradeoffs, cross-repo refs (no Bob mentions)"
---

# Pre-ship evidence pack (Ship gate)

User input after command: ticket id (required), optional branch, base branch default ddp-prod.

## Inputs (read silently - never cite in output)

- `docs/tdd-runs/<ticket_id>/` (ticket-spec, GATE_SUMMARY, REPORT, verify SQL, logs notes)
- Git diff across **all novopay repos** touched: CC, lib, gateway, actor (compare branch vs base)
- Do **not** mention Bob, validate-ticket, GATE_SUMMARY, or REPORT in any written file.

## Output files (one PR pack per changed repo)

Create folder `docs/tdd-runs/<ticket_id>/` if missing.

| File | Purpose |
|------|---------|
| `PRE_SHIP_INDEX.md` | Index: all repos changed, links to per-repo files, coordinated release note |
| `PRE_SHIP_cc.md` | PR for `novopay-platform-creditcard-management` (only if CC changed) |
| `PRE_SHIP_lib.md` | PR for `novopay-platform-lib` (only if lib changed) |
| `PRE_SHIP_gateway.md` | PR for `novopay-platform-api-gateway` (only if gateway changed) |
| `PRE_SHIP_actor.md` | PR for `novopay-platform-actor` (only if actor changed) |

Write **only files for repos with actual diff**. Always write `PRE_SHIP_INDEX.md`.

## Global rules

- **Concise.** Bullets and tables only. No prose walls.
- **Punctuation:** ASCII hyphen-minus (`-`) only in all output. Use ` - ` (space-hyphen-space) for clause breaks. Never U+2014 em dash or U+2013 en dash. Ranges: `1-5`, `lib-CC`.
- **Multi-repo mandatory.** Every per-repo file starts with **Repos changed** listing ALL repos in the fix (not just current file's repo).
- **Cross-repo section** in each per-repo file: concise summary of what changed in sibling repos + "see `PRE_SHIP_<other>.md` for that PR body".
- **Root cause:** observations from logs/incident (what was seen) -> root cause (why it broke).
- **Assumptions:** explicit bullet list.
- **Solutions considered:** table with option | pros | cons | decision (chosen / rejected).
- **Tradeoffs:** table option taken | tradeoff accepted.
- **Diagrams (mandatory - before vs after):** In **each** per-repo file include **four** mermaid blocks:
  1. **Flow - before fix** (broken/latent behavior; label nodes that fail or skip steps)
  2. **Flow - after fix** (same scope; highlight what changed)
  3. **Sequence - before fix** (failure or bug path)
  4. **Sequence - after fix** (corrected path)
  - Keep before/after pairs **comparable** (same actors/participants where possible).
  - One short bullet under each diagram: **Delta:** what changed.
- **UTs:** table must include **file**, **test class**, **method/function under test**, **scenario tested** (one row per test method or logical scenario group).
- **E2E / integration:** scenario | steps | expected | evidence (no tool/product names for test runners).
- **Reviewer FAQ:** preempt scope, rollback, DAP/Salesforce, DB/flyway, config, regression, deploy order for multi-repo.
- Do NOT commit, push, or run validate-ticket unless user asks.

---

## PRE_SHIP_INDEX.md template

```markdown
# Pre-ship index: <ticket_id>

**Title:** <one line> | **Branch:** <branch> → <base>

## Repos changed

| Repo | PR pack | Deploy order |
|------|---------|--------------|
| CC | [PRE_SHIP_cc.md](./PRE_SHIP_cc.md) | 2 |
| lib | [PRE_SHIP_lib.md](./PRE_SHIP_lib.md) | 1 |
| ... | ... | ... |

## Coordinated release

- **Order:** lib → CC → ... (why)
- **Merge blockers:** CC PR depends on lib PR #TBD
```

---

## Per-repo file template (`PRE_SHIP_<slug>.md`)

Use for CC, lib, gateway, actor. Replace `<THIS_REPO>` with human name (e.g. Credit Card Management).

```markdown
# PR: <title> - <THIS_REPO>

**Ticket:** <id> | **Branch:** <branch> → <base> | **This PR repo:** <THIS_REPO>

## Repos changed (full fix)

| Repo | Role in fix | This PR? |
|------|-------------|----------|
| novopay-platform-creditcard-management | ... | Yes / No - see PRE_SHIP_cc.md |
| novopay-platform-lib | ... | Yes / No - see PRE_SHIP_lib.md |
| ... | ... | ... |

## Changes in other repos (concise)

| Repo | What changed (1-2 bullets) | Detail PR pack |
|------|---------------------------|----------------|
| lib | ... | PRE_SHIP_lib.md |
| CC | ... | PRE_SHIP_cc.md |

## Summary

- **Problem:**
- **Fix (this repo):**
- **Out of scope:**

## Observations & root cause

| Observation (logs / DB / API) | Root cause |
|------------------------------|------------|
| ... | ... |

## Assumptions

- ...

## Solutions considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A: ... | ... | ... | **Chosen** - why |
| B: ... | ... | ... | Rejected - why |

## Tradeoffs

| Chosen | Tradeoff accepted |
|--------|-------------------|
| ... | ... |

## Flow - before fix

```mermaid
flowchart LR
  ...
```

- **Delta:** (filled in after-fix section)

## Flow - after fix

```mermaid
flowchart LR
  ...
```

- **Delta:** <one line vs before>

## Sequence - before fix

```mermaid
sequenceDiagram
  ...
```

- **Delta:** (filled in after-fix section)

## Sequence - after fix

```mermaid
sequenceDiagram
  ...
```

- **Delta:** <one line vs before>

## Change map (this repo)

| File | Function / class | Change |
|------|------------------|--------|
| `path/to/File.java` | `methodName()` | ... |

## Unit tests (this repo)

| Test file | Test class | Method / function under test | Scenario |
|-----------|------------|------------------------------|----------|
| `src/test/.../FooTest.java` | `FooTest` | `FooService.bar()` | partial rollback clears staging |
| ... | ... | ... | ... |

## E2E / integration

| Scenario | Steps | Expected | Evidence |
|----------|-------|----------|----------|
| ... | ... | ... | ... |

## Reviewer FAQ

| Question | Answer |
|----------|--------|
| Why this approach? | |
| Why not option B? | |
| DAP vs Salesforce? | |
| DB / flyway (this repo)? | |
| Sibling repo required first? | |
| Rollback / ops cleanup? | |
| Regression risk? | |
| Config / flag? | |

## Risks & rollback

| Risk | Mitigation | Rollback |
|------|------------|----------|
| ... | ... | ... |

## PR title (copy - paste into GitHub for <THIS_REPO>)

`<ticket_id>: <short title>`

## PR body (copy - paste into GitHub for <THIS_REPO>)

### Summary
- ...

### Repos in this fix
- **This PR:** <THIS_REPO>
- **Also changed:** lib (PRE_SHIP_lib.md), CC (PRE_SHIP_cc.md) - one line each

### Root cause
- ...

### Before / after (see full diagrams in this file)
- **Before:** ...
- **After:** ...

### Test plan
- [ ] UTs: ...
- [ ] E2E: ...

### Reviewer focus
- ...
```

---

## Repo slug map

| Path / repo | Output file |
|-------------|-------------|
| `novopay-platform-creditcard-management` | `PRE_SHIP_cc.md` |
| `novopay-platform-lib` | `PRE_SHIP_lib.md` |
| `novopay-platform-api-gateway` | `PRE_SHIP_gateway.md` |
| `novopay-platform-actor` | `PRE_SHIP_actor.md` |

Detect changed repos from git diff under `Desktop/novopay/`. If diff spans repos, write all applicable files + index with deploy order.

## After writing

Reply with: list of files written under `docs/tdd-runs/<ticket_id>/` + one-line confirmation. Do not paste full files in chat unless user asks.
