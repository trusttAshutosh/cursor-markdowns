---
name: onboarding-doc
description: >-
  Use when writing or revising an onboarding guide for a new joiner, about a
  product, platform, service, or any other topic. Also when the user asks for
  a plain-English visual guide, a day-1 reading path, read-and-grasp times, or
  a pass that reads the guide as a new joiner until only Good is left.
---

# Onboarding doc

Write a guide a new person can grasp, not a reference dump. Visual first. One picture is the one to remember. Times are for a real first read.

Worked example of this shape: `docs/guides/product-onboarding.md` in `trustt-platform-creditcard-management` (CC, LOC, AOC, ESO). Copy the shape. Do not copy that product into a guide about something else.

## When not to use

API field specs, RCA, Jira comments, and code review have their own formats. Do not turn those into this guide.

## Before writing

1. Name the readers. Default is developer, QA, and product. Ask only if a different set would change the day-1 path.
2. Read the source of truth the user names (code, spec, or an existing doc). Do not write from memory.
3. Do not invent. If the source does not spell out an acronym, do not spell it out. If you checked a fact for one product, do not claim it for the others. If you did not verify an API path, do not name one.
4. Agree the file path before drafting. Default is `docs/guides/<topic>-onboarding.md` in the repo that owns the topic. One copy. No Desktop duplicate.

ASCII hyphens only. No class names, file names, or code in the guide. Names the team says out loud (an API, a status, a role) are allowed.

## Shape

```markdown
# <Topic> - Onboarding

For <readers>. Plain English, visual first. Start at the next section. Where this file lives is at the end.

**Time to read and grasp,** not a skim. Follow each diagram and read each table row.

| Read | Time |
|---|---|
| Full guide, including this opening and the closing note | <sum> |
| Part A, sections 1-N | <sum of Part A> |
| Part B, sections ... | <sum of Part B> |

## Start here

**Read: <n> min.** The bullets are the short picture. This time is for grasping them, plus who should read what, and the contents.

### The topic in one minute

- <what this thing is, and who decides>
- <the products or parts, each in a few words>
- <the people, and which screen they use>
- <the shared rhythm>
- <the one distinction people get wrong>
- <what controls access>

### What to read

| You are | Day 1 | Time to grasp | Look up when needed |
|---|---|---|---|
| Developer | Start here, Part A, then <lookup sections they need on day 1> | <sum> | <section numbers> |
| QA | Start here, Part A, then <their day-1 extras> | <sum> | <section numbers> |
| Product | Start here and Part A | <sum> | <section numbers> |

### Contents

**Part A - Understand - <part time>**

1. The big picture - <min>
2. Who is who - <min>

**Part B - Reference - <part time>**

## Keeping this doc

**Read: 1 min.**

**Source:** <what you read, and the date>.
**Master copy:** <path>.
```

Part A is what you must understand. Part B is lookup. Day 1 is Part A plus only the Part B sections that role cannot work without. Everything else is "look up when needed".

Under every `# Part` and `##` section, on its own line:

`**Read: <n> min.**`

The contents list and the heading line use the same number. When a section changes, recompute that section, the part sum, the role sums, and the full-guide sum.

## How to write a section

- Open with the picture (mermaid) or the table. Prose is the sentence the picture cannot say.
- One journey, one flowchart, and that is the one to remember. A sequence or a stage table stays only if it answers a different question. Put one line above it: why it exists ("who talks to the bank", "the APIs and what each step stores").
- The usual case goes in the day-1 table. Send the reader to a later section only when the answer really depends. Do not send the common case there.
- A long code list, a tag list, or a chain they must not memorize gets one line: skip on day 1, open it when a case mentions it.
- The opening, the word list, and the confusions table must say the same thing. If a later section is more precise, fix the earlier sentence. Do not leave both.
- A confusions table is pairs of "people often think" and "actually". Use it for the mistakes that waste a first week.
- Status stays a sentence under the stage table. Do not add a status diagram that draws a loop on top of another arrow.

## Read times

Times are to read and grasp, not to skim.

| Unit | Time |
|---|---|
| Prose outside tables and diagrams, new terms | 100 words per minute |
| A diagram the reader must trace | 2 min (1 min if the text says skip it) |
| A dense flowchart (many decisions) | 4 min |
| A table data row | 20 seconds |

Round each section to the nearest minute. Minimum 1 minute. Part time and role time are the sums, not a round number you pick first. Show hours and minutes when the sum is over 60 (`1 hr 23 min`). The full guide includes the opening and the closing note.

## Joiner loop

After a draft, and again after every revision, do this from scratch. Do not stop after one pass.

1. Read as a new joiner who has not seen the source. For each part, mark Good, OK, or Bad, with a reason.
   - **Bad:** a contradiction, or they have to stop and ask.
   - **OK:** they can finish, but something still slows them (a repeat with no reason, a usual case sent to a later section, one word used two ways).
   - **Good:** they can grasp it and move on.
2. As an old member, change only what is Bad or a stalling OK. Do not add chapters. Do not lengthen day 1.
3. Read the new text from scratch. Stop when that pass is only Good.

Hunt for these stalls first:

| Stall | Fix |
|---|---|
| The opening says an outside system is not called, then a later picture shows a call | Split "not sent" from "a check that does call" |
| The same journey appears three times | Keep one as the picture to remember. Label the others |
| The day-1 table sends the usual case to a later section | Put the usual answer in the day-1 table |
| A word means one thing in the word list and another in the journey | Make the later, precise sentence the one used everywhere |
| A diagram hides a label on top of another | Drop the diagram. One sentence under the table |

## Publish

- Do not mention this skill inside the guide. The guide is for people. Point agents at this skill from the repo agent index only.
- Do not commit, push, or open a PR unless the user asks.
- Do not create a second mdshare doc.
- If the file is `docs/guides/product-onboarding.md` in credit-card-management, also follow `.cursor/rules/onboarding-doc-mdshare-sync.mdc` (full-file mdshare draft, and the open PR preview). For any other topic, publish only when the user asks.
