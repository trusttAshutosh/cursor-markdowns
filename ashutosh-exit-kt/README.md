# Ashutosh Kumar - exit KT

**Live folder:** `C:\Users\ashutosh.kumar\Desktop\ashutosh-exit-kt`  
**Git backup:** `Desktop/cursor-markdowns/ashutosh-exit-kt` (repo `trusttAshutosh/cursor-markdowns`)  
**Started:** 2026-10-22  
**Last updated:** 2026-10-22

This is the KT Ashutosh must give if he leaves. It is **not** an architecture dump. Git, Jira, `AGENTS.md`, and Bob docs already explain how the code and agent OS work.

## What belongs here

Only what **AI cannot reconstruct** after he is gone:

- Verbal promises with bank / product / QA that never landed in a ticket
- Landmines he already paid for (symptom, wrong fix, real fix, how to prove)
- Unfinished threads (local branches, on-hold tickets, DMs, unpublished SQL)
- People and access that die with his laptop
- One-off ops he ran by hand (not Flyway)
- Why a decision was made, including rejected alternatives

## What does not belong here

- Class walkthroughs, API field tables, orchestration XML
- Copy-paste of `AGENTS.md` / `BOB_GUIDE.md` / product onboarding
- Passwords, tokens, `.env` contents (point at the file, transfer access)

## How a successor should use this

Three recorded 45-min sessions. Ashutosh talks, successor types.

1. **BKYC assign + admin + SMS + Cursor/Bob OS** (`01`, `08`)
2. **CC / KYC Engine / current WIP** (`03`, `04`)
3. **People, access, hand-run SQL, unwritten promises** (`02`, `05`, `06`, `07`)

Exit test: successor can (a) explain auto-assign caps and visit-owner id without pinging him, (b) run a QA SELECT via the remote-db helper, (c) say which current tickets are still his.

## Files

| File | Contents |
| --- | --- |
| [01-ownership-map.md](01-ownership-map.md) | What walks out with him vs what is already in git |
| [02-promises-unwritten.md](02-promises-unwritten.md) | Bank / product / QA verbal agreements |
| [03-landmines.md](03-landmines.md) | Looks correct, still fails |
| [04-unfinished.md](04-unfinished.md) | Alive / dead / waiting |
| [05-people-and-access.md](05-people-and-access.md) | Who to ping; access to transfer |
| [06-ops-hand-run.md](06-ops-hand-run.md) | SQL / flushes / reprocess steps not in Flyway |
| [07-decision-journal.md](07-decision-journal.md) | Why, including rejected alternatives |
| [08-cursor-bob-os.md](08-cursor-bob-os.md) | Agent OS he built; do not re-explain Bob from scratch |
| [_template-entry.md](_template-entry.md) | Paste shape for a new bullet |
| [CHANGELOG.md](CHANGELOG.md) | Dated appends |

## How agents keep this alive

Personal skill: `~/.cursor/skills/ashutosh-exit-kt/SKILL.md`

When a session surfaces a durable unwritten fact, **append** it to the matching file. Add one line to `CHANGELOG.md`. Do not rewrite the whole folder.

## Already written elsewhere (link, do not copy)

- Agent operating rules: `Desktop/novopay/AGENTS.md`
- Cursor + Bob team KT: `Desktop/novopay/bob-the-builder/docs/BOB_GUIDE.md`
- BKYC journey tracker: `https://mdshare.trustt.com/md/s/RndrcBu-sg6n`
- Product onboarding (CC/LOC/AOC/ESO): `novopay-platform-creditcard-management/docs/guides/product-onboarding.md` (mdshare `https://mdshare.trustt.com/md/s/7NmufeEoyqRx`)
- Laptop migrate of agent config: `Desktop/cursor-markdowns`
