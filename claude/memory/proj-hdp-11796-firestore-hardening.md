---
name: proj-hdp-11796-firestore-hardening
description: "HDP-11796 Firestore dead-connection fix - decisions, branch/worktree layout, compat rules, what is left (UAT AC, promotion, actor flag)"
metadata:
  node_type: memory
  type: project
  originSessionId: f8282129-7a24-4443-9056-833f6d16bade
  modified: 2026-09-28T06:03:21.200Z
---

HDP-11796 (UAT incident 24 Sep 2026: consents co-browsing `secure-channel` hung 60 s and returned 503 for
~15 min because the Firestore gRPC connection went silently dead; no keepalive, unbounded `ApiFuture.get()`).

**State 2026-09-28 (afternoon): committed, pushed, 6 PRs open (feature -> env, bkup not needed, all MERGEABLE):**
| Repo | QA PR | UAT PR | Head |
| --- | --- | --- | --- |
| trustt-platform-lib | #6785 | #6786 | `ddp-fea-hdp-11796-firestore-keepalive` (base = merge-base(ddp-qa, ddp-uat) 87a9a60df0, firestore module; pushed with `NOVOPAY_GIT_HOOK_SKIP_PROD_SYNC=1` because the split is not on prod-master) |
| trustt-platform-consents | #3268 | #3269 | `ddp-fea-hdp-11796-firestore-keepalive-prod` (old prod-master d323ce72f base, clean into both envs) |
| trustt-platform-actor | #18539 | #18540 | `ddp-fea-hdp-11796-firestore-keepalive-prod` (old prod-master 1d9247bef0 base, clean into both envs) |
GitHub repos were renamed `trusttai/trustt-platform-*` (old khoslalabs/novopay-platform-* URLs redirect).

**Prod line moved under us:** lib and actor `origin/ddp-prod-master` were fast-forwarded to `ddp-prod` on 2026-09-28 (lib f208051481 = Boot 4 catalog but NO firestore split, firebase module 0.0.1.RELEASE; actor 2d0d0e2093). Consents prod-master unchanged (Boot 3 d323ce72f). Merging new prod-master into ddp-qa/uat conflicts on unrelated files (45 lib / 74 actor prod-only commits), so QA/UAT heads stay on the old bases. Prod PR heads prepared but NOT pushed: local branches `ddp-fea-hdp-11796-firestore-keepalive-pm` in `.wt-11796-pm/novopay-platform-lib|actor` (cherry-picked onto new prod-master, lib 22 tests green, actor compiles). Remote lib `...-prod` branch (old base) is stale once the pm branch is pushed. Scratch Boot 4 worktrees `.wt-11796-b4/*` (consents/actor branches `hdp-11796-b4-scratch`) can be removed.

Original worktrees (old prod-master base, commits 38d47a33ea lib / 57f423877 consents / 949040abaa actor):
- `C:\Users\ashutosh.kumar\Desktop\novopay\.wt-11796\novopay-platform-lib` (module `infra-essentials-firebase`,
  version 0.0.1.RELEASE -> 0.0.2.20260928.RELEASE; new `FirestoreClientSettings`, `FirestoreOptionsFactory`,
  `FirestoreUnavailableException`; `FireStoreUtils.awaitResult` + `isRetryable`; 4 test classes, 22 tests green)
- `...\.wt-11796\novopay-platform-consents` (`FirebaseCoBrowsingService` opt-in + retry-once, lock TTL in
  `FirebaseCoBrowsingSecureChannelService.channelLockTtlMillis()`, `cc.cobrowsing.firestore.*` props; 16 tests green)
- `...\.wt-11796\novopay-platform-actor` (`FirebaseGeoLocationService` opt-in knobs `agent.geo.location.firestore.*`, default OFF)
Sibling layout matters: consents/actor `settings.gradle` has `includeBuild '../novopay-platform-lib'`.

**Locked decisions (user confirmed 2026-09-28):**
- Base = `origin/ddp-prod-master` (live Boot 3.5.7 / Java 21 line; `ddp-prod` is the Boot 4 line with the
  `infra-essentials-firestore` split, 382 lib commits ahead). Forward-port later: bump to 0.0.3, move the 3
  new classes into `infra-essentials-firestore`.
- Config via `@Value` properties, not masterdata/Flyway.
- Strict backward compat: lib 6-arg overloads = legacy byte-for-byte (null settings); no new wire error code
  (13014 kept, retryability = exception subtype); consents flag `cc.cobrowsing.firestore.hardening.enabled`
  default true (kill switch); actor flag default false; fail-open if hardened options cannot be built.
- Values: keepalive 60 s / 20 s timeout, rpc 10 s, total 12 s, await 15 s, retry 1 x 500 ms; lock TTL =
  max(10 s, worst case + 5 s).
- Read path (`getChannelKeyHashFromFirestore`) is retried too (idempotent).

**Still open:** user review of the diff; commit/push on request only; merge to `ddp-bkup-uat` needs per-action
approval; UAT AC 1-7 incl. blackhole test of all resolved `firestore.googleapis.com` IPs; kill-switch drill;
enable actor flag after soak; DevOps network ticket + log alert are separate. Draft Jira confirmation comment
was given in chat (post from the user's own login, never via the connector).
Sequence diagrams: `docs/incidents/2026-09-24-uat-cobrowsing-firestore/sequence-before-after.md`.

Related: [[pref-git-workflow]], [[ref-flyway-infra-versioning]], [[ref-machine-commands]], [[proj-spring4-java25-upgrade]].
