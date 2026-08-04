---
name: pr-authoring
description: Create or update high-quality pull requests using conventional commit types (feat, fix, chore, refactor, docs, test, perf, ci, build), a detailed PR body, per-commit change summaries, and evidence from git. Use when the user asks to create or update a PR, improve PR descriptions, write commit messages, summarize changes, include testing guidance, attach screenshots/logs, or assess security impact.
---

# PR Authoring

## Goal

Produce merge-ready commits and pull requests that are easy to review, test, and audit.

## When To Use

Use this skill when:

- A user asks to create or update a pull request.
- A user asks for better commit messages.
- A user asks for a detailed PR description.
- A user asks to include security posture, affected files/flows, testing guidance, or screenshots/logs.

## Required Workflow

### Branch Safety Rule (Mandatory)

- Do not create new branches.
- Do not delete any branch (local or remote).
- Always prepare commits and create the PR from the current existing working branch.
- Open PR from the current branch to the user-specified target branch.
- If the target branch is not specified, ask the user before creating the PR.

### Existing PR Rule (Mandatory)

- Before opening a **new** PR, check whether an **open** PR already exists for the **current head branch** into the **agreed base branch**.
- Prefer GitHub CLI with evidence, for example (after resolving current branch name, e.g. `git branch --show-current`):
  - `gh pr list --head <current-branch> --base <base-branch> --state open --json number,url,title`
- **If exactly one open PR matches:** **update** that PR (`gh pr edit <number> ...`) with the new title/body instead of creating a duplicate. Confirm user intent if they only asked to "draft" text versus apply an edit on GitHub.
- **If more than one match:** stop and ask the user which PR number to update.
- **If none match:** create the PR (`gh pr create ...`) only after user intent for PR creation is clear.
- If `gh` is unavailable or unauthenticated, state that explicitly and provide the PR body for manual paste, still noting "no duplicate PR" guidance for the developer.
- When updating, keep the same PR URL/number unless the user asks otherwise.

### Evidence-Only Rule (Mandatory)

- Do not infer file lists, symbols, or behavioral claims from memory.
- Do not include any file/symbol in PR text unless it is present in git output.
- Do not write speculative statements like "minor utility adjustment" without diff evidence.
- If evidence is missing or ambiguous, state that explicitly and ask the user.
- If the user asks for "only files touched in those commits", compute from commit scope only (not guesses).

### User-Intent and Approval Gate (Mandatory)

- Before any git write operation, explicitly confirm what the user wants:
  - stage only
  - commit only (if already staged)
  - stage + commit
  - push
  - PR creation
  - PR update (edit title/body on an existing open PR)
- Do not assume permission to stage, commit, or push unless the user explicitly asked.
- Before pushing, present a concise summary of pending changes/commits and ask for explicit approval.
- If approval to push is not explicit, stop after local prep and ask.
- If any ambiguity exists around desired action scope, ask first and wait for confirmation.

1. Inspect git state and change scope.
   - Run `git status`, `git diff`, `git log --oneline -n 10`, and `git diff <base>...HEAD` if creating or updating a PR.
   - Always run `git log --oneline <base>..HEAD` to enumerate included commits.
   - Always run `git diff --name-only <base>...HEAD` to build the authoritative file list.
   - **Per-commit evidence:** For each commit SHA returned by `git log --oneline <base>..HEAD`, run:
     - `git show --no-patch --format=fuller <sha>` (or `--stat`) for subject/body and change size, and
     - `git show --name-status --pretty=format: <sha>` for the authoritative file list for that commit.
       Use this output to fill **Commits in this PR** in the PR body (subjects and paths must match git output).
