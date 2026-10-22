# 01 - Ownership map

Not a list of PRs. A successor asks **him** for these areas because the trap is tribal. How-it-works is in git.

PR/volume index (do not copy here): [work evidence](https://mdshare.trustt.com/md/s/pbNeFBryyGmF)

## Go-to (walks out with him)

| Area | Why he is the go-to | Reference, do not re-explain |
| --- | --- | --- |
| BKYC auto-assign + ADM1/2/3/6 + assign SMS | Built the path that fills agents; QA "bugs" are often cap / pin / terminal-flag | [HDP-8949](https://novopay.atlassian.net/browse/HDP-8949) tree; tracker `https://mdshare.trustt.com/md/s/RndrcBu-sg6n` |
| BKYC entitled corporates | Switched ops from Actor **id** to admin-portal **code**; bank UAT is not ddp UAT | `07`; [HDP-8930](https://novopay.atlassian.net/browse/HDP-8930); [HDP-12336](https://novopay.atlassian.net/browse/HDP-12336) |
| DIY / unassisted CC | RCA'd same-second ref collision; server-issued ref; 5 prod cases still need bank remap | [DPB-2148](https://novopay.atlassian.net/browse/DPB-2148) `TICKET_RESUME.md` |
| CC KYC Engine cross-service | Multi-repo wiring + log masking + Final DAP switches; bank evidence = real applogs only | [HDP-7350](https://novopay.atlassian.net/browse/HDP-7350) / [HDP-7351](https://novopay.atlassian.net/browse/HDP-7351), [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645), [HDP-12000](https://novopay.atlassian.net/browse/HDP-12000) |
| ETB vs NTB on resume Demog | `50003`/`IPA0=N` is not NTB except D101/D106 | [HDP-12387](https://novopay.atlassian.net/browse/HDP-12387) |
| Consent customer IP | Portal-open IP vs gateway agent IP; CC0005 false same-network | [HDP-5366](https://novopay.atlassian.net/browse/HDP-5366), [HDP-6421](https://novopay.atlassian.net/browse/HDP-6421) |
| LOC PE-PQ / HIBVPRD | Bank workbook is **not in git**; MEMO-LINE5 layout | `03`; [HDP-7076](https://novopay.atlassian.net/browse/HDP-7076), [HDP-8565](https://novopay.atlassian.net/browse/HDP-8565) |
| Admin portal UAM reports | SQL lives only on **prod DSA Superset**, not in any repo | [HDP-12027](https://novopay.atlassian.net/browse/HDP-12027) |
| CC Excel masters via Masters Mgmt | JAR replacement; masters-mgmt SoT is `ddp-qa` (no `ddp-prod`) | [HDP-12841](https://novopay.atlassian.net/browse/HDP-12841) |
| Partner CC status pull (Blostem) | Mapping still needs bank sign-off; gateway skip-list is **on the box**, not in git | [HDP-8768](https://novopay.atlassian.net/browse/HDP-8768) |
| Agent OS (Cursor, Bob, remote-db, rules) | He built it; `AGENTS.md` is the SoT | `08`; `BOB_GUIDE.md` |
| Flyway / common-scripts / TaskAlloc exception | Collision history; TaskAlloc DDL not in the JAR | `AGENTS.md`; [HDP-8967](https://novopay.atlassian.net/browse/HDP-8967) |
| Product onboarding doc + mdshare sync | Master copy in CC repo; mdshare id must stay in sync | `https://mdshare.trustt.com/md/s/7NmufeEoyqRx` |

## He unblocks, does not own the code

| Area | Owner | What he actually holds |
| --- | --- | --- |
| BKYC ingest / ADM7 / close file / Superset MIS | Abhishek (`trustt-abhishek`) **leaving** | Clarifications (e.g. [HDP-10501](https://novopay.atlassian.net/browse/HDP-10501)); not the file parser |
| BKYC service spine / consent APIs | Deepankar | Tracker + PR template; Grafana epic [HDP-11496](https://novopay.atlassian.net/browse/HDP-11496) is Deepankar's, Phase 1 moved to Dinesh |
| Agent list / bio / submit | Harini | |
| Add-on CASE-NBR / cust id | Gowtham | He diagnosed blank CASE-NBR = no stored cust id ([HDP-12325](https://novopay.atlassian.net/browse/HDP-12325)) |
| eKYC log masking in lib | Sanooj assignee | He drove preprod merge notes ([HDP-11645](https://novopay.atlassian.net/browse/HDP-11645)) |
| Jenkins TaskAlloc env | Arnold | Asked UAT setup ([DEVOPS-22139](https://novopay.atlassian.net/browse/DEVOPS-22139)) |

## Repos he lives in (for restore, not a PR count)

CC, lib, masterdata, TaskAlloc, actor, gateway, notifications, initial-setup, consents, authorization, batch, banking-origination, masters-mgmt, bob-the-builder, `Desktop/novopay`, `Desktop/cursor-markdowns`.
