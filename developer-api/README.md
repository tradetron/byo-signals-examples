# The other direction: the Developer API

Signals go **into** Tradetron. The Developer API lets your own app **read** from it: your deployments and their status,
open positions, today's P&L, engine notifications. It cannot trade, deploy or stop anything. (If you create strategies,
two write scopes, `broadcasts:write` and `automations:write`, let a key message your own subscribers; the console's
Docs tab covers them. This folder only reads.)

1. Creator Hub → **Developer API** → create a key. Tick only the scopes you need (`deployments:read` for this
   script). Pick an expiry (30 days, 90 days or none) and, if you can, an IP allowlist. Scopes are fixed when the key
   is made. Copy the key (`ttk_…`) when it is shown.
2. `export TT_DEV_API_KEY=ttk_...` and run `python3 read_deployments.py`.

| Endpoint (base `https://tradetron.tech/api/v1`) | Scope |
|---|---|
| `GET /me/deployments?page=` | `deployments:read` |
| `GET /me/deployments/{id}/positions` | `deployments:read` |
| `GET /me/live-pnl?ids=&execution=` | `pnl:read` |
| `GET /me/notifications?since=&ids=` | `events:read` |
| `GET /creator/deployments?status=&template=&q=` | `creator:read` |

Send the key as `Authorization: Bearer ttk_…` (or `X-API-KEY: ttk_…`). Every list takes `?fields=a,b`. Answers are
`{"success": true, "data": …}` or `{"success": false, "error": "…"}`. Each key allows 12 calls a minute and 10,000 a
day; a 429 says how many seconds to wait. The console's Try it runs the same calls in the browser, and its usage view
lists each key's calls.

No code at all? The console's **Feeds** send a deployment error (Error-Execution or Blocked) or a P&L snapshot to
Telegram (connect it in your account first) or to an https web address of your own.
