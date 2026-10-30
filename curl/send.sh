#!/usr/bin/env bash
# send.sh - one Signal Bridge signal with curl.
# The request is the curl example on Signal Bridge -> Done -> Code (30 Oct 2026); only the key
# and the values come from your environment and arguments instead of being pasted in.
#
#   export TT_AUTH_TOKEN=...                 # Code tab -> Your key
#   ./send.sh RELIANCE BUY 1                 # open a Long of 1 (the qty pair goes first)
#   ./send.sh RELIANCE "BUY EXIT"            # close it (no qty: the strategy uses what it has)
#
# Pairs run key/value, key1/value1, ... in that order, and the signal goes LAST.
# "Ok" means Tradetron received it; whether the strategy acted is in Runtime Data -> <SYMBOL>_msg.
set -euo pipefail
: "${TT_AUTH_TOKEN:?Set TT_AUTH_TOKEN first (Signal Bridge -> Done -> Code -> Your key)}"
SYMBOL="${1:-${TT_SYMBOL:-RELIANCE}}"
ACTION="${2:-BUY}"
QTY="${3:-}"

if [ -n "$QTY" ]; then
  BODY=$(printf '{"auth-token":"%s","key":"%s_qty","value":"%s","key1":"%s","value1":"%s"}' \
    "$TT_AUTH_TOKEN" "$SYMBOL" "$QTY" "$SYMBOL" "$ACTION")
else
  BODY=$(printf '{"auth-token":"%s","key":"%s","value":"%s"}' "$TT_AUTH_TOKEN" "$SYMBOL" "$ACTION")
fi

curl -s -X POST 'https://api.tradetron.tech/api?' \
  -H 'Content-Type: application/json' \
  -d "$BODY" \
  -w '\nHTTP %{http_code}\n'
