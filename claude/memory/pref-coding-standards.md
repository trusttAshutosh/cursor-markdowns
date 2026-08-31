---
name: pref-coding-standards
description: "Coding standards and Deepankar's developer clone — Java/Spring conventions, base+v1/v2, Redis-first, v2 REST"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:31:53.419Z
---

Coding standards + how Deepankar codes (the "developer clone"). Match this voice by default; propose a
different approach only with a clear stated trade-off.

**Why:** consistent, production-ready code that mirrors the existing codebase reduces review friction and
prod risk.

**How to apply:**

General standards:
- Senior-level, modular, single-responsibility, DRY, KISS, production-ready with edge cases handled.
- No deprecated methods/libraries. Performance & scalability first; optimized DB queries (no N+1, select
  only needed columns). Centralized error handling — never swallow exceptions; log with context and
  meaningful error responses. Validate inputs, guard nulls. Structured logging (ERROR/WARN/INFO/DEBUG).
- RESTful: resource URLs, correct HTTP verbs, stateless, proper status codes. SonarQube-clean; Javadoc on
  public APIs; comments explain "why"; keep OpenAPI specs current.
- Stack: Spring Boot microservices, Java 21 baseline (Java 25 on the upgrade branch, see
  [[proj-spring4-java25-upgrade]]). Standard layout: `config/ controller/ dto(records)/ exception/
  filter/ model/ repository/ service/ util/`.

Deepankar's clone (from solo commits — api-gateway `94e3cc3b`, `1af0f1dc`, `e71a0bca`, `6d8ca07d`, `6b348749`):
- **Structure:** shared servlet/filter logic in `filter/base/Base*`; version-specific classes under
  `v1`/`v2`; new cross-cutting behavior extends the base, wired in subclasses. Keep v1/v2 thin.
- **DI:** constructor injection of platform abstractions (`ICacheClient`, cache support); drop libraries
  when platform Redis/cache already covers the case.
- **Solutions:** Redis-first for cache/session/rate-limit; rate limit via Bucket4j + `ICacheClient` (Lua
  INCR, revert on `WRONGTYPE`, fail-closed 429); canonical cache keys; configurable flags for prod parity.
- **Tests:** JUnit + Mockito, colocated mirroring package; update existing test class on contract change,
  new test class per new filter type; tests ride with the behavior change.
- **Commits:** Conventional Commits with scope, small focused diffs; `compileJava` green before push.
- **Naming:** `*Filter`, `*Processor`, `*DAOService`; explicit `v2` suffix when a parallel API exists.

**v2 REST pattern (locked):** new v2 APIs use Spring `@RestController` + `BaseController` /
`BatchInternalBaseController` + DTOs — **not** orchestration XML, `@Processor`, or JTF `templates/.../v2/`.
Path: service `@PostMapping("/apiName")` under `/api/v2` matches gateway tail after `{version}/{service}/`;
camelCase DTOs. SoT: `novopay-platform-lib/infra-platform/docs/v2-rest-api-pattern.md`. References:
`GatewayControllerV2`, `NotificationCenterController`, `WorkflowV2Controller`, `InternalWorkflowController`.

Refresh the clone from `git log --author="Deepankar Sarkar" --no-merges --invert-grep
--grep="Co-authored-by" -n 20 --oneline` (sample 3–5 commits; don't scan full history).

Related: [[pref-working-style]], [[pref-git-workflow]], [[proj-spring4-java25-upgrade]].
