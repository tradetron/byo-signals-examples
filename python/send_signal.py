"""
send_signal.py - send Signal Bridge signals to Tradetron.

This is the file Signal Bridge gives you (Done -> Code -> Download .py, saved as
tt_signal_bridge.py), downloaded on 30 Oct 2026, with three changes so it can live
in a public repository:
  1. the key is read from the TT_AUTH_TOKEN environment variable, never from the file;
  2. the basket comes from TT_SYMBOL (default RELIANCE) and TT_TEMPLATE_ID;
  3. an HTTP refusal (401 / 403 / 429) is explained instead of raising a bare error.
Everything else (the pairs, their order, the User-Agent, the throttle) is the
downloaded file, unchanged.

Standard library only (Python 3.8+).

    export TT_AUTH_TOKEN=...            # Signal Bridge -> Code -> Your key
    export TT_SYMBOL=RELIANCE           # your bridge's variable, as the Links tab shows it
    python send_signal.py               # one BUY of 1 of TT_SYMBOL
    python send_signal.py "BUY EXIT"    # close it

or from your own code:

    from send_signal import signal
    signal("MY", "RELIANCE", "BUY", qty=1)      # open a Long
    signal("MY", "RELIANCE", "BUY EXIT")        # close it

A signal is acted on in the strategy's next evaluation cycle (seconds), only
while the deployment is running and the market is open. Check the result in
Tradetron: My Deployments -> the strategy -> Runtime Data -> <SYMBOL>_msg
(ACCEPTED_BUY, REJECTED_POSITION_OPEN, REJECTED_MAX_POSITION, SL_HIT ...).
Send to a Live Offline deployment first: it runs on live prices and places no order.
"""
import os
import urllib.error
import json
import time
import urllib.request

WEBHOOK_URL = "https://api.tradetron.tech/api?"

TEMPLATES = {
    "MY": {
        "template_id": int(os.environ.get("TT_TEMPLATE_ID", "0")),   # for your own reference only
        "auth_token": os.environ.get("TT_AUTH_TOKEN", ""),
        "symbols": [s.strip().upper() for s in os.environ.get("TT_SYMBOL", "RELIANCE").split(",") if s.strip()],
    },
}

ACTIONS = ("BUY", "BUY EXIT", "SELL", "SELL EXIT")
QTY_METHODS = {"FIX": 1, "CAPITAL_PCT": 2, "CAPITAL_RISK_PCT": 3, "ALLOCATION_METHOD_1": 4}
TRADE_UNITS = {"M": 1, "P": 2, "%": 3}   # Money, Points, Percent
MASTER_UNITS = {"M": 1, "%": 2}          # Money, Capital %
WEEKDAYS = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5, "SAT": 6, "SUN": 7}

# Tradetron's published webhook limits: 3/second, 30/minute, 250/hour.
_sent = []


def _throttle():
    now = time.time()
    while True:
        _sent[:] = [t for t in _sent if now - t < 3600]
        wait = 0.0
        last_sec = [t for t in _sent if now - t < 1]
        if len(last_sec) >= 3:
            wait = max(wait, 1 - (now - last_sec[0]))
        last_min = [t for t in _sent if now - t < 60]
        if len(last_min) >= 30:
            wait = max(wait, 60 - (now - last_min[0]))
        if len(_sent) >= 250:
            raise RuntimeError("Tradetron allows 250 signals per hour; this process has used them all")
        if wait <= 0:
            break
        time.sleep(wait + 0.05)
        now = time.time()
    _sent.append(time.time())


def send_pairs(template, pairs):
    """POST one webhook call carrying several variable=value pairs, in order.
    Pair order is load-bearing: key/value, key1/value1, key2/value2, ..."""
    t = TEMPLATES[template]
    body = {"auth-token": t["auth_token"]}
    for i, (k, v) in enumerate(pairs):
        sfx = "" if i == 0 else str(i)
        body["key" + sfx] = str(k)
        body["value" + sfx] = str(v)
    _throttle()
    req = urllib.request.Request(
        WEBHOOK_URL, data=json.dumps(body).encode(),
        # A User-Agent is REQUIRED: Cloudflare in front of the webhook answers
        # 403 (error 1010) to Python's default "Python-urllib/3.x".
        headers={"Content-Type": "application/json", "User-Agent": "tt-signal-bridge/1.0"},
        method="POST")
    if not t["auth_token"]:
        raise SystemExit("Set TT_AUTH_TOKEN first (Signal Bridge -> Done -> Code -> Your key).")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            text = resp.read().decode(errors="replace")
            return {"http_status": resp.status, "body": text}
    except urllib.error.HTTPError as e:
        return {"http_status": e.code, "body": e.read().decode(errors="replace")[:300],
                "meaning": REFUSALS.get(e.code, "Tradetron refused the signal.")}


