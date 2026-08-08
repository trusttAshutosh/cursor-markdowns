---
name: where-did-time-go
description: >-
  Build a chronological daily workflog as a table (time, duration, work, ticket,
  chat) with total duration at the end. Use when the user asks where time went,
  daily workflow, workflog, timeline of today's chats,
  /where-did-time-go, or standup that must include investigation with no ticket.
disable-model-invocation: true
---

# Where did time go

Produce one **unified daily timeline** across **all** Cursor chats that day:
blocks from every session merged into a single list, sorted **start → end** by
time — including investigation that never became a commit or Jira ticket.

Never group the final output by chat/project. Chats are only the source; the
deliverable is one chronological **table** plus a **total duration** footer.

## Trigger

Default window: **today** (local timezone). Also: yesterday, last N days, a date.

## Workflow

```
- [ ] 1. Resolve day + person
- [ ] 2. Collect sessions for that day
- [ ] 3. Build time blocks (start → end → topic + build/ops/meta tag)
- [ ] 4. Sort chronologically; merge overlaps
- [ ] 5. Optionally attach commits to blocks
- [ ] 6. Emit workflog (table + total duration + Mix footer)
- [ ] 7. Persist run to Desktop worklogs (required)
```

### 1. Resolve day + person

- Day from user request or `date +%Y-%m-%d`.
- Person = current user (`git config user.name` / email local-part). One person
  per run unless the user names someone else (still only their local transcripts).

### 2. Collect sessions

Scan: `~/.cursor/projects/*/agent-transcripts/**/*.jsonl`

Fast filter (mtime that day):

```bash
find "$HOME/.cursor/projects" -path "*/agent-transcripts/*/*.jsonl" -newermt "YYYY-MM-DD" ! -newermt "YYYY-MM-DD +1 day" 2>/dev/null
```

Optional helper (if Python responds quickly):

```bash
/c/Python314/python ~/.cursor/skills/where-did-time-go/scripts/list_sessions.py --since YYYY-MM-DD
```

If the helper hangs, use `find` + read files yourself.

Also include a file if any embedded `<timestamp>...` falls on that day even when
mtime is later.

### 3. Build time blocks from each session

For each matching `.jsonl`:

1. Pull every `<timestamp>...` and every `<user_query>...`.
2. **Session start** = earliest timestamp that day (else first user turn that day).
3. **Session end** = latest timestamp that day (else file mtime if same day).
4. **Duration** = end − start (label `~`). If only one stamp → `duration unknown`.
5. **Topic** = short outcome from user queries + final assistant conclusion
   (what was worked on — not tool spam). Prefer functional wording.
6. **Tag** the topic as `build:` / `ops:` / `meta:` (see Work tags in step 6).
7. Note Jira keys if present (`PROJ-123` pattern only); leave **Ticket** blank when none.
8. Cite `[title](uuid)` with transcript uuid (folder/stem).

Split one long chat into multiple blocks **only** when the topic clearly changes
(new problem / new ticket) with timestamps far apart; otherwise one block per session.

### 4. One timeline across all chats

1. Collect blocks from **every** matching session (all projects).
2. Sort by **start time ascending** (then end time) into **one** list.
3. Do **not** nest under chat names or project folders in the final output.
4. Same topic continuing in a later message of the same chat → keep/extend one block.
5. Different chats interleaved in time → interleave their blocks in clock order
   (Chat A 9:00, Chat B 9:20, Chat A 10:00 → that order).
6. Heavy overlap on the same topic → merge; different topics overlapping → list
   both and mark `(overlap)`.
7. Drop pure meta (plugin how-to) unless user asked for the full day.

### 5. Commits (optional enrichment)

Same rules as `what-did-i-get-done` for that day. Attach a commit under the
block it belongs to when obvious; do not invent a separate timeline from commits
alone if chats already cover the work.

### 6. Output format (required)

**Single day timeline** — one **table**, rows in clock order, all chats mixed.
Always end with a **total duration** line.

```markdown
## Workflog — YYYY-MM-DD
**Person:** <name>

| # | Time | Duration | Work | Ticket | Chat |
|---|------|----------|------|--------|------|
| 1 | 08:10–08:55 | ~45m | build: OTP RCA | | [OTP RCA](uuid) |
| 2 | 09:05–09:25 | ~20m | build: DSA report DAO fix | PROJ-123 | [DSA report fix](uuid) |
| 3 | 14:05–14:45 | ~40m | meta: Atlassian capture design | | [Work capture design](uuid) |

**Total duration:** ~1h 45m *(estimates from chat timestamps)*

**Mix:** build ~1h 5m · ops ~0m · meta ~40m

**Wall clock:** 08:10–14:45 (~6h 35m span) — optional; include when gaps between blocks are large.
```

