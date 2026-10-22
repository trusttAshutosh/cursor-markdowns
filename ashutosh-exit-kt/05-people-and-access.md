# 05 - People and access

From tickets he actually unblocked. Not an org chart.

## People

| Need | Who | Why him |
| --- | --- | --- |
| Merge / BKYC spine / Grafana epic | Deepankar Sarkar (`deepankar-np`) | Merges his QA PRs; [HDP-11496](https://novopay.atlassian.net/browse/HDP-11496) owner |
| DPB-2148 bank remap, HDP-12841 product, add-on CASE-NBR | Gowtham Kumar Reddy | PO on those; tagged on DPB-2148 existing-data |
| BKYC ingest / close file / ADM7 | Abhishek Puranik (`trustt-abhishek`) | **Leaving** - get KT now |
| Agent APIs / bio / submit | Harini (`Harini-Trustt`) | |
| Preprod builds (lib, CC, masterdata); HDP-12036 consent error text | Samyuktha S | He asked her to take those builds. Preprod DB helper user is also `Samyuktha` |
| UAT decrypt function / DBA | `rprabhakar` | Recreated `platform_master.decrypt` 2026-10-15 by hand |
| HDP-12874 reporter; BKYC admin FE; UAM bank VIEW drift | Arvind R | [HDP-11743](https://novopay.atlassian.net/browse/HDP-11743), [HDP-11535](https://novopay.atlassian.net/browse/HDP-11535) |
| eKYC log masking | Sanooj M P | [HDP-11645](https://novopay.atlassian.net/browse/HDP-11645) |
| TaskAlloc Jenkins UAT | Arnold Smith E | [DEVOPS-22139](https://novopay.atlassian.net/browse/DEVOPS-22139) |
| Notifications mail health on box | Nusullapalli Srinu | [DEVOPS-23239](https://novopay.atlassian.net/browse/DEVOPS-23239) uncomment `management.health.mail.enabled` |
| Grafana Phase 1 now | Dineshkumar A B | Do not duplicate |
| DIY FE (no change) | Manohar Rudhravaram, Ranesh Suthar | Named on DPB-2148 414213 |
| DPB-2148 prod data / remap | Santhosha KR | Tagged on 414044 |
| Superset FD journey | Saumyaranjan Pradhan | [HDP-11011](https://novopay.atlassian.net/browse/HDP-11011) |
| Blostem / CC status mapping sign-off | Bank product (name [FILL]) | [HDP-8768](https://novopay.atlassian.net/browse/HDP-8768) |
| Bank UAT BKYC ops | [FILL] | Only they can run writes; `supersetreadonly` is SELECT only |
| DSA corporate approve 12001 | Hareesha Balarajappagari | [DPB-2145](https://novopay.atlassian.net/browse/DPB-2145) |
| First-time agent reactivation 220000 | Kavya Lingutla | [HDP-11386](https://novopay.atlassian.net/browse/HDP-11386) |
| Hide DB details in report errors | Prabhakar Reddy Mukkadaiah | [HDP-8209](https://novopay.atlassian.net/browse/HDP-8209) |
| GitHub / Jenkins / VPN access | S M Bhupathi, Lokeswara Reddy Valleti | DEVOPS tickets he opened |
| Firestore UAT soak | Sanooj M P | Also [HDP-11796](https://novopay.atlassian.net/browse/HDP-11796) assignee |
| Do **not** write Jira via MCP | Deepankar's Atlassian login | Connector + Browser 1. Drafts only. |

## Access (point, do not copy secrets)

| Access | Where | Trap |
| --- | --- | --- |
| QA / UAT / preprod DB + SSH + Superset | `%USERPROFILE%\.cursor\novopay-remote-db.env` | Sync to cursor-markdowns **excludes** this file |
| Preprod DB | same helper `--env preprod` user Samyuktha | **No** grant on `ddp_task_allocation` or `platform_master` |
| Bank UAT DB | **He has none** | Only pasted SELECT output |
| Prod DSA Superset | `https://ddp-superset.novopay.in` (DDP). DSA URL is **manual**, not Flyway | He cannot apply HDP-12027 there |
| QA/UAT Superset | same live instance; UAT MySQL `ddp_superset` is stale | Write only with explicit yes |
| Jira / BKYC Chat webhook | `%USERPROFILE%\.cursor\bkyc-jira.env` | Chat is stopped |
| mdshare PAT | Cursor `mcp.json` | Needed to pull Grafana mdshare docs; never print |
| GitHub | `trusttAshutosh` | |
| cursor-markdowns | `trusttAshutosh/cursor-markdowns` | Who pushes after he leaves: [FILL] |
| LOC bank workbook | `Downloads\LOC APIs mapping v 0.1 (2).xlsx` | Not in any repo |
| Jira in this Cursor | Atlassian MCP = **Deepankar** | Never write. Paste from Ashutosh browser |
| QA Redis | tomcat account on app box | Normal SSH user: connection refused on 6379 |

Transfer access **before** last day. Rotate anything that was only his SSH key.
