# 📚 Kindle Sender Bot — Project Plan for Claude Code

## Project Overview

A Telegram bot that accepts document files from users and forwards them to their registered Kindle email address via the Amazon Send-to-Kindle service. The bot provides each user a dedicated trusted sender email address to register in their Amazon account.

Built with **Python 3.11+** and **aiogram 3.2x**, deployed via **webhook** (not long-polling) on a shared InterServer VPS slice that also hosts other bots and websites.

---

## 🖥️ VPS Reality Check

| Resource | InterServer Slice 1 | Notes |
|---|---|---|
| CPU | 1 vCore | Shared across all bots/sites on this VPS |
| RAM | 2 GB | ~100–150 MB per Python bot process |
| SSD | 40 GB | OS ~3 GB, leave ~35 GB for projects |
| Bandwidth | 2 TB/month | Ample for bots + small sites |
| IP | 1 dedicated public IP | Required for Nginx + HTTPS webhooks |

**Capacity estimate:** This slice comfortably runs 8–12 lightweight aiogram bots simultaneously, plus a few static/small websites, as long as no single bot does heavy CPU work (ML, video processing, etc.). This bot is email+file forwarding — well within budget.

---

## 🏗️ VPS-Level Infrastructure

### OS Recommendation
**Ubuntu 22.04 LTS** — widely documented, long support window, stable `apt` ecosystem.

### Server Software Stack

```
Internet (HTTPS :443)
        │
        ▼
   [Cloudflare]  ← optional but recommended (DDoS, free SSL certs via CF)
        │
        ▼
  [Nginx]  ← reverse proxy, terminates TLS, routes by subdomain/path
        │
        ├──► /kindle_bot/webhook  → localhost:8001  (this bot)
        ├──► /other_bot/webhook   → localhost:8002  (future bot)
        ├──► example.com          → localhost:3000  (future website)
        └──► ...
```

### Required packages on VPS

```bash
# System
apt install nginx certbot python3-certbot-nginx python3 python3-pip python3-venv git

# Each bot gets its own virtualenv — never install globally
python3 -m venv /opt/bots/kindle_bot/venv
```

### SSL / HTTPS

Telegram **requires HTTPS** for webhooks. Two options:

| Option | How | Cost |
|---|---|---|
| **Let's Encrypt** (recommended) | `certbot --nginx -d yourdomain.com` | Free |
| Cloudflare proxy | Set DNS to CF, use CF's edge TLS | Free |

You need a **domain name** pointed to your VPS IP. Even a cheap one (~$5–10/yr) works. Each bot can either share the same domain with different paths, or use subdomains.

---

## 📁 Project Structure

```
/opt/bots/kindle_bot/          ← deployment root on VPS
├── venv/                      ← isolated virtualenv
├── .env                       ← secrets (chmod 600)
├── kindle_bot.db              ← SQLite database
├── logs/
│   └── bot.log
├── kindle_bot.service         ← systemd unit file
│
└── app/                       ← actual source code (git repo)
    ├── bot.py
    ├── config.py
    ├── handlers/
    │   ├── __init__.py
    │   ├── start.py
    │   ├── settings.py
    │   └── documents.py
    ├── middlewares/
    │   ├── __init__.py
    │   └── db_middleware.py
    ├── services/
    │   ├── __init__.py
    │   ├── mailer.py
    │   └── file_handler.py
    ├── db/
    │   ├── __init__.py
    │   ├── models.py
    │   └── database.py
    ├── keyboards/
    │   ├── __init__.py
    │   └── inline.py
    ├── utils/
    │   ├── __init__.py
    │   └── validators.py
    └── requirements.txt
```

---

## ⚙️ Tech Stack

| Component | Choice |
|---|---|
| Bot framework | `aiogram 3.2x` |
| Transport | Webhook (aiohttp server behind Nginx) |
| Database | SQLite via `SQLAlchemy` (async, `aiosqlite`) |
| Email sending | `aiosmtplib` + Gmail/SMTP relay |
| File download | aiogram's built-in `bot.download()` |
| Config | `pydantic-settings` with `.env` |
| Process manager | `systemd` |
| Reverse proxy | Nginx + Let's Encrypt |
| Migrations | `alembic` (optional but recommended) |