#### Table columns

| Column | Content |
|--------|---------|
| **#** | Row number, sort key = start time |
| **Time** | `HH:MM–HH:MM` block start–end |
| **Duration** | `~Xm` or `~Xh Ym`; use `unknown` if only one stamp |
| **Work** | **Required tag** + one short phrase — see Work tags below |
| **Ticket** | Jira ID(s) only (e.g. `PROJ-123`, `AAN-601`); **leave blank** when none — never `no ticket`, prose, or repo names |
| **Chat** | `[title](uuid)` transcript cite |

Mark overlapping different-topic blocks with `(overlap)` in the **Work** cell
(after the tag), e.g. `ops: Jenkins deploy watch (overlap)`.

#### Work tags (required)

Every **Work** cell **must** start with exactly one of these prefixes
(`tag:` + space + phrase):

| Tag | Use for | Examples |
|-----|---------|----------|
| `build:` | Shipping product/ticket work - implement, fix, test, Bob prove, commit, ticket RCA toward a change | Feature/bug code, Sonar on feature tests, UAT RCA for a ticket, QA handoff for a feature |
| `ops:` | Env / deploy / infra / branch hygiene - firefighting that is not the feature itself | Flyway checksum repair, Jenkins watch, merge-conflict resolve, branch sync/pull, DB/env drift checks |
| `meta:` | Tooling, process, skills, non-ticket analysis | `/where-did-time-go`, plugin how-tos, agent hygiene, work-capture design, Jira insights canvases |

Rules for tagging:

- Pick **one** primary tag (the dominant purpose of the block).
- Ticket-linked investigation that aims to ship a fix → `build:` (even if mostly logs).
- Pure deploy/Flyway/merge/branch work with no feature outcome → `ops:`.
- Skills, Cursor tooling, standup capture, product-insight docs with no code → `meta:`.
- Never invent other prefixes (`fix:`, `qa:`, etc.).

#### Total duration (required footer)

1. Parse each row's **Duration** to minutes (`~1h 45m` → 105).
2. **Sum all rows** for the total.
3. Rows marked `(overlap)` that share the same clock window — count each row's
   duration once (do not double-count the same minutes twice). When unsure,
   sum naively and add: *(may double-count N min of overlap)*.
4. Format total as `~Xh Ym` (or `~Xm` if under 1h).
5. Always note estimates when timestamps are sparse: *(estimates from chat timestamps)*.

#### Mix footer (required)

After **Total duration**, always emit a **Mix** line that sums minutes by Work tag
(same overlap rules as the total - do not double-count shared windows):

```markdown
**Mix:** build ~Xh Ym · ops ~Ym · meta ~Zm
```

Omit a category only if its sum is 0 (`ops ~0m` is fine to keep for scanability).
Unknown-duration rows do not contribute to Mix (same as Total).

Example footer:

```markdown
**Total duration:** ~7h 20m *(estimates from chat timestamps; 31m overlap not double-counted)*

**Mix:** build ~4h 10m · ops ~2h 30m · meta ~40m
```

#### Spoken shape (optional, after the table)

> Ashutosh — 2026-07-31 — **~1h 45m total** (build ~1h 5m / meta ~40m)  
> 08:10–08:55 build: OTP RCA · 09:05–09:25 build: DSA report DAO fix · 14:05–14:45 meta: Atlassian capture design

Wrong: sections per chat (“Chat 1… Chat 2…”).  
Wrong: numbered list instead of table.  
Wrong: Work cell without `build:` / `ops:` / `meta:` prefix.  
Right: one table from earliest start to latest end, total + Mix at the bottom.

Rules:

- Sort key = block start time only (cross-chat).
- One row per block; keep **Work** to one line starting with `build:` / `ops:` / `meta:`.
- **Ticket** column: Jira IDs only; blank cell if no linked ticket.
- Always state the date, **Total duration**, and **Mix** footer.
- Durations are estimates from chat timestamps — say so if sparse.
- Do not create Jira unless explicitly asked this turn.
- No secrets, full logs, or stack traces.
- Always persist the run (step 7) after emitting the table.

### 7. Persist run to Desktop worklogs (required)

Every successful run **must** write the full markdown workflog (same content as
shown to the user) to a durable folder on the Desktop, grouped by **month**,
then by **day** (so multiple runs on the same day stay together).

**Root:** `~/Desktop/worklogs`  
On this machine: `C:/Users/ashutosh.kumar/Desktop/worklogs`

**Layout:**

```
worklogs/
  YYYY-MM/                    # month of the *work day* (step 1)
    YYYY-MM-DD/               # day folder (always - groups re-runs)
      hh-mm_AM.md             # 12-hour clock + AM/PM (local save time; no seconds)
      hh-mm_PM.md
```

