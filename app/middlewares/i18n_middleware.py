"""Resolves the user's language and injects `user`, `lang`, and `_` into handlers.

Runs inside DbSessionMiddleware (registered on message/callback_query observers),
so `session` is already present in data.
"""
from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.types import User as TgUser

from db.database import get_or_create_user
from locales import DEFAULT_LANG, detect_lang, get_translator


class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        session = data.get("session")
        tg_user: TgUser | None = data.get("event_from_user")
        if session is not None and tg_user is not None:
            user = await get_or_create_user(session, tg_user.id)
            # Until the user explicitly picks (language is None), render in the
            # locale Telegram reports — but DON'T persist it, so /start can still
            # detect first contact and prompt for a language choice.
            lang = user.language or detect_lang(tg_user.language_code)
            data["user"] = user
            data["lang"] = lang
            data["_"] = get_translator(lang)
        else:
            data.setdefault("lang", DEFAULT_LANG)
            data.setdefault("_", get_translator(DEFAULT_LANG))
        return await handler(event, data)
