"""Document/photo intake → validate → confirm → email to Kindle."""
from __future__ import annotations

import logging
from datetime import date
from typing import Callable

from aiogram import Bot, F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.models import User
from keyboards.inline import CANCEL_SEND, CONFIRM_SEND, confirm_send_keyboard
from services import file_handler, mailer
from utils.validators import REJECTED_EXTENSIONS, ALLOWED_FORMATS_TEXT, is_allowed_extension

logger = logging.getLogger(__name__)
router = Router()

_SENDER = html.quote(settings.SENDER_EMAIL or "(not configured)")
_MAX_MB = settings.MAX_FILE_SIZE_BYTES // 1024 // 1024


@router.message(F.document | F.photo)
async def on_file(
    message: Message, state: FSMContext, user: User, _: Callable[..., str]
) -> None:
    meta = file_handler.extract_meta(message)
    if meta is None:
        return

    if not is_allowed_extension(meta.filename):
        hint = _("unsupported_hint", ext=meta.ext) if meta.ext in REJECTED_EXTENSIONS else ""
        await message.answer(
            _("unsupported", ext=html.quote(meta.ext or "?"), hint=hint, formats=ALLOWED_FORMATS_TEXT)
        )
        return

    if meta.size and meta.size > settings.MAX_FILE_SIZE_BYTES:
        await message.answer(_("too_large", max_mb=_MAX_MB))
        return

    if not user.kindle_email:
        await message.answer(_("no_kindle"))
        return

    if settings.RATE_LIMIT_PER_DAY > 0:
        used_today = user.sent_today if user.last_sent_date == date.today() else 0
        if used_today >= settings.RATE_LIMIT_PER_DAY:
            await message.answer(_("rate_limited", limit=settings.RATE_LIMIT_PER_DAY))
            return

    await state.update_data(file_id=meta.file_id, filename=meta.filename)
    await message.answer(
        _("confirm_prompt", filename=html.quote(meta.filename), email=html.quote(user.kindle_email)),
        reply_markup=confirm_send_keyboard(_),
    )


@router.callback_query(F.data == CONFIRM_SEND)
async def on_confirm(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
    bot: Bot,
    user: User,
    _: Callable[..., str],
) -> None:
    data = await state.get_data()
    await state.clear()
    file_id = data.get("file_id")
    filename = data.get("filename")
    if not file_id or not filename:
        await callback.answer(_("expired"), show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=None)
        return

    if not user.kindle_email:
        await callback.answer()
        await callback.message.edit_text(_("set_kindle_first"))
        return

    await callback.answer(_("sending"))
    await callback.message.edit_reply_markup(reply_markup=None)

    path = None
    try:
        path = await file_handler.download_to_temp(bot, file_id, filename)
        await mailer.send_to_kindle(
            user.kindle_email, path, filename, convert=user.convert_enabled
        )

        today = date.today()
        user.sent_today = user.sent_today + 1 if user.last_sent_date == today else 1
        user.last_sent_date = today
        user.documents_sent += 1
        await session.commit()

        await callback.message.edit_text(
            _("sent_ok", filename=html.quote(filename), email=html.quote(user.kindle_email), sender=_SENDER)
        )
    except Exception:
        logger.exception("Failed to send document to Kindle")
        await callback.message.edit_text(_("send_error"))
    finally:
        file_handler.cleanup(path)


@router.callback_query(F.data == CANCEL_SEND)
async def on_cancel(
    callback: CallbackQuery, state: FSMContext, _: Callable[..., str]
) -> None:
    await state.clear()
    await callback.answer(_("cancelled_answer"))
    await callback.message.edit_text(_("cancelled"))
