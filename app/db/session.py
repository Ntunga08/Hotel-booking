from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from .base import SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    finally:
        await db.close()