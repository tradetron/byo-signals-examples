# TradingView, through PineBridge

**Use PineBridge first** (Create → Pine Script Strategy on Tradetron). Paste your Pine Script; PineBridge reads
whether it is an indicator or a strategy and how it signals, asks what each signal should trade, builds the Tradetron
strategy, links its key and writes the alert messages for you. Its **Done** screen lists what is left, in order, each
with a Copy button:

1. *(strategy scripts only)* Replace your script with the tagged version PineBridge gives you, then Save.
2. **Webhook URL**, the same one for every alert: `https://api.tradetron.tech/api?`
   (TradingView: Alert → Notifications → tick Webhook URL → paste).
3. **One Message per signal** (TradingView: Alert → Message). Your key is already inside each one.
4. **Deploy it** on Tradetron, Live Offline or Live Auto. A strategy acts on your TradingView signals only while it is
   deployed. Start Live Offline.

You can come back to that screen any time: My Strategies → **API** on the PineBridge strategy.

## The message bodies (`examples/`)
What PineBridge writes, with the key replaced by `<YOUR_KEY>`. Use the ones from your own Done screen; these are for
reading, not for pasting.

| Your script | Alerts | Message |
|---|---|---|
| Indicator, "always in trade" | 2 | `api_buy` = `1` Long (go long, exit short), `2` Short (go short, exit long) |
| Indicator, "entry and exit based" | 4 | `api_buy` = `1` Long Entry, `2` Long Exit, `3` Short Entry, `4` Short Exit |
| Strategy script | 1 | key `{{strategy.order.comment}}`: TradingView fills in the order comment PineBridge tagged (L / S / LX / SX), so one alert covers every signal |

TradingView side, as PineBridge's Done screen says it:
- Indicator: one alert per signal, Condition = your indicator and the exact signal, **Trigger = Once Per Bar Close**.
- Strategy: one alert on your strategy, firing on **"Order fills and alert() function calls"**.

The strategy PineBridge builds resets its signal variable when it enters, so one alert is one trade.

## Before you start
TradingView sends webhooks only on a **paid TradingView plan**, and only with **two-factor authentication** turned on
in your TradingView account. Those are TradingView's rules, not Tradetron's; check their current plans page.

## Not using PineBridge?
Any alert can send the same JSON to the same address. If the strategy is one you built yourself, see
[`../own-strategy/`](../own-strategy/) for what it must do with the value.
