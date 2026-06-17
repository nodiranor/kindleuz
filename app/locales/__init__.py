"""Lightweight dict-based i18n: t(), language detection, and display names."""
from __future__ import annotations

from typing import Callable

from locales.translations import TRANSLATIONS

DEFAULT_LANG = "en"
LANGUAGES: tuple[str, ...] = ("uz", "ru", "en")
LANG_NAMES: dict[str, str] = {"uz": "O‘zbekcha", "ru": "Русский", "en": "English"}


def t(key: str, lang: str, **kwargs) -> str:
    """Translate `key` into `lang`, falling back to English then the raw key."""
    table = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])
    template = table.get(key) or TRANSLATIONS[DEFAULT_LANG].get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, IndexError):
            return template
    return template


def detect_lang(code: str | None) -> str:
    """Map a Telegram language_code (e.g. 'ru', 'en-US', 'uz') to a supported lang."""
    if not code:
        return DEFAULT_LANG
    code = code.lower()
    for lang in LANGUAGES:
        if code.startswith(lang):
            return lang
    return DEFAULT_LANG


def get_translator(lang: str) -> Callable[..., str]:
    """Return a `_(key, **kwargs)` bound to a single language."""
    def _(key: str, **kwargs) -> str:
        return t(key, lang, **kwargs)
    return _
