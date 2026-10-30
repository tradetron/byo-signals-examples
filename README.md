# Bring your own signals: examples for Tradetron

Sample code for the free TT Uni course **Bring Your Own Signals: TradingView, Python and the Tradetron API**.
Your signal comes from somewhere else (a chart, a script, a spreadsheet, your own app); Tradetron executes it.
Every snippet here was copied from what the product itself hands you (Signal Bridge's Code tab and its
downloadable `.py`, PineBridge's Done screen, the Developer API console) and was run against a Live Offline
Signal Bridge on Tradetron's demo account on 30 Oct 2026.

**This repository holds no key.** Every script reads yours from the environment (`TT_AUTH_TOKEN`, or
`TT_DEV_API_KEY` for the Developer API). Copy `.env.example` to `.env`; `.env` is git-ignored.

## The contract, on one page
- **One address** for every signal: `https://api.tradetron.tech/api?` (GET with the fields in the query
  string, or POST them as JSON).
- **The key** is your strategy's API key: Signal Bridge → Done → Code → Your key, or My Strategies → the
  strategy's API button. It belongs to that strategy and drives every deployment of it. Anyone holding it can
  send signals to it. If it leaks, unlink and link again on the API button: you get a new key and the old one
  is refused.
- **Pairs, in order:** `auth-token`, then `key` / `value`, `key1` / `value1`, `key2` / `value2` … Each pair
  sets one runtime variable. The order must not change. On a Signal Bridge the pair named after the symbol
  (`RELIANCE` = `BUY`, `BUY EXIT`, `SELL`, `SELL EXIT`) is the signal and goes **last**; settings such as
  `RELIANCE_qty` go before it. Names are case-sensitive.
- **What comes back:**

  | Answer | Means |
  |---|---|
  | `200 Ok` | Tradetron received it. Whether the strategy acted is in **Runtime Data → `<SYMBOL>_msg`** (`ACCEPTED_BUY`, `REJECTED_POSITION_OPEN`, …). |
  | `401 Unauthorized` | The key is wrong or was rotated. Relink from My Strategies → API OAuth Token. |
  | `403 error code: 1010` | Refused before Tradetron saw it: a blocked User-Agent (Python's default `Python-urllib/3.x` is one). Send your own `User-Agent`. |
  | `429` | Too many signals in a short time. |

- **Limits:** 3 signals a second and 30 a minute, per strategy (Tradetron's own Signal Pad and code state
  these). The downloaded Python client also stops itself at 250 an hour, the figure in Tradetron's help
  pages; we are still confirming that hourly figure with the team that runs the webhook, so treat it as a
  safe ceiling, not a promise.
- **When it counts:** a signal is acted on in the strategy's next evaluation cycle (seconds), only while the
  deployment is running and the market is open. A late signal is refused, not held.
- **Live Offline first.** Deploy the strategy Live Offline (it runs on live prices and places no order) and
  prove every signal there before you deploy Live Auto with your broker. A signal strategy cannot be
  backtested: there is no history of your signals.

## What is here
| Folder | Use it for |
|---|---|
| [`links/`](links/) | a signal as a plain web address (bookmark, any app that opens a link) |
| [`excel/`](excel/) | the Buy / Sell sheet Signal Bridge gives you |
| [`curl/send.sh`](curl/send.sh) | one POST from a terminal |
| [`python/send_signal.py`](python/) | the downloaded Python client, key from the environment |
| [`tradingview/`](tradingview/) | TradingView alerts through PineBridge, and the message bodies |
| [`own-strategy/`](own-strategy/) | sending to a strategy you built yourself (Get Runtime, Hybrid, the reset) |
| [`developer-api/read_deployments.py`](developer-api/) | the other direction: read your deployments from your app |
| [`amibroker/`](amibroker/) | placeholder, no tested snippet yet |

## Quick start
```bash
cp .env.example .env          # put your key in .env
set -a; . ./.env; set +a
./curl/send.sh RELIANCE BUY 1             # Live Offline deployment, market hours
python3 python/send_signal.py "BUY EXIT"  # close it
```
Then open the deployment in Tradetron → **Runtime Data** and read `RELIANCE_msg`.

The examples are mechanical (buy RELIANCE, one share) to show the plumbing. They are a practice example, not a
recommendation. Education, not investment advice. MIT licence.
