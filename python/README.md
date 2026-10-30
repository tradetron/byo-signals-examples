# Python: send_signal.py

`send_signal.py` is the file Signal Bridge gives you (Done → Code → **Download .py**), with three changes so it can
live in public: the key comes from `TT_AUTH_TOKEN`, the symbol from `TT_SYMBOL`, and a refusal (401 / 403 / 429) is
explained instead of raised. Standard library only, Python 3.8+.

```bash
export TT_AUTH_TOKEN=...       # Code tab -> Your key
export TT_SYMBOL=RELIANCE      # your bridge's variable, exactly as the Links tab shows it
python3 send_signal.py                 # BUY 1 of RELIANCE
python3 send_signal.py "BUY EXIT"      # close it
python3 send_signal.py BUY 5           # BUY 5
```

From your own code: `from send_signal import signal` then `signal("MY", "RELIANCE", "BUY", qty=1)`.
`signal()` also takes `target`, `sl` and their units; `configure()` sets portfolio settings (capital, max
positions, session). A setting sent with a signal stays in force for that symbol until you change it; an intraday
bridge starts each session from its built settings.

What it does that matters:
- **Pairs in order**, the signal last (`send_pairs()` numbers them `key`, `key1`, `key2` …).
- **Its own User-Agent** (`tt-signal-bridge/1.0`). Python's default agent is refused with `403 error code: 1010`.
- **A throttle**: 3 a second, 30 a minute, and it stops at 250 an hour (see the main README on that figure).

Run it against a **Live Offline** deployment during market hours, then read the deployment's **Runtime Data →
`<SYMBOL>_msg`**: `ACCEPTED_BUY`, then `ACCEPTED_BUY_EXIT` after the exit.

`CERTIFICATE_VERIFY_FAILED` on a Mac means that Python install has no CA certificates yet: run
`Install Certificates.command` from its Applications folder (python.org installers), or point `SSL_CERT_FILE` at a
CA bundle.
