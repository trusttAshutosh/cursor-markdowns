---
name: proj-spring4-java25-upgrade
description: "ddp-fea-spring4-java25-upgrade branch — Spring Boot 4 / Java 25 / Gradle 9 fleet upgrade, catalog, gotchas"
metadata: 
  node_type: memory
  type: project
  originSessionId: 755481cc-2faf-4a57-8ad0-da97b5f87585
  modified: 2026-08-13T10:33:56.901Z
---

Fleet upgrade line **`ddp-fea-spring4-java25-upgrade`** (renamed from `…java24…` on 2026-07-15) vs
`ddp-prod`. Canonical detail: **`novopay-platform-lib/docs/changelog.md`** (prefer over re-diffing 600+
files). Service checklist example: `novopay-platform-batch/docs/UPGRADE-JAVA24-SPRINGBOOT4.md`. State
current as of 2026-08-10.

**Stack delta** (source of truth: `novopay-platform-lib/gradle/libs.versions.toml`):
| | ddp-prod | this branch |
|---|---|---|
| JDK | 21 | **25 LTS** (26 is feature-only) |
| Spring Boot | 3.5.x | **4.1.0** |
| Gradle | 8.x | **9.6.1** |
Catalog pins: jakarta.persistence 3.2, jakarta.servlet 6.1, Jackson 2.18+/jackson3 3.1, grpc-bom 1.0.2,
aws-sdk-bom 2.29.0, mysql-connector 9.4, Lombok 1.18.44, Foojay resolver matched in settings. Android
modules of `digi-distribution-app` stay on **Java 21** (Android toolchain) — by design.

**What landed beyond version bumps:** Kafka Boot-4 health contributor + metrics + property aliases + DLQ
hardening (`infra-message-broker`); gRPC Resilience4j on masterdata/notifications clients + spring-grpc 1.1
starters; `RestClient` in `infra-api-client`/gateway + STAN/correlation MDC; Redis hybrid JSON/JDK
serializer; OpenTelemetry / log correlation with **Elastic APM removed**; `infra-logging` +
`LogMaskingRuleContributor` SPI; SonarLint (not SQ scanner); AWS SDK **v2** everywhere (drop
`com.amazonaws`), Jackson-3 sweep (`tools.jackson.*`, keep `com.fasterxml.jackson.annotation`).

**Boot-4 migration gotchas (fixed):**
- **EnvironmentPostProcessor:** implement `org.springframework.boot.EnvironmentPostProcessor`; register
  ONLY via `META-INF/spring/org.springframework.boot.EnvironmentPostProcessor.imports`. Never under legacy
  `spring.factories` key (assignability abort — Nacos/Kafka EPP class failure).
- **AsyncConfigurer + `@Bean`:** don't add extra `@Bean` methods (e.g. `TomcatProtocolHandlerCustomizer`)
  on a `@Configuration` that implements `AsyncConfigurer` — Boot 4 may invoke the factory on the async
  configurer (gateway crash; split into a separate config class).
- Health → `boot.health.contributor`; `AutoConfiguration.imports` not `spring.factories`;
  `BeanDefinitionBuilder` not `GenericBeanDefinition`; drop remaining `javax.*`. Flyway 12 (BOM 12.4.0),
  starter exclude pattern unchanged.

**IST timestamps decision (2026-08-10):** evidence columns are **`DATETIME`** (zone-less, stores literal
digits), so **migrate `Instant` → `LocalDateTime`** to mirror the column. Config-only
`hibernate.jdbc.time_zone` was **rejected** (invisible, lost via override, reverts to UTC). Prod parity:
`new Date()` + IST JVM ≡ `LocalDateTime.now()`. Pilot done on limits (main 0 errors; 64 tests use
`Instant.EPOCH` fixtures; repo-local `ExecutionContextDates.resolveLocalDateTime`). Remaining `Instant`
field counts to migrate: actor 120, accounting 49, masterdata 29, gateway 14, notifications 10,
creditcard 8, consents 4, approval 4, authorization 3, batch 2, complaint 2; zero in banking-orig/
banking-txn/dms/india-stack/limits/term-deposit. Lib `JavaTimeDateConvert` left unchanged on purpose
(2 callers: actor email validation + onboarding history — fix during actor migration to return
`LocalDateTime`). Interim risk: unmigrated repos still write UTC digits.

**Fleet:** ddp-prod merge completed Jul 2026 across microservices; prod tip synced. Not on branch:
`callbacks`, `ddp-microfrontend-aeps` (no ddp-prod). Merge rules: take upgrade catalog + toolchain, replay
feature-only deps on top, fix HealthIndicator imports first, plugins block (no `get`, no GString),
`compileJava` then test on JDK25 runtime. Conflict hotspots: `libs.versions.toml`, wrapper/
`gradle.properties`, root+module `build.gradle`, `settings` foojay/includeBuild, `AutoConfiguration.imports`.

When changing existing prod behavior on this line, still ask backward-compat vs `origin/ddp-prod`
([[pref-git-workflow]]). Infra jar version bumps: [[ref-flyway-infra-versioning]].
