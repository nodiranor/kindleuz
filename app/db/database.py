"""Async engine, session factory, and one-time schema bootstrap."""
from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import settings
from db.models import Base, User

engine = create_async_engine(settings.DATABASE_URL, echo=False)


def _migrate(connection) -> None:
    """Tiny in-place migration for SQLite (no Alembic). Adds new columns to an
    existing `users` table created before they were introduced."""
    existing = {col["name"] for col in inspect(connection).get_columns("users")}
    if "language" not in existing:
        connection.execute(text("ALTER TABLE users ADD COLUMN language VARCHAR(2)"))


def create_db_pool() -> async_sessionmaker[AsyncSession]:
    """Return a session factory bound to the shared engine."""
    return async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    """Create tables if they don't exist, then apply small in-place migrations."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_migrate)


async def get_or_create_user(session: AsyncSession, telegram_id: int) -> User:
    """Fetch the user row, inserting a fresh one on first contact."""
    user = await session.get(User, telegram_id)
    if user is None:
        user = User(telegram_id=telegram_id)
        session.add(user)
        await session.flush()
    return user
