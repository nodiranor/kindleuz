"""Application configuration loaded from environment / .env (pydantic-settings v2)."""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env lives at the repo root (one level above app/). Resolve it absolutely so
# the bot finds it no matter what the current working directory is.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ─── Run mode ────────────────────────────────────────────────────────────
    MODE: Literal["polling", "webhook"] = "polling"

    # ─── Telegram ──────────────────────────────────────────────────────────--
    BOT_TOKEN: str

    # ─── Webhook (only required when MODE=webhook) ─────────────────────────────
    WEBHOOK_BASE_URL: str = ""
    WEBHOOK_SECRET: str = ""
    WEBHOOK_PATH: str = "/webhook"
    PORT: int = 8001

    # ─── SMTP ──────────────────────────────────────────────────────────────--
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SENDER_EMAIL: str = ""  # defaults to SMTP_USER below; whitelisted at Amazon
    # Set False when the mail host's TLS cert name mismatches (common on shared
    # hosting "mail.*" aliases). CA-chain trust stays on; only hostname is relaxed.
    SMTP_VERIFY_HOSTNAME: bool = True

    # ─── App ───────────────────────────────────────────────────────────────--
    MAX_FILE_SIZE_BYTES: int = 20 * 1024 * 1024  # 20 MB (Telegram Bot API cap)
    DATABASE_URL: str = "sqlite+aiosqlite:///./kindle_bot.db"
    TEMP_DIR: str = ""  # blank -> OS temp dir
    RATE_LIMIT_PER_DAY: int = 30  # 0 = unlimited

    @property
    def webhook_url(self) -> str:
        """Full public webhook URL Telegram will POST updates to."""
        return f"{self.WEBHOOK_BASE_URL.rstrip('/')}{self.WEBHOOK_PATH}"

    @model_validator(mode="after")
    def _finalize(self) -> "Settings":
        if not self.SENDER_EMAIL:
            self.SENDER_EMAIL = self.SMTP_USER
        if not self.TEMP_DIR:
            self.TEMP_DIR = tempfile.gettempdir()
        if self.MODE == "webhook":
            missing = [
                name
                for name in ("WEBHOOK_BASE_URL", "WEBHOOK_SECRET")
                if not getattr(self, name)
            ]
            if missing:
                raise ValueError(
                    f"MODE=webhook requires these settings: {', '.join(missing)}"
                )
        return self


settings = Settings()
