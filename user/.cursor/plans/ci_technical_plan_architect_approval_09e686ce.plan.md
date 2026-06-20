---
name: CI technical plan architect approval
overview: "A-Z technical plan for architect approval: standardised per-repo CI for all microservices (GitHub Actions), with build-order config, Gradle cache, correct Java version, and cost/time/space optimisation."
todos: []
isProject: false
---

# Technical Plan: Per-Repository CI for Microservices (Architect Approval)

**Document type:** Technical plan for architecture approval  
**Scope:** CI/CD build pipeline for all Novopay/Trustt microservices on GitHub  
**Owner:** Platform / DevOps

---

## 1. Goal

- **Primary:** Provide a single, consistent, and maintainable CI build pipeline that runs on every push and pull request for **each microservice in its own GitHub repository**, ensuring compilation (and optionally tests) succeed before merge.
- **Secondary:** Support building each microservice **together with its dependencies** (e.g. `novopay-platform-lib`) in the correct order, with a **configurable** list of dependency repos so the build order can be changed without editing the pipeline.
- **Non-goals (out of scope):** Deployment, SonarQube/JaCoCo, Docker build/push, or replacing existing Jenkins deploy pipelines unless explicitly decided later.

---

## 2. What (Scope and deliverables)

**In scope**

- **Per-repo workflow:** One GitHub Actions workflow per microservice repository: `<repo>/.github/workflows/build.yml`.
- **Optional build-deps config:** Optional file per repo to declare dependency repos and order: `<repo>/.ci/build-deps.yml`.
- **Build command:** Default `./gradlew clean build -x test`; configurable via one env in the workflow (e.g. `BUILD_CMD`).
- **Java version:** Aligned with project (default Java 21; override per repo where needed).
- **Dependency resolution:** Gradle resolves and downloads dependencies from Maven Central (and other declared repos); no manual “insertion” of dependencies.
- **Cache:** Gradle user home (`~/.gradle/caches`, `~/.gradle/wrapper`) cached via GitHub Actions to reduce build time and network usage.
- **Build order:** Checkout dependency repos (e.g. lib) as per config; then a single Gradle build in the microservice repo (Gradle handles `includeBuild` order).

**Deliverables**

- Workflow template: YAML that can be copied into each microservice repo (or invoked via reusable workflow).
- Optional `.ci/build-deps.yml` schema and example.
- Short README/runbook (e.g. `.github/README-CI.md`) describing where files live, how to change the build command, and how to add/change dependency repos.
- Clarification of “where to add the file”: **inside each microservice repo**, not in a single shared repo (each repo builds itself and its declared dependencies).

**Out of scope (for this plan)**

- Migrating existing Jenkins deploy pipelines.
- SonarQube, JaCoCo, or other quality gates (can be added later as extra steps).
- Docker build/push and deployment.

---

## 3. Why (Rationale and drivers)

- **Consistency:** One pattern for all microservices (GitHub Actions + Gradle + optional deps config) reduces cognitive load and onboarding.
- **PR quality:** Every PR gets an automatic compile (and optionally test) check before merge, reducing broken main/master.
- **Correct build order:** Microservices depend on `novopay-platform-lib` (and possibly others); CI must build “lib then service” without requiring a monorepo. Using Gradle `includeBuild` plus checkout of dependency repos achieves this.
- **Flexibility:** Build command and list of dependency repos are configurable (env + `.ci/build-deps.yml`) so teams can change behaviour without changing pipeline logic.
- **Efficiency:** Caching Gradle dependencies and wrapper reduces runner time and network; optimisation is time-first, then space (see Cost optimisation).

---

## 4. How (Technical approach)

**4.1 Where files live**

- **Workflow:** `<microservice-repo>/.github/workflows/build.yml`. CI runs in that repo’s context (on push/PR to that repo).
- **Config:** `<microservice-repo>/.ci/build-deps.yml` (optional). Lists repos to checkout before building and their paths/refs.

**4.2 Build flow (high level)**

1. Checkout the **current (microservice) repo**.
2. If `.ci/build-deps.yml` exists, **checkout each listed repository** into the specified `path` (e.g. `../novopay-platform-lib`) so that `settings.gradle`’s `includeBuild '../novopay-platform-lib'` resolves.
3. **Set up JDK** (e.g. Java 21) with **Gradle cache** (`cache: 'gradle'` in `actions/setup-java@v4`).
4. Run **one** Gradle command (e.g. `./gradlew clean build -x test`). Gradle builds included builds (e.g. lib) first, then the microservice.

**4.3 Dependency resolution (what gets “downloaded”)**

- Gradle reads `build.gradle` / `settings.gradle` and resolves dependencies from declared repositories (e.g. Maven Central). The workflow does **not** “insert” dependencies; it only runs `./gradlew`. Downloaded artifacts and metadata are stored under **Gradle user home** (`~/.gradle/caches`, `~/.gradle/wrapper`). Caching this directory avoids re-downloading on every run.

**4.4 Cache strategy**

- **What:** `~/.gradle/caches` and `~/.gradle/wrapper` (via `cache: 'gradle'` in setup-java or via `actions/cache` with same paths).
- **When we save:** At end of job (automatic when using `actions/cache` or `cache: 'gradle'`).
- **When we restore:** At start of job, before running Gradle.
- **Eviction:** No explicit eviction; GitHub evicts by LRU when repo cache exceeds 10GB. Cache key can include hash of `**/*.gradle`* and `**/gradle-wrapper.properties` so dependency changes produce a new key; old caches become unused and are evicted over time.
- **Space:** Do **not** cache `build/` or project output; only Gradle’s dependency and wrapper data.

