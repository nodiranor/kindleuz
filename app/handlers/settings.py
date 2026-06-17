"""/setkindle, /myemail, /status, /convert, /language, /cancel + language callback."""
from __future__ import annotations

from typing import Callable

from aiogram import F, Router, html
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.models import User
from keyboards.inline import LANG_PREFIX, language_keyboard
from locales import LANG_NAMES, t
from utils.validators import is_valid_kindle_email

router = Router()

_SENDER = html.quote(settings.SENDER_EMAIL or "(not configured)")


class SetKindle(StatesGroup):
    waiting_for_email = State()


async def _save_kindle(
    message: Message,
    candidate: str,
    session: AsyncSession,
    user: User,
    state: FSMContext,
    _: Callable[..., str],
) -> None:
    """Validate + persist a Kindle address. Stays in-state on invalid input so
    the user can just retry; clears state and confirms on success."""
    candidate = candidate.strip()
    if not is_valid_kindle_email(candidate):
        await message.answer(_("setkindle_invalid"))
        return
    user.kindle_email = candidate
    await session.commit()
    await state.clear()
    await message.answer(_("setkindle_saved", email=html.quote(candidate), sender=_SENDER))


@router.message(Command("setkindle"))
async def cmd_setkindle(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    user: User,
    state: FSMContext,
    _: Callable[..., str],
) -> None:
    arg = (command.args or "").strip()
    if arg:
        # Power-user form: /setkindle name@kindle.com on one line.
        await _save_kindle(message, arg, session, user, state, _)
        return
    # Conversational form: ask, then capture the user's next message.
    await state.set_state(SetKindle.waiting_for_email)
    await message.answer(_("setkindle_prompt"))


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext, _: Callable[..., str]) -> None:
    if await state.get_state() is None:
        await message.answer(_("cancel_nothing"))
        return
    await state.clear()
    await message.answer(_("action_cancelled"))


@router.message(Command("myemail"))
async def cmd_myemail(message: Message, _: Callable[..., str]) -> None:
    await message.answer(_("myemail", sender=_SENDER))


@router.message(Command("status"))
async def cmd_status(
    message: Message, user: User, lang: str, _: Callable[..., str]
) -> None:
    kindle = html.quote(user.kindle_email) if user.kindle_email else _("status_no_kindle")
    convert = _("state_on") if user.convert_enabled else _("state_off")
    await message.answer(
        _(
            "status",
            kindle=kindle,
            count=user.documents_sent,
            convert=convert,
            lang=LANG_NAMES.get(lang, lang),
        )
    )


@router.message(Command("convert"))
async def cmd_convert(
    message: Message, session: AsyncSession, user: User, _: Callable[..., str]
) -> None:
    user.convert_enabled = not user.convert_enabled
    await session.commit()
    await message.answer(_("convert_on") if user.convert_enabled else _("convert_off"))


@router.message(Command("language", "til", "язык"))
async def cmd_language(message: Message, _: Callable[..., str]) -> None:
    await message.answer(_("language_choose"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith(LANG_PREFIX))
async def on_language_set(
    callback: CallbackQuery, session: AsyncSession, user: User
) -> None:
    new_lang = callback.data.removeprefix(LANG_PREFIX)
    if new_lang not in LANG_NAMES:
        await callback.answer()
        return
    was_unset = user.language is None
    user.language = new_lang
    await session.commit()
    await callback.answer()
    # Confirm in the freshly chosen language.
    await callback.message.edit_text(t("language_set", new_lang))
    if was_unset:
        # First-run onboarding — greet now that we know their language.
        await callback.message.answer(t("welcome", new_lang))


# Registered LAST so command handlers above win first; only fires while we're
# waiting for the email, and only for text messages (a photo falls through).
@router.message(SetKindle.waiting_for_email, F.text)
async def on_kindle_email(
    message: Message,
    session: AsyncSession,
    user: User,
    state: FSMContext,
    _: Callable[..., str],
) -> None:
    await _save_kindle(message, message.text, session, user, state, _)
