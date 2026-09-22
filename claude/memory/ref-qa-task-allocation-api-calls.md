---
name: ref-qa-task-allocation-api-calls
description: "How to curl QA task-allocation v2 APIs: public api-gateway route (no SSH/login) and direct 8022/TLS route, flat body, x-stan and 429 traps, login-to-corporate map incl. bankmaker"
metadata: 
  node_type: memory
  type: reference
  originSessionId: d9860180-f87c-4b3a-a68c-c9b7d3aecca0
  modified: 2026-09-07T13:21:14.625Z
---

Calling `trustt-platform-task-allocation` v2 APIs on QA (verified 2026-09-07).

**Base URL:** `https://localhost:8022/task-allocation/api/v2` — reached via
`python %USERPROFILE%\.cursor\novopay-remote-ssh.py --env qa --cmd '<curl>'`.

- Port is **8022** on QA, not 8020 (8020 is the local/dev port).
- **TLS is mandatory** — plain `http://` returns `Bad Request / This combination of host and port requires TLS`. Use `curl -sk`.
- Mandatory headers, in the order the filter rejects them: `X-Tenant-Code: ddp`, then `X-Stan: <any unique numeric>`, then `X-User-Id: <user.id>`.
- **Body is FLAT**, not the `{request:{...},headers:{...}}` platform envelope. Sending the envelope produces misleading `VALIDATION_FAILED / "<field> must not be null"` errors. Example: `{"pageSize":3,"offset":0,"listType":"UNASSIGNED"}`.
- Pass the payload with `-d @/tmp/file.json` — nested quoting through the SSH `--cmd` string mangles inline JSON and yields the same false "must not be null" errors.
- `getTaskList` `listType` must be one of `UNASSIGNED` / `IN_PROGRESS` / `CLOSED`.

**Verified QA login → corporate map** (`user` → `employee.actor_id` → `employee.corporate_id`, login name in `user_handle.value` where `handle_type_id=7`):

| user.id | login | corporate | type |
|---|---|---|---|
| 19 | `BANKMAKER` | 2 "Tenant" | CORPORATE (UAM_ADMIN) |
| 1392 | `PARVEENMAKER@NOVOPAY.IN` | 10 Manipal | admin |
| 133044 | `RISLCORP@GMAIL.COM` | 166512 RISL | admin |
| 89, 100, 101, 133149, 133154 | — | 26, 42, 43, 166597, 166602 | BFA (field agents) |

Entitled corporates config (`ddp_masterdata.configuration`): `trustt.taskallocation.bkyc.entitled.corporate.ids = 10,166512`.

**`bankmaker` (user 19) IS now a bank-wide login** (superseded 2026-09-15; the older "rejected with 4000088" note is stale). HDP-8930 added `BkycAdminCorporateScope`: a login whose corporate is TENANT gets `BkycAdminScope.allCorporates()`, so user 19 sees every corporate on `getTaskList`/`getEligibleAgentsForTask` and passes the scope check on `updateTaskAssignment` (a non-existent taskId returns `4000058`, not not-entitled — a safe no-op probe).

**UAM on QA (2026-09-15, HDP-11535):** `ddp_authorization` role `ddp_BANKMKR` (id 3, role_group EMPL, ~290 users incl. 19) holds all five `TASK-ALLOC-BKYC-*` perms incl. VIEW + ASSIGN, although V4000133 deletes EMPL VIEW/ASSIGN. The EMPL rows (`role__permission__mapping` ids 45944-45948) are newer than every migration row, i.e. re-granted after the migration (likely a Role Management save). Webapp shows Assign/Re-assign purely on `TASK-ALLOC-BKYC-ASSIGN`. Read-only DB: `python ~/.cursor/novopay-remote-db-readonly.py --env qa --schema ddp_authorization --sql "..."`.

**UAM tree mechanics (HDP-11535, 2026-09-18):** Create Role tree per role group = `role_group__feature__mapping` (feature granularity only); create/update role reject codes outside it with 272015. QA `ddp_BANKMKR` was re-granted VIEW/ASSIGN via a Role Management save (16-09 13:15, user 20). Webapp sidebar is built from the USER permission tree (`getAllPermissionsListForUser`, joins the feature mapping): BKYC menu needs feature code `TASK-ALLOC-BKYC` (`sidebar.data.ts`, `featureApiKeyMapping`), KYC List needs story `TASK-ALLOC-BKYC-CORP`. Moving a story to a new feature code needs a webapp mapping line or the menu disappears.

## Easier route: the public API gateway (no SSH, no login) - verified 2026-09-09

