---
name: ref-qa-server-access
description: How to read QA app-server logs and QA DB from this machine - log paths, SSH route (password via paramiko, key auth is refused), log line format, and what each service log contains
metadata:
  type: reference
---

**QA app server** `np-ddp-qa-app.novopay.in` (172.31.2.132, IST clock). Connection details live in
`~/.cursor/novopay-remote-db.env` (`QA_SSH_*`). **Key auth is refused** (`Permission denied
(publickey,password)`), so the `ssh_base()` helper in `~/.cursor/novopay-remote-db-readonly.py`
cannot log in; use the password with **paramiko** (`pip install paramiko`, user-level, verified
2026-09-07): `SSHClient.connect(host, username, password, look_for_keys=False, allow_agent=False)`.
No `sshpass`/`plink` on this machine.

**Log layout** (`/apps/applogs/<tenant-or-kind>/<service>-<kind>.log`, rotated daily into
`/apps/applogs/<kind>/archived/archived-logs-YYYY-MM/<service>/YYYY-MM-DD-<service>-<kind>-1.log.gz`):
- `ddp/task-allocation-ddp.log` - controller DEBUG lines (`getAgentTaskList | agentId=… listType=…`),
  full response bodies, `GlobalExceptionHandler` errors. The line format is
  `[ts] [service] [LEVEL] [class] [tenant] [api] [stan] [userId] msg`; agent-app STANs are bare
  epoch-millis, portal STANs are `<userId>_<millis>`.
- `ddp/api-gateway-ddp.log` - every inbound API with headers (device id, channel, referer), so it
  shows *who* called from *where* (AGENT_APP vs WEB portal).
- `ddp/actor-ddp.log` - login; `token key for user id <userId> is <agentCorpId>_<userId>` maps an
  app user to its agent (corporate) id.
- `common/`, `perf/`, `es/` - same per-service split; `common` was empty for the 4000005 case.

**QA DB** (`np-ddp-qa-db.novopay.in`, user `mugesh`, direct TCP, `QA_DB_VIA_SSH` false) works via
`python ~/.cursor/novopay-remote-db-readonly.py --env qa --schema <schema> --sql "<SELECT>"`
(verified 2026-09-07 12:20 IST; an `ERROR 1045` seen earlier the same day was transient).
Read-only by tool design; Ashutosh has no write grants either - see [[proj-hdp-7636-deferred-qa-tests]].

**Useful joins:** agents are `ddp_actor.corporate` rows (`code` = RF-number, `parent_id` = 10 Manipal);
agent app users are `ddp_actor.user`; task history is `ddp_task_allocation.task_status_history`
(`change_source` AGENT_MOBILE / AUTO_ASSIGN / updateTaskAssignment, `actor_id`) and
`task_assignment` (`is_active`, `unassigned_on`). Local snapshots of older logs sit in
`novopay/SERVER_LOGS/` (stale - last pulled 2026-09-04).

Related: [[ref-machine-commands]], [[proj-task-allocation]].
