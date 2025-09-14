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

async def update_room(db: AsyncSession, room_id: int, room: schemas.RoomUpdate) -> models.Room | None:
    """update room in database"""
    result = await db.execute(select(models.Room).where(models.Room.id==room_id))
    db_room = result.scalars().first()
    if db_room:
        for var, value in vars(room).items():
            setattr(db_room, var, value) if value else None
        db.add(db_room)
        await db.commit()
        await db.refresh(db_room)
        return db_room
    return None

async def delete_room(db: AsyncSession, room_id: int) -> models.Room | None:
    """delete room from database"""
    result = await db.execute(select(models.Room).where(models.Room.id==room_id))
    db_room = result.scalars().first()
    if db_room:
        await db.delete(db_room)
        await db.commit()
        return db_room
    return None
async def count_rooms(db: AsyncSession) -> int:
    """count total number of rooms in database"""
    result = await db.execute(select(func.count(models.Room.id)))
    return result.scalar_one()

async def search_rooms(db: AsyncSession, room_type: Optional[str]= None, min_price: Optional[float]=None, max_price: Optional[float]=None ) -> List[models.Room]:
    """search room based on room type and price range """
    filters=[]
    if room_type:
        filters.append(models.Room.room_type.ilike(f"%{room_type}%"))
    if min_price is not None:
        filters.append(models.Room.price >= min_price)
    if max_price is not None:
        filters.append(models.Room.price <= max_price)
    if filters:
        query = select(models.Room).where(and_(*filters))
    else:
        query = select(models.Room)
    result = await db.execute(query)
    return result.scalars().all()  

