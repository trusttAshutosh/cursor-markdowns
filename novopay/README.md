# Novopay workspace

Local multi-repo workspace for Novopay platform services, Bob proof, and Cursor agents.

## Cold start (agents)

1. Open [`novopay.code-workspace`](novopay.code-workspace) (not a single nested service alone).
2. Read [`AGENTS.md`](AGENTS.md) — orchestrator gates + self-check.
3. Day-to-day commands: [`.cursor/WORKFLOWS.md`](.cursor/WORKFLOWS.md).
4. Bob CLI: `python bob.py --help` or `.\bob.cmd` (engine lives in `bob-the-builder/`).

There is no single “start the monorepo” command. Boot the host service you need (often via Bob), with local MySQL/Redis as in `bob-the-builder/templates/user.env.example`.

## Validate a small change

Do **not** rebuild the whole tree by default.

```bash
# Preferred (works on Windows without make)
npm run validate -- novopay-platform-api-gateway
npm run lint -- novopay-platform-webapp
npm run format -- novopay-platform-webapp

# Same script directly
python scripts/validate-change.py novopay-platform-api-gateway
python scripts/validate-change.py --test novopay-platform-api-gateway
python scripts/validate-change.py --lint novopay-platform-webapp

# Optional Make wrappers (if make is installed)
make validate SERVICE=novopay-platform-api-gateway
make lint SERVICE=novopay-platform-webapp
```

| Change type | Default check |
|-------------|----------------|
| Java/Gradle service | `./gradlew compileJava` in that service (`--test` for unit tests) |
| Node webapp with ESLint/Prettier | `npm run lint` / format when scripts exist |
| E2E / API+DB proof | `bob validate-ticket <id>` **only when the human asks to prove** |

## Key paths

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Agent contract + learned prefs |
| `.cursor/WORKFLOWS.md` | Slash commands + Bob phrases |
| `.cursor/skills/` | Canonical skills |
| `.cursor/mcp.json` | `mysql` (Bob tools / DB queries) + Playwright browser MCP |
| `docs/tdd-runs/<ticket-id>/` | Ticket specs + Bob evidence |
| `bob-the-builder/` | Bob engine + docs |

## Plugins

Recommended Cursor marketplace plugins: [`.cursor/CURSOR_PLUGINS.md`](.cursor/CURSOR_PLUGINS.md) (`bob plugins`).
