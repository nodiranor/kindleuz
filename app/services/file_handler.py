"""Telegram file metadata extraction, temp download, and cleanup."""
from __future__ import annotations

import logging
import os
import uuid
from dataclasses import dataclass

from aiogram import Bot
from aiogram.types import Message

from config import settings
from utils.validators import get_extension

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FileMeta:
    file_id: str
    filename: str
    size: int  # bytes; 0 if Telegram did not report it
    ext: str


def extract_meta(message: Message) -> FileMeta | None:
    """Pull file info from a document or photo message. Returns None otherwise."""
    if message.document:
        doc = message.document
        filename = doc.file_name or f"document_{doc.file_unique_id}"
        return FileMeta(doc.file_id, filename, doc.file_size or 0, get_extension(filename))
    if message.photo:
        # Photos arrive as multiple sizes with no filename — take the largest.
        photo = message.photo[-1]
        filename = f"photo_{photo.file_unique_id}.jpg"
        return FileMeta(photo.file_id, filename, photo.file_size or 0, ".jpg")
    return None


async def download_to_temp(bot: Bot, file_id: str, filename: str) -> str:
    """Stream a Telegram file straight to disk (never into RAM). Returns the path."""
    ext = get_extension(filename) or ".bin"
    path = os.path.join(settings.TEMP_DIR, f"kindle_{uuid.uuid4().hex}{ext}")
    await bot.download(file_id, destination=path)
    return path


def cleanup(path: str | None) -> None:
    """Best-effort temp-file removal; safe to call in a finally block."""
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            logger.warning("Could not delete temp file %s", path, exc_info=True)
