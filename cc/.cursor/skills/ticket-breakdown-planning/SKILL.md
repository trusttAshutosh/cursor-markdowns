---
name: ticket-breakdown-planning
description: Break down epics or features into Jira-ready sub-tickets with Product ticket body, Engineering reference, QA reference, journey impact tables, <=4h estimation slices, and justification. Use when user asks to create tickets, split tickets, sub-tasks, estimate work, sprint planning, or plan breakdown in data-purging/remarketing style for Novopay backend flows.
---

# Ticket Breakdown and Estimation Planning (Novopay Style)

## When To Use

Use when the user asks to:

- Break down a ticket / epic / feature into sub-tickets
- Create Jira-ready ticket text (Product + Engg + QA comments)
- Estimate work in **<=4 hour** slices with justification
- Plan sprint delivery order and dependencies
- Produce plans matching **data-purging** or **remarketing** format

Canonical format references (read when available):

- Data-purging style: `%USERPROFILE%\.cursor\plans\dsa_lead_lifecycle_tickets_02a51237.plan.md`
- Remarketing SMS style: `%USERPROFILE%\.cursor\plans\cc_remarketing_subtickets_47faa95c.plan.md`
- Technical depth (test matrices): `%USERPROFILE%\.cursor\plans\cc_remarketing_sms_batch_ddadc85b.plan.md`

Detailed copy-paste templates: [templates.md](templates.md)  
Worked examples: [examples.md](examples.md)

---

## Inputs Required

If missing, ask (use AskQuestion when available):

1. **Source material**: PRD snippet, product UD, raw notes, existing Jira, or conversation decisions
2. **Scope**: single feature vs full epic breakdown
3. **Target**: Jira sub-tickets only, or also main/parent ticket text
4. **Estimation unit**: hours (default), story points only if user requests
5. **Max slice size**: default **4 hours** per subtask row
6. **Modules/services** affected (for Engg/QA flow map)
7. **Branch baseline** (default: backend `ddp-prod`, frontend `dsa-prod` when UI touched)

Optional but valuable:

- Locked decisions already agreed (reduces rework)
- Open questions for Product sign-off (blockers vs non-blockers)

---

## Core Rules

1. **Content differs, format stays the same** — adapt wording to the feature; never drop sections from the template.
2. **Every sub-ticket gets all blocks** — Product ticket, Engineering reference, QA reference (as separate Jira comments).
3. **Journeys impacted is always a 3-column table**: `Journey | Who | What changes`.
4. **Estimation is always a 3-column table**: `Subtask | Est (hrs) | Why this size / justification`.
5. **Subtasks must be <=4h** unless user explicitly allows larger slices.
6. **Separate policy/foundation from delivery** when risk is high (eligibility, schema, config before batch/send paths).
7. **No existing MIS/report contract changes** unless user explicitly includes reporting work — use separate remarketing audit / tracking instead.
8. **Mark assumptions** as `ASSUMPTION` until Product confirms.

---

## Workflow

### Step 1 — Ingest and normalize requirements

Extract and label:

| Label | Meaning |
| --- | --- |
| **LOCKED** | Agreed in discussion or UD |
| **OPEN** | Needs Product/Engg answer before dev |
| **ASSUMPTION** | Reasonable default; confirm in sign-off |

Produce a short **UD vs decisions** section when source material is messy (mirror remarketing/purging plans).

### Step 2 — Choose breakdown strategy

| Strategy | When |
| --- | --- |
| **Vertical slices** | Independent deliverables (schema, batch, consumer, QA pack) |
| **Flow slices** | One ticket per major flow (retail vs bulk vs assisted) |
| **Risk slices** | High-risk logic first (eligibility, dedupe, link resolution) |
| **Layer slices** | Infra → domain → integration → QA/docs |

Default for backend batch/SMS features: **Risk + Vertical** (foundation → retail path → bulk path → config → QA/docs).

### Step 3 — Size and split tickets

Target ticket count guidance:

| Epic size | Typical sub-ticket count |
| --- | --- |
| Small feature | 2-4 |
| Medium feature | 4-7 |
| Large epic | 6-10 |

If total estimate > ~40h, split further or move QA/docs to its own ticket.

### Step 4 — Write each sub-ticket (mandatory sections)

For **each** sub-ticket, output in this order:

1. `### Product ticket` — Title, Description, Acceptance criteria, Depends on, Jira journey select/do not select, **Journeys impacted** (table), **Estimation** (table)
2. `### Engineering reference` — Journey/flow map table, modules, baseline patterns, implementation steps, schema/config if any
3. `### QA reference` — Pre-requisites, test data setup table, functional tests, DB checks, regression, out of scope

