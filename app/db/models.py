"""SQLAlchemy 2.0 ORM models."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    # Telegram IDs can exceed 32-bit, so use BigInteger.
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    kindle_email: Mapped[str | None] = mapped_column(String(255), default=None)
    # None until set: lets us detect first contact and pick from Telegram locale.
    language: Mapped[str | None] = mapped_column(String(2), default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    documents_sent: Mapped[int] = mapped_column(Integer, default=0)
    convert_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Daily rate-limit bookkeeping.
    sent_today: Mapped[int] = mapped_column(Integer, default=0)
    last_sent_date: Mapped[date | None] = mapped_column(Date, default=None)
