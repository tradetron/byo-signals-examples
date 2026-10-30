# A signal is a web address

Signal Bridge → Done → **Links** gives you four links per symbol (Buy, Exit buy, Sell, Exit sell). Opening one in
any browser sends the signal; the page shows `Ok`. Each link trades the minimum quantity.

Anatomy (the key replaced by a placeholder; never share a real link, it carries your key):

```
https://api.tradetron.tech/api?auth-token=<TT_AUTH_TOKEN>&key=RELIANCE&value=BUY
```

| Part | Means |
|---|---|
| `https://api.tradetron.tech/api?` | the one address for every signal (it ends in `?`) |
| `auth-token=` | your strategy's key |
| `key=RELIANCE&value=BUY` | the signal: set the variable `RELIANCE` to `BUY` |

Exit buy is `value=BUY%20EXIT` (a space is written `%20` in a link).

To set the quantity, put a quantity pair first and move the signal to `key1` / `value1`, as the Links tab's
"what a link looks like" line does:

```
https://api.tradetron.tech/api?auth-token=<TT_AUTH_TOKEN>&key=RELIANCE_qty&value=1&key1=RELIANCE&value1=BUY
```

`Ok` means Tradetron received the signal. Whether the strategy acted on it is in the deployment's
**Runtime Data → `RELIANCE_msg`**. Test links only against a Live Offline deployment.
