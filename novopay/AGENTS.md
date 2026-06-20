# Novopay workspace

## Orchestrator model (fixed - do not let Continual Learning edit this section)

**You (human):** approve or reject at four gates only - Plan, Build, Prove, Ship.

**Agent:** everything else - workspace, memory, skills, Bob runs, boot fixes, hygiene.

**Bob:** proof engine (not redundant). Agent implements; Bob produces `REPORT.md` evidence.

Do not ask the human to pin files, switch workspace, or run memory chores.

### Gate checklist for the human

1. **Plan** - Is scope right? Any client questions?
2. **Build** - Does the diff match the plan?
3. **Prove** - Does Bob `GATE_SUMMARY.md` show PASS on Plan/Build/Prove for the right ticket?
4. **Ship** - OK to commit/PR?

---

Plain bullets below are for Continual Learning. Keep section names exactly as named.

## Learned User Preferences

- Do not commit or push Novopay changes unless explicitly asked.
- Run `bob validate-ticket <ticket-id>` only when explicitly asked to test/prove ("bob let's test", "validate", "test this ticket", "bob validate-ticket", "Bob to test") — never auto-run Bob after every code fix. Default proof when asked is **E2E** (API + DB + logs), not Gradle unit tests. Bob autoboot should be true; boot fixes go in `bob-the-builder/runner/config/boot-remediation.yaml` or host `deploy/tdd/`, not chat-only workarounds.
- Stay on the active ticket; do not mix docs or test artifacts from unrelated tickets (e.g. LOC jumbo vs SQLi).
- For security fixes, prove the vulnerability with reproducible queries or API calls before fixing, then re-run the same checks after.
- PE-PQ jumbo: case-insensitive compare, skip jumbo offer inquiry, treat as no jumbo offer; no CBCI, MIS, or Insta-loan scope creep.
- Fix failing unit tests by updating tests, not production classes, unless prod code is genuinely wrong.
- No one-line helper methods; put constants in the appropriate constants class.
- Gateway stays generic; domain-specific auth and business rules belong in domain services (e.g. actor).
- Use ASCII hyphens in markdown docs, not em dashes.
- Before quality review on a diff, use `/thermo-nuclear-code-quality-review`.
- Day-to-day workflows: see `novopay/.cursor/WORKFLOWS.md` or `Desktop/cursor-markdowns/WORKFLOW.md` (visual one-pager).
- Keep pinned+today+yesterday Cursor chats at ~6-8 active; archive stale chats (7+ days) via `bob chat-hygiene`, never delete; periodically run `/workflow-from-chats` and then `/agents-memory-updater` to convert recent chat deltas into durable memory.
- For SQL migration sequence numbers, first check the latest seq on each repo's common-scripts branch (branch name may differ slightly, e.g. `ddp-fea-common-script` vs `ddp-fea-common-scripts`), then use next seq.
- Root-cause / incident analysis must follow `~/.cursor/rules/incident-analysis-format.mdc`: phased history tables, mermaid flow, commit link + author + date on every commit, working-vs-broken timeline, numbered why/fix/ops sections, one-line summary.

## Learned Workspace Facts

- Primary monorepo root: `Desktop/novopay` with services including `novopay-platform-creditcard-management`, `novopay-platform-lib`, `novopay-platform-api-gateway`, `novopay-platform-actor`, and `bob-the-builder`.
- Canonical agent skills live at `Desktop/novopay/.cursor/skills/`; CC repo `.cursor/skills` is a junction to the same folder.
- Bob TDD artifacts live under each service's `docs/tdd-runs/<ticket-id>/` (REPORT.md, postman collections, DB verify SQL).
- Local DB for Bob/CC is typically `root`/`root` per `application.properties`; CC needs `application.properties` on bootRun classpath; consents/notifications need `novopay.service.name`.
- CC health endpoint: `http://localhost:8016/cc-mgmt/actuator/health`.
- Backend baseline branch is often `ddp-prod`; lib changes use composite `includeBuild` from CC.
- Single orchestrator rule: `~/.cursor/rules/novopay-orchestrator.mdc` (always applies, even from home workspace).
- One-click workspace: `novopay.code-workspace` (root + bob + CC + lib + gateway + actor).
- Bob orchestrator checklist per ticket: `docs/tdd-runs/<ticket-id>/GATE_SUMMARY.md` (Plan / Build / Prove / Ship).
- Monthly: stop hook auto-runs `bob meta-review --hook stop` every 30d (or run `bob meta-review` manually) -> human reviews `bob-the-builder/docs/META_REVIEW.md` + `CONTEXT_USAGE_AUDIT.md` -> approve rule/skill/Bob changes manually or `bob onboard --force` for rule sync.