For read APIs the gateway is far cheaper than the 8022/SSH route above:
`https://ddp-qa.trustt.com/api-gateway/api/v2/task-allocation/<api>`, plain `curl` from Windows,
no VPN hop and no portal login. Auth is HTTP `x-*` headers only:

```
TS=$(date +%s%N | cut -c1-13)
curl -sS -X POST "https://ddp-qa.trustt.com/api-gateway/api/v2/task-allocation/getTaskList"  -H "Content-Type: application/json"  -H "x-tenant-code: ddp" -H "x-client-code: NOVOPAY"  -H "x-channel-code: WEB" -H "x-end-channel-code: WEB"  -H "x-stan: $TS" -H "x-transmission-datetime: $TS"  -H "x-operation-mode: SELF" -H "x-run-mode: REAL"  -H "x-function-code: DEFAULT" -H "x-function-sub-code: DEFAULT"  -H "x-user-id: 1392" -H "x-actor-type: EMPLOYEE"  -H "user_id: 1392" -H "function_code: DEFAULT" -H "function_sub_code: DEFAULT"  -d '{"pageSize":50,"offset":0,"listType":"UNASSIGNED","taskType":"BKYC"}'
```

Body is flat here too. `x-user-id: 1392` is Manipal admin `PARVEENMAKER@NOVOPAY.IN` (see map above).

Two traps when scripting a sweep of many calls:

- **`x-stan` must be unique per call** or the gateway replies `12001 Duplicate request found`. A
  millisecond timestamp collides once calls go faster than 1/ms - add a counter, not just `random`.
- **The gateway rate-limits**, replying `429 "You have exhausted your API Request Quota"` in a
  **`response_status`** envelope (snake_case) instead of the usual `responseStatus`. A script that only
  reads `responseStatus` sees no `taskList` and silently records "0 rows", which looks exactly like a
  genuine empty result and will corrupt a test sweep. Always check for both keys and treat 429 as retry,
  and pace bulk sweeps at roughly one call every 2 to 3 seconds.
- Validation failures come back as **HTTP 500** with a normal `responseStatus` FAIL body (for example
  `4000047` bad searchField, `4000048` bad date, `4000045` bad listType, `4000049` bad paging), so
  `urlopen` raises `HTTPError` - read `e.read()` rather than treating it as a transport error.

**Deployed QA frontend** can be diffed against local source without a login: fetch
`https://ddp-qa.trustt.com/portal/`, read the chunk hash map out of `runtime.*.js`
(`f.u=e=>(({...}[e]||e)+"."+{id:"hash"}[e])`), download the chunks and grep. The BKYC admin list
component lives in the lazily loaded chunk, not `main.*.js`.

See [[proj-hdp-7636-bkyc]] and [[proj-task-allocation]].

## Multipart uploads and the agent-side name-match calls (verified 2026-09-09)

- **The api-gateway refuses multipart.** `POST .../api-gateway/api/v2/task-allocation/uploadTaskLeadFile`
  with `-F` returns `UNSUPPORTED_MEDIA_TYPE`, "File and multipart uploads are not supported on this
  path". Lead files must go through the 8022 route: base64 the CSV locally, `echo <b64> | base64 -d >
  /tmp/x.csv` over `novopay-remote-ssh.py --env qa --cmd`, then
  `curl -sk -X POST 'https://localhost:8022/task-allocation/api/v2/uploadTaskLeadFile'
  -H 'X-Tenant-Code: ddp' -H 'X-Stan: <ts>' -H 'X-User-Id: 19' -F 'fileType=LEAD' -F 'corporateId=10'
  -F 'file=@/tmp/x.csv'`. `X-User-Id: 19` (bankmaker) is required: a corporate admin gets `4000088`
  on the upload API. Ingest plus AUTO_ASSIGN completes in a few seconds.
- **curl cannot run from the scratchpad directory** on this machine: Git Bash reports "path longer than
  allowed for a Win32 working directory". Copy the file somewhere short first.
- **Agent app logins are `user_handle.handle_type_id = 6`**, not 7. Manipal field agents:
  user `277` = 9100000005 = agent 147, `133149` = 9100000053 = 166597, `133150` = 9100000058 = 166598,
  `133154` = 9100000070 = 166602.
- **`checkNameMatch` works from both routes** and hits the live HDFC UAT Posidex from QA (no simulator
  row for TASK-ALLOCATION). A matching name scores 100 and **consumes no attempt**
  (`attemptCount = matched ? used : used + 1`), so sending the task's own `customer_name` is a free
  reachability probe. A junk name scores 0 to 6 and spends one attempt; the third failure writes
  `NAME_MATCH_FAILED` and moves the task to `KYC_FAILED`. `KYC_FAILED` cannot be set through
  `updateTaskStatus` (`4000090`), so this lockout is the only way to create that state.