# What a refusal means. 401 and 429 use the Signal Pad's own words; 403 / 1010 is Cloudflare
# refusing a default Python User-Agent, which the header above avoids.
REFUSALS = {
    401: "This strategy's API token is no longer valid. Relink it from My Strategies -> API OAuth Token, then update TT_AUTH_TOKEN.",
    403: "Refused before Tradetron saw it (error 1010 = a blocked User-Agent). Keep the User-Agent header.",
    429: "Too many signals in a short time (the limit is 3 a second, 30 a minute). Wait a moment.",
}


def signal(template, symbol, action, qty=None, qty_method=None,
           target=None, target_unit=None, sl=None, sl_unit=None):
    """Send one BUY / BUY EXIT / SELL / SELL EXIT for one basket symbol.

    qty          FIX: units (lot multiples) per trade.  CAPITAL_PCT / CAPITAL_RISK_PCT: the percent.
    qty_method   FIX (default), CAPITAL_PCT, CAPITAL_RISK_PCT, ALLOCATION_METHOD_1
    target, sl   per-trade levels; 0 turns them off
    *_unit       'M' money, 'P' points, '%' percent of entry price
    Settings sent with a signal stay in force for that symbol until changed.
    """
    symbol = symbol.upper()
    action = action.upper().replace("_", " ").strip()
    if symbol not in TEMPLATES[template]["symbols"]:
        raise ValueError("%s is not in the %s basket: %s" % (symbol, template, TEMPLATES[template]["symbols"]))
    if action not in ACTIONS:
        raise ValueError("action must be one of %s" % (ACTIONS,))
    pairs = []
    if qty_method is not None:
        pairs.append((symbol + "_qm", QTY_METHODS[qty_method.upper()]))
    if qty is not None:
        pairs.append((symbol + "_qty", qty))
    if target is not None:
        pairs.append((symbol + "_tp", target))
    if target_unit is not None:
        pairs.append((symbol + "_tpu", TRADE_UNITS[target_unit.upper()]))
    if sl is not None:
        pairs.append((symbol + "_sl", sl))
    if sl_unit is not None:
        pairs.append((symbol + "_slu", TRADE_UNITS[sl_unit.upper()]))
    pairs.append((symbol, action))          # the signal goes LAST
    return send_pairs(template, pairs)


def configure(template, capital=None, master_target=None, master_target_unit=None,
              master_sl=None, master_sl_unit=None, max_positions=None,
              max_capital_allocation_pct=None, intraday=None, exit_minutes_before_close=None,
              working_days=None, session_start_hhmm=None, session_end_hhmm=None,
              sqroff_all_on_tp_sl=None, auto_expiry_exit=None):
    """Portfolio settings. Send after deploying, and again after any intraday
    day-end (a new run starts from the template defaults)."""
    m = []
    if capital is not None: m.append(("capital", capital))
    if master_target is not None: m.append(("mt", master_target))
    if master_target_unit is not None: m.append(("mtu", MASTER_UNITS[master_target_unit.upper()]))
    if master_sl is not None: m.append(("ms", master_sl))
    if master_sl_unit is not None: m.append(("msu", MASTER_UNITS[master_sl_unit.upper()]))
    if max_positions is not None: m.append(("maxpos", max_positions))
    if max_capital_allocation_pct is not None: m.append(("maxcap", max_capital_allocation_pct))
    if intraday is not None: m.append(("intraday", 1 if intraday else 0))
    if exit_minutes_before_close is not None: m.append(("xmin", exit_minutes_before_close))
    if working_days is not None:
        m.append(("wdays", "".join(str(WEEKDAYS[d.upper()[:3]]) for d in working_days)))
    if session_start_hhmm is not None: m.append(("tstart", session_start_hhmm))
    if session_end_hhmm is not None: m.append(("tend", session_end_hhmm))
    if sqroff_all_on_tp_sl is not None: m.append(("sqall", 1 if sqroff_all_on_tp_sl else 0))
    if auto_expiry_exit is not None: m.append(("autoexp", 1 if auto_expiry_exit else 0))
    if not m:
        raise ValueError("nothing to configure")
    return send_pairs(template, m)


def reset_after_master_stop(template):
    """After Master Target / Master SL halts the portfolio, re-arm it (P&L re-baselined)."""
    return send_pairs(template, [("rebase", 1)])


if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "BUY"
    qty = sys.argv[2] if len(sys.argv) > 2 else ("1" if action.upper() in ("BUY", "SELL") else None)
    symbol = TEMPLATES["MY"]["symbols"][0]
    print(signal("MY", symbol, action, qty=qty, qty_method="FIX" if qty else None))