---

## 🗃️ Database Model

```python
# db/models.py
class User(Base):
    __tablename__ = "users"

    telegram_id: int          # Primary key
    kindle_email: str | None  # Set by user via /setkindle
    created_at: datetime
    documents_sent: int       # Counter for stats
```

---

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Welcome message + setup instructions |
| `/help` | Full usage guide + limitations |
| `/setkindle <email>` | Save user's Kindle email address |
| `/myemail` | Show the bot's sender email (for Amazon whitelist) |
| `/status` | Show current Kindle email + docs sent count |

---

## 📨 Core Email Flow

```
User uploads file
       │
       ▼
Validate file (type + size)
       │
       ▼
Download file from Telegram servers
       │
       ▼
Look up user's Kindle email in DB
       │
       ├─── Not set? → Ask user to /setkindle first
       │
       ▼
Send via SMTP (aiosmtplib)
  From: bot_sender@yourdomain.com   ← user must whitelist this
  To:   user_kindle@kindle.com
  Attachment: the document file
       │
       ▼
Confirm success / report error to user
       │
       ▼
Delete temp file from disk (always, even on error)
```

---

## ✅ Supported File Types

Based on Amazon's official Personal Document Service accepted formats:

```python
ALLOWED_EXTENSIONS = {
    ".pdf",   # PDF
    ".doc",   # Word (older)
    ".docx",  # Word
    ".rtf",   # Rich Text
    ".txt",   # Plain text
    ".htm",   # HTML
    ".html",  # HTML
    ".mobi",  # Mobipocket (Kindle native)
    ".epub",  # EPUB (supported on newer Kindles)
    # Images (sent as photo documents):
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",   # non-animated only
    ".bmp",
    ".tiff",
    ".tif",
}
```

> ⚠️ **Not supported by Amazon**: `.zip`, `.cbz`, `.fb2`, `.djvu` — the bot must explicitly reject these.

---

## ⚠️ Limitations to Implement & Communicate

These must be shown to the user in `/help` and enforced in code:

### Amazon-side Limits

