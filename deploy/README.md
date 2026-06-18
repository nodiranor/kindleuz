# Deploying in webhook mode

Artifacts in this folder:
- `nginx/kindle_bot-bootstrap.conf` — HTTP-only, used once to obtain the first cert
- `nginx/kindle_bot.conf` — final TLS reverse proxy; forwards `/tg/` → `127.0.0.1:8001`
- `kindle_bot.service` — systemd unit

The webhook **secret** and **path** are already generated and stored in your local
`.env` (`WEBHOOK_SECRET`, `WEBHOOK_PATH=/tg/…`). Reuse the same values on the VPS.

> **Paths:** this guide uses `/opt/bots/kindle_bot` as the install dir — substitute
> your actual path everywhere (e.g. `/tg_bots/kindleuz`). The Nginx config is
> path-independent (it only proxies to `127.0.0.1:8001`); only the systemd unit
> and the `.env` location depend on it.

## 1. Code + virtualenv
```bash
mkdir -p /opt/bots/kindle_bot/{app,logs}
# upload the app/ folder to /opt/bots/kindle_bot/app
python3 -m venv /opt/bots/kindle_bot/venv
/opt/bots/kindle_bot/venv/bin/pip install -r /opt/bots/kindle_bot/app/requirements.txt
```

## 2. .env at /opt/bots/kindle_bot/.env
Copy your local `.env` there and change **only** `MODE`:
```ini
MODE=webhook
WEBHOOK_BASE_URL=https://amerikadan.uz
# WEBHOOK_SECRET / WEBHOOK_PATH: keep the generated values; path must stay under /tg/
```
```bash
chmod 600 /opt/bots/kindle_bot/.env
chown -R www-data:www-data /opt/bots/kindle_bot
```

## 3. TLS + Nginx (bootstrap HTTP → issue cert → enable TLS)
The 443 server can't load until the cert exists, so bring nginx up HTTP-only first.
```bash
apt install nginx certbot -y
mkdir -p /var/www/certbot

# 3a. HTTP-only config so nginx runs and can serve the ACME challenge:
cp deploy/nginx/kindle_bot-bootstrap.conf /etc/nginx/sites-available/kindle_bot.conf
ln -sf /etc/nginx/sites-available/kindle_bot.conf /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 3b. Issue the cert via webroot (writes only to /etc/letsencrypt, not nginx):
certbot certonly --webroot -w /var/www/certbot -d amerikadan.uz --agree-tos -m you@example.com -n

# 3c. Swap in the full TLS config (cert now exists) and reload:
cp deploy/nginx/kindle_bot.conf /etc/nginx/sites-available/kindle_bot.conf
nginx -t && systemctl reload nginx
```
Renewals are automatic (certbot.timer) and keep working because the `/.well-known/`
location stays in the HTTP block.

## 4. Start the service
```bash
cp deploy/kindle_bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now kindle_bot
journalctl -u kindle_bot -f      # expect: "Webhook set to https://amerikadan.uz/tg/…"
```

## 5. Verify
```bash
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo"
```
Expect `url` set to your `/tg/…` path, low `pending_update_count`, and no
`last_error_message`.

## ⚠️ DNS gotcha
`amerikadan.uz` must resolve to **this VPS** for both certbot and Telegram to
reach it. If that domain currently points at your web/email host, use a
subdomain for the bot instead (e.g. `bot.amerikadan.uz` → VPS IP), and update:
`WEBHOOK_BASE_URL`, the Nginx `server_name`, and `certbot -d bot.amerikadan.uz`.

## Switching back to polling
Set `MODE=polling` in `.env` and `systemctl restart kindle_bot`. Startup calls
`delete_webhook`, so Telegram's side is cleared automatically.
