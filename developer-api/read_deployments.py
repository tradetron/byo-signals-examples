"""
read_deployments.py - list your Tradetron deployments with a Developer API read key.

    GET https://tradetron.tech/api/v1/me/deployments      scope: deployments:read

Make the key in Creator Hub -> Developer API (tick deployments:read). A Developer API key
only reads: it can never trade, deploy or stop a strategy. Each key allows 12 calls a minute
and 10,000 a day; answers are cached for a few seconds, so polling faster gains nothing.

    export TT_DEV_API_KEY=ttk_...
    python read_deployments.py              # id, name, mode, status of each deployment
    python read_deployments.py --pnl        # also capital and P&L (keep these off a shared screen)

Standard library only (Python 3.8+).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://tradetron.tech/api/v1"
FIELDS = "deployment_id,name,deployment_type,status,open_positions"
PNL_FIELDS = ",capital,pnl,currency_code"


def get(path, key):
    req = urllib.request.Request(BASE + path, headers={
        "Authorization": "Bearer " + key,     # or X-API-KEY: ttk_...
        "Accept": "application/json",
        "User-Agent": "byo-signals-examples/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            msg = json.loads(body).get("error", body)
        except ValueError:
            msg = body[:200]
        hint = {401: "the key is wrong, expired or revoked",
                403: "the key lacks deployments:read, or this IP is outside its allowlist",
                429: "a limit was reached; wait the Retry-After seconds"}.get(e.code, "")
        raise SystemExit("HTTP %d: %s%s" % (e.code, msg, (" (" + hint + ")") if hint else ""))


def main():
    key = os.environ.get("TT_DEV_API_KEY", "")
    if not key.startswith("ttk_"):
        raise SystemExit("Set TT_DEV_API_KEY to a ttk_ key from Creator Hub -> Developer API.")
    fields = FIELDS + (PNL_FIELDS if "--pnl" in sys.argv else "")
    page, rows = 1, []
    while True:
        answer = get("/me/deployments?page=%d&fields=%s" % (page, fields), key)
        data = answer.get("data") or {}
        rows += data.get("deployments") or []
        if page >= int(data.get("last_page") or 1):
            break
        page += 1
        time.sleep(5)          # stays inside 12 a minute
    print("%d deployment(s)" % len(rows))
    for r in rows:
        print("  " + "  ".join("%s=%s" % (k, r.get(k)) for k in fields.split(",")))


if __name__ == "__main__":
    main()
