---
name: Gateway KT Playbook
overview: Create a complete, production-oriented KT markdown playbook for the full gateway application, explicitly excluding PDF additions and including multipart-related behavior/changes relevant to ddp-uat, structured for fast onboarding, safe changes, and incident debugging.
todos:
  - id: inventory-surface
    content: Inventory all endpoint groups, filter chains, and external integrations for complete-scope KT.
    status: completed
  - id: map-major-flows
    content: Build sequence diagrams and step/failure tables for each major gateway flow.
    status: completed
  - id: ops-debug-sections
    content: Draft logging, error handling, production issue, and change-impact sections focused on incident debugging.
    status: completed
  - id: safe-dev-onboarding
    content: Create safe development checklist and quick onboarding reading path for new engineers.
    status: completed
  - id: compose-md-playbook
    content: Assemble final KT markdown at repo root with strict requested format and visual structure.
    status: completed
isProject: false
---

# Gateway KT Playbook Plan

## Goal
Produce a single, highly scannable KT document at `[GATEWAY_KT_PLAYBOOK.md](GATEWAY_KT_PLAYBOOK.md)` that enables a new backend engineer to operate, debug, and safely modify this gateway service independently.

## Scope (Complete Application)
- Include all major gateway surfaces and flows currently present in the repository, including:
  - V1 routing and filter chain via `[src/main/java/in/novopay/apigateway/config/FilterConfig.java](src/main/java/in/novopay/apigateway/config/FilterConfig.java)`
  - V1 entry controller `[src/main/java/in/novopay/apigateway/controller/GatewayControllerV1.java](src/main/java/in/novopay/apigateway/controller/GatewayControllerV1.java)`
  - V2 entry controller `[src/main/java/in/novopay/apigateway/controller/GatewayControllerV2.java](src/main/java/in/novopay/apigateway/controller/GatewayControllerV2.java)`
  - Shared gateway/internal/document/proxy/request-forward endpoints in:
    - `[src/main/java/in/novopay/apigateway/controller/GatewayController.java](src/main/java/in/novopay/apigateway/controller/GatewayController.java)`
    - `[src/main/java/in/novopay/apigateway/controller/InternalAPIController.java](src/main/java/in/novopay/apigateway/controller/InternalAPIController.java)`
    - `[src/main/java/in/novopay/apigateway/controller/DocumentController.java](src/main/java/in/novopay/apigateway/controller/DocumentController.java)`
    - `[src/main/java/in/novopay/apigateway/proxy/ProxyController.java](src/main/java/in/novopay/apigateway/proxy/ProxyController.java)`
    - `[src/main/java/in/novopay/apigateway/requestforward/RequestForwardController.java](src/main/java/in/novopay/apigateway/requestforward/RequestForwardController.java)`
  - Exclude PDF-specific additions from KT scope.
  - Include multipart/document-related behavior and ddp-uat operational notes (upload limits, request shape, environment-specific risks) with emphasis on `[src/main/java/in/novopay/apigateway/controller/DocumentController.java](src/main/java/in/novopay/apigateway/controller/DocumentController.java)` and relevant properties in `[src/main/resources/application.properties](src/main/resources/application.properties)`.
- Include configuration, logging, and operational concerns from:
  - `[src/main/resources/application.properties](src/main/resources/application.properties)`
  - `[deploy/application/log/log4j2-spring.xml](deploy/application/log/log4j2-spring.xml)`
  - `[build.gradle](build.gradle)`

## KT Document Structure (as requested)
- `1. System Overview`
  - Purpose, placement in platform architecture.
  - External dependencies table (protocol + criticality).
- `2. High Level Request Flow`
  - Mandatory sequence diagram for Client -> Gateway -> Filters -> Services -> Downstream -> Response.
  - Brief explanation per stage.
- `3. Entry Points`
  - Controllers/endpoints table (method, purpose, downstream calls, risk).
  - Filters table (order, responsibility, critical impact).
- `4. Core Flows`
  - Separate subsections + sequence diagram + numbered steps + failure scenarios table for:
    - v1 API flow
    - v2 API flow
    - proxy flow (`/p/s`, `/p/a`)
    - request forwarding flow (`/forward/**`)
    - document upload/download flow
    - multipart upload/download nuances for ddp-uat
- `5. Authentication & Security Flow`
  - End-to-end auth sequence diagram (token/signature/session/authorization failure branches).
  - Security mechanisms table with risk if broken.
- `6. Configuration`
  - Important properties table (purpose/default/risk), highlighting auth flags, host allowlist, session/rate-limit, CORS, cache.
- `7. Error Handling`
  - Exception-to-HTTP/body behavior mapping table (including 200-with-failure-body pattern where applicable).
- `8. Logging & Debugging`
  - Key logs table (MDC keys: tenant/api-name/stan/user-id/traceId).
  - Practical request-trace debugging steps.
- `9. Testing`
  - Test types table (unit/integration/critical filter tests), current gaps, and disabled-test risk.
- `10. Performance`
  - Bottlenecks table (filter chain cost, downstream latency, cache misses, request log I/O).
- `11. Production Issues`
  - Common issues table with symptoms/root cause/fix.
- `12. Change Impact Analysis`
  - “If you change X” impact table (filter order, auth mode, session timeout, routing conventions, headers).
- `13. Gotchas`
  - Non-obvious behaviors and order dependencies.
- `14. Safe Development Guide`
  - Step-by-step add/modify/test/validate checklist with do/don’t markers.
- `15. Quick Onboarding Path`
  - Recommended reading and hands-on sequence for first days.

## Diagram & Formatting Standards
- Use Mermaid sequence diagrams for all major flows listed above.
- Keep content in bullets and tables (minimal prose).
- Mark risky items with `⚠️` and safe practices with `✅`.
- Include assumptions explicitly where inference is necessary.

## Evidence Mapping (What KT content will be grounded on)
- Filter order and URL patterns: `[src/main/java/in/novopay/apigateway/config/FilterConfig.java](src/main/java/in/novopay/apigateway/config/FilterConfig.java)`.
- Endpoint definitions and method signatures: controller classes in `src/main/java/in/novopay/apigateway/controller`.
- Proxy and forwarding behavior: `[src/main/java/in/novopay/apigateway/proxy/ProxyService.java](src/main/java/in/novopay/apigateway/proxy/ProxyService.java)`, `[src/main/java/in/novopay/apigateway/requestforward/RequestForwardProcessor.java](src/main/java/in/novopay/apigateway/requestforward/RequestForwardProcessor.java)`.
- Security/auth/session details: base filters in `src/main/java/in/novopay/apigateway/filter/base`.
- Runtime properties and logging semantics: `application.properties` + `log4j2-spring.xml`.
- Testing posture: `src/test/java/in/novopay/apigateway/**` (including disabled tests and newly added PDF tests).
- Testing posture: `src/test/java/in/novopay/apigateway/**` (including disabled tests); exclude PDF-addition-focused tests from the KT flow narrative.