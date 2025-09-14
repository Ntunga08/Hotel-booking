from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import models
from app.schemas import schemas
from sqlalchemy import update, delete
from sqlalchemy import func
from sqlalchemy import  and_, or_
from typing import List, Optional

"""create new  room in database"""
async def create_room(db: AsyncSession, room: schemas.RoomCreate) -> models.Room:
    db_room = models.Room(**room.dict())
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room


