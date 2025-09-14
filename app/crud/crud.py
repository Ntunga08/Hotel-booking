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

async def get_room(db: AsyncSession, room_id: int) -> models.Room | None:
    """recieve single room by id from database"""
    result = await db.execute(select(models.Room).where(models.Room.id==room_id))
    return result.scalars().first()

async def get_room_by_number(db: AsyncSession, room_number: str) -> models.Room | None:
    """recieve single room by room number from database"""
    result = await db.execute(select(models.Room).where(models.Room.room_number==room_number))
    return result.scalars().first() 

async def get_rooms(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Room]:
    """recieve all rooms from database"""
    result = await db.execute(select(models.Room).offset(skip).limit(limit))
    return result.scalars().all()   