2. If the user wants a GitHub PR created or updated, run the **Existing PR Rule**: detect an open PR for `--head <current> --base <base>`; then **edit** or **create** accordingly.
3. Confirm user intent for stage/commit/push/PR create/update actions before executing write operations.
4. Classify commits by intent using conventional types.
5. Draft commit message(s) emphasizing why, not only what.
6. Draft PR title and body using the template in this skill (including **Commits in this PR**).
7. Before pushing, request explicit approval after sharing what will be pushed.
8. Validate that PR text covers:
   - What changed
   - Why it changed
   - Files and flows affected
   - Functions/classes/modules touched and how behavior changed
   - Contract/data-shape changes and compatibility notes
   - Test plan and evidence
   - Security assessment
   - Performance/scalability impact and observability signals
   - Rollback or mitigation notes when risk is non-trivial

## Commit Type Selection

Choose the narrowest correct type:

- `feat`: User-facing or API-facing capability added.
- `fix`: Bug fix, broken behavior correction, production issue remediation.
- `refactor`: Internal restructuring with no intended behavior change.
- `chore`: Maintenance tasks, scripts, housekeeping, tooling noise.
- `docs`: Documentation-only updates.
- `test`: Test additions or test-only changes.
- `perf`: Performance or scalability improvement.
- `ci`: CI pipeline/workflow changes.
- `build`: Build/dependency/version packaging changes.

If multiple independent intents exist, split into multiple commits where practical.

## Commit Message Format

Use:

```text
<type>(<optional-scope>): <imperative summary>

<why this change is needed and what problem it solves>
<optional impact note: behavior/perf/security>
```

### Examples

```text
feat(flow): add customer-id based INIT fast path

Enable flow initialization with customer_id to skip details screen for known users.
This reduces latency and improves conversion for returning customers.
```

```text
fix(webhook): reject invalid signature before payload processing

Prevent unauthenticated webhook payloads from entering business logic.
This closes a spoofing risk on the inbound WhatsApp event path.
```

## PR Title Format

Default:

```text
<type>: <clear high-level outcome>
```

Examples:

- `feat: add cached idempotent response path for repeated flow screens`
- `fix: handle missing mobile fallback in INIT customer-id flow`

## PR Body Template

Use this exact structure and fill every section with concrete details:

```markdown
## What this PR does

- [High-level change 1]
- [High-level change 2]
- [Any non-obvious architecture or design decision]

## Problem / Fix

- **Problem:** [What was broken, risky, or missing]
- **Root cause:** [Underlying technical reason]
- **Fix applied:** [How the implementation solves it]
- **Why this approach:** [Trade-off rationale]

## Files changed

- `[path/to/fileA]` - [Purpose of the change]
- `[path/to/fileB]` - [Purpose of the change]
- `[path/to/fileC]` - [Purpose of the change]

## Commits in this PR (mandatory)

- Source: `git log --oneline <base>..HEAD` plus per-commit `git show` as in the workflow.
- Include a **table** mapping each commit to what changed, for example:

| Commit       | Subject (from git)        | Files touched (`git show --name-status`) | Short summary of change     |
| ------------ | ------------------------- | ---------------------------------------- | --------------------------- |
| `<full-sha>` | `<first line of message>` | `M path/a.js`, `A path/b.js`             | [Evidence-backed one-liner] |

- One row per commit in `<base>..HEAD` (use `git log --reverse --oneline <base>..HEAD` if you want oldest-first in the table; otherwise be consistent).
- Do not invent paths; the **Files touched** column must match `git show --name-status <sha>` for that row.

## Functions / symbols touched

- `[file-path]` -> `[symbolName()]` - [Added/Updated/Removed] - [Behavioral impact]
- `[file-path]` -> `[symbolName()]` - [Added/Updated/Removed] - [Behavioral impact]
- `[file-path]` -> `[SymbolOrConstant]` - [Added/Updated/Removed] - [Why reviewer should care]

## Technical implementation details

- **Control flow changes:** [Branching/early-return/retry/error-handling deltas]
- **Data contract changes:** [Request/response/schema/DTO/validation updates]
- **State and side effects:** [DB/Redis/cache/queue/file/network behavior changes]
- **Concurrency/idempotency:** [Race prevention, dedupe key, locking, retry semantics]
- **Failure-path behavior:** [What happens on timeout/downstream failure/invalid input]
- **Observability:** [Logs/metrics/traces added or changed; alerting impact]

## Affected flows

- **Flow / endpoint:** `[name or route]`
  - **Before:** [Behavior]
  - **After:** [Behavior]
  - **Risk level:** [Low/Medium/High]

## Optional visual aids (use when helpful)

- **Mermaid diagram:** [Add sequence/flow/state diagram for multi-step control flow, retries, async fan-out, or branching logic]
- **Table:** [Use compact tables for before/after behavior, endpoint impact, config changes, or risk matrix]

## Security assessment

- **Threats considered:** [Spoofing, tampering, data leakage, auth bypass, injection, replay, etc.]
- **Controls implemented/validated:** [Validation, authN/authZ, sanitization, encryption, rate limit, logging hygiene]
- **Data sensitivity impact:** [PII/secrets/tokens touched?]
- **Residual risk:** [What still remains and why acceptable]
- **Follow-ups:** [Any hardening tasks not in this PR]

## Test plan

- [ ] Unit-level validation completed
- [ ] Manual API validation completed (include request/response samples)
- [ ] Regression checks on related flows completed
- [ ] Negative-path/security checks completed
- [ ] Logs reviewed for errors and sensitive data leakage

## Test evidence

- **Commands run:** `[npm test]`, `[npm run dev]`, `[curl ...]`, etc.
- **Logs / traces:** [Paste key snippets proving behavior]
- **Screenshots:** [Attach UI/API screenshots when relevant]
- **Critical path proof:** [One end-to-end example per changed flow with expected output]

## Backward compatibility & rollout

- **Breaking changes:** [None or describe]
- **Config/env changes:** [None or list variables]
- **Rollback plan:** [How to revert safely]
- **Operational notes:** [Feature flags, canary scope, runbook/update needs]
```

