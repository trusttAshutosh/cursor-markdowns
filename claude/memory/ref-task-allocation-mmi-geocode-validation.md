---
name: ref-task-allocation-mmi-geocode-validation
description: How to validate task-allocation MapMyIndia customer geocoding on QA/UAT (HDP-11732) and the UAT MDC-loss trap that makes it fail open
metadata:
  type: reference
---

Validating the BKYC customer map pin (HDP-11732, PRs #94/#95, commit `89ef012`, deployed QA 17:07 / UAT 17:09 on 2026-09-22):

- **Is the fix deployed:** jar is `/apps/novopay-platform-task-allocation/task-allocation-1.0.0.SNAPSHOT.jar`;
  `unzip -l <jar> | grep 'TaskCustomerGeocodeService$LatLng'` (1 = fixed build).
- **Trigger:** only rows with `customer_lat IS NULL` get geocoded (stored coords are never redone). Call
  `getAgentTaskList` as the task's agent over 8022 (`X-User-Id` = agent app user; agent -> user via
  `ddp_actor.employee.corporate_id` join `user.actor_id`). QA 166602=133154, 166556=133099; UAT 31991=32536.
- **Read result:** `ddp_task_allocation.task.customer_lat/lng` + log lines `Address geocode for taskId=... is not
  inside pincode` / `Geocoded customer coordinates`. QA 2026-09-22: 921303 (580001) -> Hubli, 921293 (518302) ->
  Adoni AP, 921298 Bellandur kept street-level: pass.
- **UAT trap:** first MMI call after a restart missed the config cache, the gRPC config fetch hit
  `DEADLINE_EXCEEDED`, and the request MDC was wiped (later lines go to `/apps/applogs/common/task-allocation-common.log`
  with `[] [] [] []`). With tenant null, MMI calls fail (`No bean named 'redisTemplatenull'`, OAuth exception) and the
  geocoder fails open to the unverified address point (UAT task 5 stored Udupi for pincode 580001). Always check the
  common log too, not only `ddp/`.
- **Root cause (lib):** `infra-essentials-grpc` `LoggingClientInterceptor.onClose` does `MDC.clear()` in `finally`,
  so ANY gRPC call in a request (config cache miss -> masterdata GetConfigurations, OK or not) wipes tenant/STAN.
  UAT has no TASK-ALLOCATION `hdfc.map.my.india.*` rows, so `latlong.operation.name` misses (NOT_FOUND) mid-request.
  MapMyIndia token cache reads the tenant from ExecutionContext `tenant_code`, which the geocoder copies from MDC.
  Re-test 2026-09-22 17:20 (UAT task 9): REVGEOCODE worked (13.3 s, returned another pincode), then the pincode
  geocode failed on tenant=null and task 9 went back to Bangalore.

Related: [[ref-uat-task-allocation-api-calls]], [[ref-qa-task-allocation-api-calls]], [[proj-task-allocation]].