Use [templates.md](templates.md) verbatim structure; fill content only.

### Step 5 — Roll up and validate

- **Estimation summary** table per epic
- **Justification table** (why this split)
- **Dependency diagram** (text or mermaid)
- **Delivery order** (numbered list)
- **Sign-off table** for OPEN items (ID, blocker?, owner, decision)

---

## Section Standards (Do Not Skip)

### Product ticket — Description

Write for **Product/PM/QA readers**, not engineers:

- Business outcome in plain language
- Bullet eligibility / exclusions / behavior rules
- What is explicitly out of scope
- Acceptance criteria as testable bullets

### Engineering reference

Must include:

- **Journey / flow map** table: `Flow | API / entry | Module`
- **Modules** list (all repos touched)
- **Baseline patterns** (link to similar existing code in repo)
- **Implementation** numbered steps (concrete, not vague)
- **Frontend** line only if UI/regression relevant

### QA reference

Must include:

- **Pre-requisites** (env, data, access, upstream tickets)
- **Test data setup (minimum)** table with columns appropriate to feature (Lead/Age/State/Expected pattern)
- **Functional tests** numbered scenarios (happy path, exclusions, failures, idempotency, regression)
- **DB checks (sample)** SQL when DB validation matters
- **Out of scope** for this ticket
- **Depends on** upstream ticket when applicable

### Jira journey field (Novopay)

When project uses journey dropdown, include per ticket:

- **Jira journey field - select these (multiple)**
- **Do not select** with explicit exclusions

See [examples.md](examples.md) for CC remarketing and DSA lifecycle patterns.

### Estimation justification quality bar

Each `Why this size / justification` cell must state one of:

- Blocks downstream work
- Isolated risk/domain
- Integration surface count
- Test matrix size
- Operational/config-only scope
- Review/QA handoff slice

Bad: "Development work"  
Good: "Integration-heavy path; failure-prone SMS + audit writes"

---

## Estimation Heuristics (Hours)

| Work type | Typical range (hrs) |
| --- | --- |
| Decision / contract finalization | 1.5-3 |
| Single DAO query or small service method | 2-4 |
| Processor + orchestration wiring | 3-5 |
| New entity + repository + flyway | 4-6 |
| Kafka publish + consumer | 8-14 (split across 2-4 tickets) |
| Config + scheduler only | 6-10 |
| Unit test slice (focused matrix) | 3-4 |
| QA matrix + evidence pack | 8-12 |
| Docs + runbook only | 4-8 |

Always split work so **no single subtask row exceeds 4h** unless user overrides.

---

## Output Modes

| Mode | Output |
| --- | --- |
| `full-plan` | Complete markdown plan file (like `.cursor/plans/*.plan.md`) |
| `jira-ready` | Per-ticket blocks ready to paste into Jira |
| `estimation-only` | Tables only (subtasks + summary + justification) |
| `single-ticket` | Break down one parent ticket ID/title only |

Default: `jira-ready` + offer to also write a consolidated plan file if useful.

---

## Quality Checklist (Before Handoff)

- [ ] Every sub-ticket has Product + Engg + QA sections
- [ ] Journeys impacted table present and non-empty
- [ ] Estimation table present; all rows <=4h (unless approved)
- [ ] Dependencies and delivery order documented
- [ ] OPEN questions listed with blocker flag
- [ ] No engineering jargon in Product ticket Description
- [ ] Engg reference includes flow map and modules
- [ ] QA reference includes pre-reqs, setup table, functional tests
- [ ] Terminology consistent within the plan (one name for txn status, consent state, etc.)

---

## Anti-Patterns

- Do not produce generic "Implement feature" tickets without journey table and acceptance criteria.
- Do not merge Engg details into Product description (keep separate comments).
- Do not estimate in story points unless user asked.
- Do not invent modules or APIs — mark `TBD` and add OPEN question.
- Do not skip QA reference for "small" infra tickets if they affect release confidence.

---

## Quick Invoke Examples

- "Break down remarketing SMS epic into sub-tickets like data purging plan"
- "Create Jira tickets with engg and QA comments for this feature"
- "Estimate this ticket in 4 hour tasks with justification table"
- "Split CC-RMK epic into implementable sub-tickets with journey impact tables"

When user references a plan file path, read it and mirror its section structure exactly.
