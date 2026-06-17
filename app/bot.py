"""Entry point. MODE=polling for local dev, MODE=webhook for VPS deployment."""
from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from db.database import create_db_pool, init_db
from handlers import documents, start
from handlers import settings as settings_handler
from middlewares.db_middleware import DbSessionMiddleware
from middlewares.i18n_middleware import LanguageMiddleware

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
ALLOWED_UPDATES = ["message", "callback_query"]


def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    # Make console output UTF-8 safe (Windows consoles default to a legacy
    # codepage; the bot handles Cyrillic/Uzbek text and emoji).
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_DIR / "bot.log", encoding="utf-8"),
        ],
    )


def build_bot() -> Bot:
    return Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(DbSessionMiddleware(create_db_pool()))
    # Runs inside the DB session; injects user/lang/translator for message & callback handlers.
    lang_mw = LanguageMiddleware()
    dp.message.middleware(lang_mw)
    dp.callback_query.middleware(lang_mw)
    dp.include_router(start.router)
    dp.include_router(settings_handler.router)
    dp.include_router(documents.router)
    return dp


async def run_polling() -> None:
    bot = build_bot()
    dp = build_dispatcher()
    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Starting in POLLING mode")
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


def run_webhook() -> None:
    from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
    from aiohttp import web

    bot = build_bot()
    dp = build_dispatcher()

    async def on_startup(bot: Bot) -> None:
        await init_db()
        await bot.set_webhook(
            url=settings.webhook_url,
            secret_token=settings.WEBHOOK_SECRET,
            allowed_updates=ALLOWED_UPDATES,
            drop_pending_updates=True,
        )
        logging.info("Webhook set to %s", settings.webhook_url)

    async def on_shutdown(bot: Bot) -> None:
        await bot.delete_webhook()
        logging.info("Webhook removed")

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=settings.WEBHOOK_SECRET
    ).register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    logging.info("Starting in WEBHOOK mode on 127.0.0.1:%s", settings.PORT)
    web.run_app(app, host="127.0.0.1", port=settings.PORT)


def main() -> None:
    setup_logging()
    if settings.MODE == "webhook":
        run_webhook()
    else:
        asyncio.run(run_polling())


if __name__ == "__main__":
    main()
