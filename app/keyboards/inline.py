"""Inline keyboards. File metadata lives in FSM state, not callback_data
(file_id can exceed Telegram's 64-byte callback_data limit)."""
from __future__ import annotations

from typing import Callable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from locales import LANG_NAMES

CONFIRM_SEND = "snd:ok"
CANCEL_SEND = "snd:no"
LANG_PREFIX = "lang:"

_FLAGS = {"uz": "🇺🇿", "ru": "🇷🇺", "en": "🇬🇧"}


def confirm_send_keyboard(_: Callable[..., str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=_("btn_send"), callback_data=CONFIRM_SEND)
    builder.button(text=_("btn_cancel"), callback_data=CANCEL_SEND)
    builder.adjust(2)
    return builder.as_markup()


def language_keyboard() -> InlineKeyboardMarkup:
    """Each language shown in its own name — independent of current locale."""
    builder = InlineKeyboardBuilder()
    for code in ("uz", "ru", "en"):
        builder.button(text=f"{_FLAGS[code]} {LANG_NAMES[code]}", callback_data=f"{LANG_PREFIX}{code}")
    builder.adjust(1)
    return builder.as_markup()