## Evidence Quality Bar

- Prefer measurable statements (latency, error-rate, throughput) over vague claims.
- Never claim security as "fully secure"; describe controls and residual risk.
- Redact secrets/tokens/PII from screenshots and logs.
- If no screenshot is applicable (backend-only), attach representative logs and API responses.
- Use exact symbol names (functions/classes/constants/routes) rather than generic wording.
- For each touched symbol, state whether behavior changed, was refactored, or only moved.
- File list must be copied from `git diff --name-only <base>...HEAD` (or commit-scoped `git show`) without additions.
- The **Commits in this PR** table must list every commit in `<base>..HEAD` with paths from `git show --name-status <sha>` for that SHA only.
- "Functions / symbols touched" must be backed by diff hunks from the listed files only.
- If a section cannot be proven from diff/commands, write `Not observed in current diff` instead of guessing.
- Add Mermaid diagrams when behavior is easier to understand visually than prose.
- Prefer small markdown tables for dense comparisons (before/after, risk, contract deltas) when they improve readability.
- Do not add diagrams/tables as decoration; include them only when they materially improve reviewer comprehension.

## Review Checklist

- [ ] Commit type matches actual intent.
- [ ] PR title and body are consistent with change scope.
- [ ] All modified files are listed with purpose.
- [ ] All impacted flows/endpoints are explicitly documented.
- [ ] Function/symbol-level touch map is complete and accurate.
- [ ] Data contract and failure-path behavior are explicitly documented.
- [ ] Security section includes threats, controls, and residual risk.
- [ ] Performance/scalability impact is quantified or explicitly noted as unchanged.
- [ ] Test plan is executable and evidence is attached.
- [ ] No branch was created or deleted; PR was opened from the current working branch.
- [ ] User intent for stage/commit/push actions was explicitly confirmed.
- [ ] Explicit user approval was captured before push.
- [ ] Open PR was searched for (`gh pr list` or equivalent); existing PR was **updated** or absence confirmed before **create**.
- [ ] PR body includes **Commits in this PR** with one row per commit and paths from `git show --name-status` per SHA.
