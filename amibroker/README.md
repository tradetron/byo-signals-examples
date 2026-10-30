# Amibroker

No tested snippet yet. Amibroker (or any tool that can make an HTTP request) sends the same thing as
[`../curl/send.sh`](../curl/send.sh): a GET of a signal link or a JSON POST to `https://api.tradetron.tech/api?`, pairs
in order, the signal last, its own User-Agent. Until someone writes and tests an AFL example against a Live Offline
deployment, this folder holds no code on purpose.
