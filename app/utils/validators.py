"""File-type and Kindle-email validation helpers."""
from __future__ import annotations

import re
from pathlib import Path

# Amazon Personal Document Service accepted formats.
ALLOWED_EXTENSIONS: frozenset[str] = frozenset({
    ".pdf", ".doc", ".docx", ".rtf", ".txt", ".htm", ".html",
    ".mobi", ".epub",
    # Images:
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
})

# Common formats Amazon does NOT accept — rejected with an explicit hint.
REJECTED_EXTENSIONS: frozenset[str] = frozenset({".zip", ".cbz", ".fb2", ".djvu"})

# Human-readable list for /help and rejection messages.
ALLOWED_FORMATS_TEXT = "PDF, DOC, DOCX, RTF, TXT, HTM, HTML, MOBI, EPUB, JPG, JPEG, PNG, GIF, BMP, TIFF"

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def is_allowed_extension(filename: str) -> bool:
    return get_extension(filename) in ALLOWED_EXTENSIONS


def is_valid_kindle_email(email: str) -> bool:
    """Valid email shape AND a kindle.com (or *.kindle.com, e.g. free.kindle.com) host."""
    email = email.strip()
    if not _EMAIL_RE.match(email):
        return False
    domain = email.rsplit("@", 1)[1].lower()
    return domain == "kindle.com" or domain.endswith(".kindle.com")