- **Max file size: 50 MB per document** (Amazon's hard cap for Send-to-Kindle email)
- **Daily storage quota**: Amazon provides 5 GB of free cloud storage; documents beyond quota may fail silently
- **Supported formats only**: Reject unsupported types with a clear message listing what IS accepted
- **EPUB caveat**: EPUB is only supported on Kindle devices/apps with firmware updated after ~2022; older devices may not display it

### Bot-side Limits (your policy, configurable)

- **Enforce the 20 MB cap** before downloading — check `file.file_size` from Telegram metadata
- **Telegram's own limit**: Bots can only download files up to **20 MB** via the standard Bot API. Files between 20–50 MB would require running the **Telegram Bot API local server** — out of scope for v1, but noted here for future reference
- **Rate limiting**: Optionally limit each user to N sends per day to avoid SMTP abuse

### Email/Trust Setup Required

- The user **must** add the bot's sender email to their **Amazon Approved Personal Document E-mail List** at: `amazon.com → Account → Manage Your Content and Devices → Preferences → Personal Document Settings`
- Reference: [How to Use Send to Kindle Email Address Service - Amazon Customer Service](https://www.amazon.com/gp/help/customer/display.html?nodeId=G7NECT4B4ZWHQ8WV)
- If the sender email is not whitelisted, Amazon silently drops the email — the bot should warn users of this clearly and repeatedly (e.g. in `/start`, `/help`, and `/myemail`)

---

## 🔧 Key Implementation Details

### `config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Telegram
    BOT_TOKEN: str
    WEBHOOK_BASE_URL: str      # e.g. https://yourdomain.com
    WEBHOOK_SECRET: str        # random 32-char string, for header validation
    PORT: int = 8001           # internal port, Nginx proxies to this

    # SMTP
    SMTP_HOST: str             # e.g. smtp.gmail.com
    SMTP_PORT: int = 587
    SMTP_USER: str             # this is what users whitelist at Amazon
    SMTP_PASSWORD: str         # Gmail App Password

    # App
    MAX_FILE_SIZE_BYTES: int = 20 * 1024 * 1024   # 20 MB
    DATABASE_URL: str = "sqlite+aiosqlite:///./kindle_bot.db"

    class Config:
        env_file = ".env"

settings = Settings()
```

### `bot.py` — Entry point (webhook mode)

```python
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from config import settings
from handlers import start, settings as settings_handler, documents
from middlewares.db_middleware import DbSessionMiddleware
from db.database import create_db_pool

async def on_startup(bot: Bot):
    await bot.set_webhook(
        url=f"{settings.WEBHOOK_BASE_URL}/webhook/{settings.BOT_TOKEN}",
        secret_token=settings.WEBHOOK_SECRET,  # extra security header
        allowed_updates=["message", "callback_query"],
    )
    logging.info("Webhook set.")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logging.info("Webhook removed.")

def main():
    logging.basicConfig(level=logging.INFO, filename="logs/bot.log")

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Middlewares
    dp.update.middleware(DbSessionMiddleware(session_pool=create_db_pool()))

    # Routers
    dp.include_router(start.router)
    dp.include_router(settings_handler.router)
    dp.include_router(documents.router)

    # Startup/shutdown hooks
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # aiohttp web app
    app = web.Application()
    handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    handler.register(app, path=f"/webhook/{settings.BOT_TOKEN}")
    setup_application(app, dp, bot=bot)

    web.run_app(app, host="127.0.0.1", port=settings.PORT)

if __name__ == "__main__":
    main()
```

### `services/mailer.py`

- Use `aiosmtplib` for async SMTP
- Attach the file as `MIMEBase` with correct `Content-Disposition`
- Subject line: `"Convert"` — this keyword triggers Amazon's auto-conversion for some formats (e.g. `.docx` → Kindle format). Optionally expose this as a user toggle.

### `handlers/documents.py`

- Listen for `F.document` and `F.photo` content types
- On receive: check extension → check size → check kindle email set → download → send → confirm
- Use FSM if you add a confirmation step ("Send `report.pdf` to `myname@kindle.com`? ✅ / ❌")
- Always wrap temp file handling in `try/finally` to guarantee cleanup from `/tmp/`

### `middlewares/db_middleware.py`

- Classic aiogram 3.x `BaseMiddleware` pattern
- Injects `AsyncSession` into handler `data` dict

---

## 🔧 Nginx Configuration

`/etc/nginx/sites-available/bots.conf`

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Kindle Bot webhook
    location /webhook/ {
        proxy_pass         http://127.0.0.1:8001;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_read_timeout 30s;

        # Increase body size limit for file metadata
        # (actual file bytes never pass through here — Telegram
        #  sends only JSON updates, files are fetched separately)
        client_max_body_size 1M;
    }

    # Future bot 2
    # location /bot2_webhook/ {
    #     proxy_pass http://127.0.0.1:8002;
    # }
}

# Redirect HTTP → HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}
```

> 💡 **Important note:** Telegram webhook payloads are pure JSON (update metadata, not binary files). Files are downloaded separately via the Bot API. So `client_max_body_size 1M` is safe — no file bytes pass through Nginx here.

---

## 🔄 Process Management — systemd

`/etc/systemd/system/kindle_bot.service`

```ini
[Unit]
Description=Kindle Sender Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/bots/kindle_bot/app
ExecStart=/opt/bots/kindle_bot/venv/bin/python bot.py
Restart=on-failure
RestartSec=5s
EnvironmentFile=/opt/bots/kindle_bot/.env

# Logging
StandardOutput=append:/opt/bots/kindle_bot/logs/bot.log
StandardError=append:/opt/bots/kindle_bot/logs/bot.log

[Install]
WantedBy=multi-user.target
```

```bash
# Commands you'll use:
systemctl enable kindle_bot    # start on boot
systemctl start kindle_bot
systemctl status kindle_bot
journalctl -u kindle_bot -f    # live logs
```

---

## 🌐 Multi-Project Port Allocation Convention

Since you'll host multiple bots, reserve ports systematically from the start:

| Port | Project |
|---|---|
| `8001` | kindle_bot (this project) |
| `8002` | future bot #2 |
| `8003` | future bot #3 |
| `3000` | future website (Node/Flask/etc.) |
| `3001` | future website #2 |

Each bot gets its own `systemd` service, `virtualenv`, and Nginx `location` block.

---

## 📋 `/help` Message Template

```
📚 Kindle Sender Bot

SETUP (one-time):
1. Use /myemail to get the bot's sender address
2. Go to amazon.com → Manage Your Content and Devices
   → Preferences → Personal Document Settings
   → Approved Personal Document E-mail List → Add the address
3. Use /setkindle your_name@kindle.com to save your Kindle email

SENDING:
Just send any supported file to this chat!

✅ Supported formats:
PDF, EPUB, DOCX, DOC, RTF, TXT, HTML, MOBI
JPG, JPEG, PNG, GIF, BMP, TIFF

⚠️ Limitations:
• Max file size: 20 MB (Telegram Bot API limit)
• Amazon's own limit is 50 MB — larger files need special setup
• EPUB requires a Kindle with updated firmware (2022+)
• Your sender email MUST be whitelisted in Amazon settings
  or documents will not arrive
• Amazon provides 5 GB free storage; older docs may be deleted

ℹ️ Use /status to see your current settings
```

---

## 📦 `requirements.txt`

```
aiogram==3.2.*
aiohttp              # webhook server (aiogram depends on this)
aiosmtplib           # async SMTP
aiosqlite            # async SQLite driver
sqlalchemy[asyncio]  # ORM
pydantic-settings    # config via .env
python-dotenv        # .env loading
```

---

## 🚀 Deployment Checklist (one-time setup)

```bash
# 1. Point your domain A record → VPS IP

# 2. On VPS: install nginx + certbot
apt install nginx certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com

# 3. Create bot directory + virtualenv
mkdir -p /opt/bots/kindle_bot/{app,logs}
python3 -m venv /opt/bots/kindle_bot/venv

# 4. Clone/upload your code
cd /opt/bots/kindle_bot/app
git clone <your_repo> .

# 5. Install dependencies
/opt/bots/kindle_bot/venv/bin/pip install -r requirements.txt

# 6. Create .env file
cp .env.example /opt/bots/kindle_bot/.env
chmod 600 /opt/bots/kindle_bot/.env
nano /opt/bots/kindle_bot/.env   # fill in secrets

# 7. Set up Nginx config + reload
cp nginx/bots.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/bots.conf /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# 8. Enable + start the bot
systemctl enable kindle_bot
systemctl start kindle_bot
systemctl status kindle_bot   # should show "active (running)"
```

---

## ⚠️ VPS Resource Cautions

Given you're on a single 2 GB RAM core shared with other projects:

- **Never load files into RAM** — always stream downloads to disk (`/tmp/`) and delete immediately after emailing
- **Temp file cleanup** — use `try/finally` to guarantee `/tmp/kindle_*` files are deleted even on errors
- **No background threads** — keep everything `async`; one blocking `smtplib` call can freeze the whole process (use `aiosmtplib` strictly)
- **SQLite is fine** for this scale — no need for Postgres on a single-bot SQLite workload
- **Log rotation** — add `logrotate` config to prevent logs filling your disk over time

---

## 🚀 Development Phases

| Phase | Tasks |
|---|---|
| **1 — Local dev** | Build & test everything locally with long-polling (`start_polling`) for fast iteration |
| **2 — VPS prep** | Set up Nginx, SSL, systemd on VPS |
| **3 — Switch to webhook** | Change `bot.py` entrypoint, set `WEBHOOK_BASE_URL`, deploy, test |
| **4 — Polish** | Confirm/cancel keyboard, rate limiting, `/status`, logging |
| **5 — Hardening** | `WEBHOOK_SECRET` header validation, `logrotate`, restrict `/tmp` cleanup |
| **6 — Optional enhancements** | Admin commands (`/stats`, `/broadcast`), Telegram Bot API local server to lift 20 MB cap, "Convert" subject toggle, multi-language support |

> 💡 **Develop locally with long-polling, deploy to VPS with webhooks.** Make this switchable via an env var `MODE=polling|webhook` so you never have to change code between environments.

---

This plan gives you a clean, scalable foundation — every future bot just needs a new port, a new `systemd` service, and a new `location` block in Nginx.
