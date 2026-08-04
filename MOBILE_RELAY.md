# Cursor Mobile Relay (Novopay)

Pointer doc - canonical repo lives at `Desktop/cursor-mobile-relay` (GitHub: publish as `cursor-mobile-relay`).

## Why

When Cursor Agent or `bob validate` waits for **Approve terminal command**, you can respond from your phone instead of the desk. **$0** - no Cursor Cloud, no paid third-party relay.

## Setup summary

1. **Cursor CDP:** shortcut Target includes `--remote-debugging-port=9222`
2. **Relay:** `python -m venv .venv && pip install -r requirements.txt`, copy `.env.example` to `.env`, set `RELAY_PASSWORD`
3. **Start:** `python -m relay` or `scripts/start.ps1`
4. **Phone:** Tailscale on PC + phone; `tailscale serve --bg --https=443 http://127.0.0.1:8787`
5. **Bookmark:** `https://YOUR-PC.tailnet.ts.net/?token=YOUR_RELAY_PASSWORD`

## With Novopay workflow

| Desk | Away |
|------|------|
| `/ticket-kickoff`, implement, `bob validate` starts | Open mobile relay when badge shows **needs approval** |
| Agent runs long Bob boot | Approve shell/MCP steps from phone |
| Return | Continue in Cursor IDE as normal |

See also [WORKFLOW.md](WORKFLOW.md) mobile section.

## Optional Google Chat

Set `GCHAT_WEBHOOK_URL` in relay `.env`.

**Alert rule:** posts to **Cursor Ops** when Cursor **needs approval** AND you have had **no keyboard/mouse activity** for `GCHAT_IDLE_SECONDS` (default **120** = 2 min). No spam while you are at the desk.

Optional `RELAY_PUBLIC_URL` = your Tailscale serve URL for a link in the message.

## Security

- Never commit `.env`
- Keep `RELAY_HOST=127.0.0.1`; expose only via Tailscale serve HTTPS
- Strong random `RELAY_PASSWORD`
