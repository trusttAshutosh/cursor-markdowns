# 06 - Ops he ran by hand

SQL, Redis/JTF flushes, reprocess steps, manual `flyway_schema_history` inserts. If it is in Flyway, it does not belong here.

**Never store credentials.** Fully qualified `schema.table`. One-liners.

Share format if this pack is pasted to ops: `.cursor/rules/sql-query-share-format.mdc`.

---

## Manual Flyway history inserts

Pattern (checksum must match the built script or boot validation fails):

`INSERT INTO \`schema\`.\`flyway_schema_history\` (...) SELECT ... WHERE NOT EXISTS (... version ...);`

List versions he inserted by hand:

| Env | Schema | Version | Why | Date |
| --- | --- | --- | --- | --- |
| [FILL] | | | | |

## Config keys he changed on env without a deploy

Masterdata `configuration` UPDATEs (key exists; value drifted).

| Env | `prop_key` | Why | Ticket |
| --- | --- | --- | --- |
| [FILL] | | | |

## Reprocess / repair playbooks (not in git)

| Situation | Steps (plain English) | Prove |
| --- | --- | --- |
| Failed BKYC ingest file | [FILL - may be Abhishek] | |
| Auto-assign missed a pin-matched agent | [FILL] | |
| Assign SMS did not send | [FILL] | |
| Gateway v2 401 until restart | `api_usecase_mapping` is in-memory; **api-gateway restart** | |
| TaskAlloc config not picking new masterdata key | config-cache flush or TaskAlloc restart | |
| UAM permission granted but API still 403 | re-login / hard-refresh; no auth restart | |

## Redis / JTF / cache

- [ ] Any key patterns he flushes by hand
- [ ] Any "delete this session key" he told QA

## [FILL] last 90 days

Dump from memory: anything he ran on QA/UAT/preprod that is not Flyway.
