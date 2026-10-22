# 06 - Ops not in Flyway

Credentials never go here. One-liners if pasted to ops.

| Situation | What to do | Prove |
| --- | --- | --- |
| New gateway v2 / `api_usecase_mapping` | **Restart api-gateway** (in-memory + missing-mapping cache) | Call via gateway, not only direct service |
| Partner API 401 `10017` after jar+Flyway ([HDP-8768](https://novopay.atlassian.net/browse/HDP-8768)) | Edit **box** `/apps/novopay-platform-api-gateway/application.properties` skip-list; gateway restart. Not in git | Gateway E2E, not CC-direct |
| New masterdata BKYC key | TaskAlloc config-cache flush or TaskAlloc restart | |
| UAM permission granted, API still 403 | Re-login / hard-refresh. No auth restart | |
| APK BKYC icon after `PRDCT-TASKREQUEST-BKYC` | Agent re-login only | |
| New row in `service_master` (e.g. TASK-ALLOCATION) | **Restart batch**. Cache-miss builds a broken URL with `[` | Batch history `remarks` |
| Entitled corporates by code | `UPDATE ...configuration SET prop_value='CORP0007' WHERE prop_key='trustt.taskallocation.bkyc.entitled.corporate.codes' AND service='TASK-ALLOCATION'` then TaskAlloc flush. Deploy **Actor first** | Codes set + old Actor = empty entitled list (fail closed) |
| Preprod HDP-12000 / similar | Take build of **lib, CC, masterdata** together (his ask to Samyuktha) | |
| Notifications health | Uncomment `management.health.mail.enabled=false` on the box ([DEVOPS-23239](https://novopay.atlassian.net/browse/DEVOPS-23239)) | |
| [HDP-8854](https://novopay.atlassian.net/browse/HDP-8854) | De-dupe preprod `CC_REPORT` rows 9450/9451/9452 | Dropdown options |
| [DPB-2148](https://novopay.atlassian.net/browse/DPB-2148) existing 5 cases | Bank remap 2 submitted ARNs; close 3 unsubmitted (FAIL). SQL via prod change process - he did not run writes | Resume: TICKET_RESUME |
| DPB-2148 Jira attachment | Remove leaked HDFC Authorization/apiKey log; rotate creds ([HDP-12335](https://novopay.atlassian.net/browse/HDP-12335)) | Attachment gone |
| [HDP-12874](https://novopay.atlassian.net/browse/HDP-12874) | Do not ship actor code. DBA; old UAT PANs stay hex | New rows decrypt |
| [HDP-12027](https://novopay.atlassian.net/browse/HDP-12027) | Apply posted SQL on **prod DSA Superset** (not QA). Never write Superset without explicit yes | Dashboard row counts |
| MMI geocode UAT | Seed `hdfc.map.my.india.*` for TASK-ALLOCATION; ship `bankIntegration*` templates; check `common/` logs | `task.customer_lat` |
| QA auto-assign test | Zero agents' non-terminal BKYC tasks first; use real office pins | Cap query in `03` |

Manual Flyway history inserts: pattern in `AGENTS.md`. List of versions he inserted by hand: **[FILL from memory]**.
