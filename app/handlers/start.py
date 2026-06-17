"""/start and /help commands."""
from __future__ import annotations

from typing import Callable

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import settings
from db.models import User
from keyboards.inline import language_keyboard
from utils.validators import ALLOWED_FORMATS_TEXT

router = Router()

_MAX_MB = settings.MAX_FILE_SIZE_BYTES // 1024 // 1024


@router.message(CommandStart())
async def cmd_start(message: Message, user: User, _: Callable[..., str]) -> None:
    if user.language is None:
        # First contact: choose a language before anything else. The welcome
        # follows once they tap a language (see on_language_set).
        await message.answer(_("language_choose"), reply_markup=language_keyboard())
        return
    await message.answer(_("welcome"))


@router.message(Command("help"))
async def cmd_help(message: Message, _: Callable[..., str]) -> None:
    await message.answer(_("help", formats=ALLOWED_FORMATS_TEXT, max_mb=_MAX_MB))
