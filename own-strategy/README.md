# Signals into a strategy you built yourself

Signal Bridge and PineBridge build the receiving strategy for you. If you built your own, it has to keep its side of
the contract. Before this, take the free TT Uni course "Automating TradingView signals on Tradetron": it teaches
variables, the JSON format and lists by hand.

## 1. Link the key, Hybrid Yes
My Strategies → the strategy's **API** button → **Link**, **Hybrid mode = Yes** → Proceed. You get the Link and the
Token (key). Hybrid Yes keeps your strategy's own conditions running (exits, universal exit, repairs) beside the
signals; Hybrid No makes it act only on signals. The choice is locked once linked; unlinking and linking again gives
a new key. Only the strategy's owner can link it.

## 2. The strategy reads the value
- **Initialize Variables**: every name you will push, seeded at 0: `nifty_buy = Number(0)`.
- **Entry** waits for it: `Get Runtime("nifty_buy") == Number(1)`, plus a positions guard so only one side is
  ever open. A pushed quantity is read with `Get Runtime Number("nifty_buy_lots")` in the Qty cell.
- Names are matched exactly: `nifty_buy` and `nifty_Buy` are two different variables. Pick one casing.

## 3. Reset it where it is used
A pushed value **stays** until something changes it. A `1` left behind fires again the moment the position closes.
Set it back to `Number(0)` in the **Set Runtime** of the condition that consumed it:
- consumed by one condition (entry only, or exit only): reset it in that condition;
- the same signal exits one side and enters the other: reset it in the **entry**, which runs last;
- never in a separate condition: Set Runtime runs after that condition's orders and is skipped when the order
  fails, so a failed order keeps its signal.

## 4. The round-trip test
Deploy **Live Offline**. In a browser, open:

```
https://api.tradetron.tech/api?auth-token=<TT_AUTH_TOKEN>&key=nifty_buy&value=1
```

The page shows `Ok`. Open the deployment's **Runtime Data**: `nifty_buy` shows `1`, and on the next evaluation the
entry turns true. Value there but no trade: check Hybrid, market hours, the positions guard and the reset. No value:
the key (rotated? another strategy's?) or the pair order. Then wire the real alerts and test each once.