**4.5 Java version**

- Default **Java 21** in the workflow template (matches majority of services). Repos that use 11 or 8 set `java-version: '11'` or `'8'` in their copy of the workflow. No need to parse `build.gradle` in the workflow.

**4.6 Configurable build-deps (`.ci/build-deps.yml`)**

- Schema (logical): `build_dependencies`: list of `{ repository: org/repo-name, path: <path>, ref: branch-or-tag }`.
- **path** must match what `settings.gradle` uses in `includeBuild` (e.g. `../novopay-platform-lib`).
- Workflow (or a script it runs) reads this file and checks out each repo into the given path. If file missing or list empty, only the current repo is built.
- **Changing behaviour:** Teams edit `.ci/build-deps.yml` (add/remove/reorder repos or change `ref`); no workflow edit required.

**4.7 Options: copy workflow vs reusable workflow**

- **Option A:** Copy the same workflow YAML into each microservice repo; set `java-version` and optionally `BUILD_CMD` per repo. Easiest to adopt.
- **Option B:** One “shared” repo with a reusable workflow; each microservice repo has a small workflow that calls it with inputs. Single place to change pipeline logic; requires maintaining the shared repo.

Recommendation: Start with **Option A**; move to **Option B** if centralised pipeline changes become frequent.

---

## 5. Changes (What will change)

- **Per microservice repo (when adopted):**
  - **Add:** `.github/workflows/build.yml` (and optionally `.ci/build-deps.yml`, `.github/README-CI.md`).
  - **No change** to `build.gradle` / `settings.gradle` / source code for the basic build; existing `includeBuild '../novopay-platform-lib'` remains valid provided CI checks out lib at `../novopay-platform-lib`.
- **Existing CI:**
  - **Root monorepo-style workflow** (if present at a single root): No longer used for per-repo builds; each microservice repo gets its own workflow. Any existing root workflow can be retired or repurposed for “full stack” builds if needed.
  - **Jenkins:** No change to existing Jenkins jobs by default; this plan introduces GitHub Actions as the standard for **PR build**. Jenkins can remain for deploy or other pipelines until a separate decision.
- **Process:**
  - PRs to a microservice repo will trigger the new workflow in that repo. Teams may rely on this for “green check” before merge.
  - New repos or new microservices: add the same workflow (and optional config) when onboarding.

---

## 6. Impact

- **Teams:** Each team owns their microservice repo(s). They get a standard, documented way to run CI (and to add/change dependency repos via `.ci/build-deps.yml`) without platform team editing every repo.
- **PR process:** Clear “build passes” signal on GitHub for each repo; reduces broken main/master from compile failures.
- **Risk:** Low. Workflow is additive (new file in each repo). No forced change to existing Jenkins or deployment until explicitly decided. Main risk is misconfiguration of `path` for dependency repos (must match `includeBuild`); documented in runbook and config example.
- **Dependencies:** If `novopay-platform-lib` or another dependency repo is unavailable (e.g. private repo access), workflow must use a token with read access; document token/perms in runbook.

---

## 7. Cost optimisation

**Time (primary)**

- **Gradle cache:** Restore `~/.gradle/caches` and `~/.gradle/wrapper` before build; save at end. Cuts dependency download and Gradle setup time on cache hit (often 1–3+ minutes per run).
- **Single job, minimal steps:** Checkout → (optional dependency checkouts) → setup Java with cache → one Gradle command. No redundant steps.
- `**--no-daemon` (optional):** Avoids Gradle daemon startup in CI; can reduce variance and cleanup.
- **Cache key:** Include hash of gradle files so cache hits when dependencies unchanged; restore-keys fallback for near-hits (fewer full re-downloads).

**Space (secondary)**

- Cache **only** Gradle user home (caches + wrapper), **not** `build/` or project `.gradle`. Keeps cache size and restore time bounded.
- One key prefix + hash per repo limits number of cache entries; GitHub’s 10GB/repo limit and LRU eviction avoid unbounded growth.

**Runner minutes**

- Fewer minutes per run due to cache; same or fewer jobs (one build job per PR/push). No additional scheduled jobs in this plan.
- If moving from Jenkins to GitHub Actions for PR build only, runner cost shifts to GitHub (Actions minutes); compare with current Jenkins runner usage if needed for approval.

---

## 8. Approval checklist (for architect)

- Goal and scope (What/Why) agreed.
- Decision: workflow in each repo (Option A) vs reusable workflow (Option B).
- Decision: default Java 21 and per-repo override acceptable.
- Decision: `.ci/build-deps.yml` as the way to configure “build this and this in this order” (change anytime without workflow edit).
- Cache strategy (what we cache, when we save/restore, eviction) accepted.
- Impact on existing Jenkins and root workflow accepted (additive; no forced Jenkins change).
- Token/access for private dependency repos (e.g. lib) documented and approved.
- Cost optimisation (time first, then space; no `build/` in cache) accepted.

---

## 9. References

- Existing plan (detailed): Per-repo CI with Gradle cache (sections 1–8).
- Current root workflow (monorepo assumption): `.github/workflows/build.yml` (to be superseded per-repo).
- Service example: `novopay-platform-actor/settings.gradle` uses `includeBuild '../novopay-platform-lib'`; Java 21 in `build.gradle`.