Examples:

```
C:/Users/ashutosh.kumar/Desktop/worklogs/2026-07/2026-07-31/03-37_PM.md
C:/Users/ashutosh.kumar/Desktop/worklogs/2026-07/2026-07-31/06-13_PM.md
C:/Users/ashutosh.kumar/Desktop/worklogs/2026-08/2026-08-04/09-02_PM.md
```

**Filename rules:**

- Pattern: `hh-mm_AM.md` or `hh-mm_PM.md`
- `hh` = 01-12 (12 for midnight and noon), zero-padded; `mm` zero-padded
- No seconds in the filename
- Suffix `_AM` or `_PM` (uppercase)
- Examples: 21:02 → `09-02_PM.md`; 00:05 → `12-05_AM.md`; 12:00 → `12-00_PM.md`

**Ordering (required):**

- When listing, migrating, or summarizing a day, sort runs **chronologically**
  (by `saved_at` in front matter, else parse `hh-mm` + AM/PM as real clock time).
- Do **not** rely on filesystem / lexicographic filename sort
  (`01-..._PM` sorts before `11-..._AM`, which is wrong).

**Rules:**

1. Create `worklogs/`, `YYYY-MM/`, and `YYYY-MM-DD/` if missing (`mkdir -p`).
2. Month + day folders = calendar date of the **work day** being summarized
   (not the month of a multi-day range's end unless the user asked for that day).
3. Filename = 12-hour `hh-mm_AM.md` / `hh-mm_PM.md` (see above). Day is
   already in the folder path - do not repeat `YYYY-MM-DD_` in the filename.
4. File body = the exact workflog markdown delivered in chat (title through
   total-duration footer; include spoken shape if you emitted it).
5. Optional YAML front matter at the top (recommended):

```markdown
---
person: Ashutosh
work_day: 2026-08-04
saved_at: 2026-08-04T21:02:15+05:30
skill: where-did-time-go
---

## Workflog — 2026-08-04
...
```

6. After saving, tell the user the path in one short line
   (e.g. `Saved: Desktop/worklogs/2026-08/2026-08-04/09-02_PM.md`).
7. Re-runs for the same day create a **new** timestamped file in that day's
   folder (do not overwrite). If the same minute collides, append `_01`, `_02`.
8. Multi-day requests: one file per day under that day's folder, or one combined
   file only if the user asked for a single view - put it under the end day's
   folder as `range_YYYY-MM-DD_to_YYYY-MM-DD_hh-mm_AM.md` (or `_PM`).
9. Legacy migrations (when touching a day/month):
   - Flat `YYYY-MM/YYYY-MM-DD_HHmmss.md` → `YYYY-MM/YYYY-MM-DD/hh-mm_AM.md`
   - Old day-folder `HHmmss.md` (24h) → `hh-mm_AM.md` / `hh-mm_PM.md`
   - Old `hh-mm-ss_AM.md` → `hh-mm_AM.md` (drop seconds)
10. Helper (optional):

```bash
/c/Python314/python ~/.cursor/skills/where-did-time-go/scripts/save_workflog.py \
  --work-day YYYY-MM-DD --stdin < workflog.md
```

## Guardrails

- Describe work performed, not unverified RCA as fact.
- Only local transcripts under `~/.cursor/projects`.
- If no chats and no commits that day: say so in one line (still optional to
  skip persisting empty runs; do persist if you emitted a real table).
- Persisted files stay on Desktop under `worklogs/` only - do not commit them
  to git repos unless the user asks.

## Daily local automation (11:59 PM)

Unattended local run (not Cursor Cloud Automations - those cannot read local
transcripts).

| Piece | Path / value |
|-------|----------------|
| Generator | `~/.cursor/skills/where-did-time-go/scripts/generate_daily_workflog.py` |
| Wrapper | `~/.cursor/skills/where-did-time-go/scripts/run_daily_workflog.cmd` |
| Windows task | `CursorWorkflogDaily` - daily at **23:59** local |
| Output | `Desktop/worklogs/YYYY-MM/YYYY-MM-DD/hh-mm_AM.md` (or `_PM`) |
| Runner logs | `Desktop/worklogs/_runner_logs/` |

Manual run:

```bash
/c/Python314/python ~/.cursor/skills/where-did-time-go/scripts/generate_daily_workflog.py
# or for a specific day:
/c/Python314/python ~/.cursor/skills/where-did-time-go/scripts/generate_daily_workflog.py --work-day YYYY-MM-DD
```

Notes:

- Auto output is heuristic (timestamps + user queries). Re-run
  `/where-did-time-go` in Cursor when you want a polished table.
- Task must run while the user is logged in (`Interactive` logon).
- If the PC is asleep at 23:59, `StartWhenAvailable` runs it after wake.
