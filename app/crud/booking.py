from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from sqlalchemy import update, delete
from typing import List, Optional
from sqlalchemy import and_, or_
from sqlalchemy import func

"""Booking CRUD operations"""
async def create_booking(db: AsyncSession, booking: schemas.BookingCreate) -> models.Booking:
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking

async def get_booking(db: AsyncSession, booking_id: int) -> models.Booking | None:
    """recieve single booking by id from database"""
    result = await db.execute(select(models.Booking).where(models.Booking.id==booking_id))
    return result.scalars().first()

async def get_bookings(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """recieve all bookings from database"""
    result = await db.execute(select(models.Booking).offset(skip).limit(limit))
    return result.scalars().all()

async def update_booking(db: AsyncSession, booking_id: int, booking: schemas.BookingUpdate) -> models.Booking | None:
    """update booking in database"""
    result = await db.execute(select(models.Booking).where(models.Booking.id==booking_id))
    db_booking = result.scalars().first()
    if db_booking:
        for var, value in vars(booking).items():
            setattr(db_booking, var, value) if value else None
        db.add(db_booking)
        await db.commit()
        await db.refresh(db_booking)
        return db_booking
    return None

async def delete_booking(db: AsyncSession, booking_id: int) -> models.Booking | None:
    """delete booking from database"""
    result = await db.execute(select(models.Booking).where(models.Booking.id==booking_id))
    db_booking = result.scalars().first()
    if db_booking:
        await db.delete(db_booking)
        await db.commit()
        return db_booking
    return None

async def count_bookings(db: AsyncSession) -> int:
    """count total number of bookings in database"""
    result = await db.execute(select(func.count(models.Booking.id)))
    return result.scalar_one()

async def get_bookings_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """recieve all bookings for a specific user from database"""
    result = await db.execute(select(models.Booking).where(models.Booking.user_id==user_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_bookings_by_room(db: AsyncSession, room_id: int, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """recieve all bookings for a specific room from database"""
    result = await db.execute(select(models.Booking).where(models.Booking.room_id==room_id).offset(skip).limit(limit))
    return result.scalars().all()

async def get_bookings_by_status(db: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """recieve all bookings with a specific status from database"""
    result = await db.execute(select(models.Booking).where(models.Booking.status==status).offset(skip).limit(limit))
    return result.scalars().all()

async def search_bookings(db: AsyncSession, user_id: Optional[int]= None, room_id: Optional[int]=None, status: Optional[str]=None ) -> List[models.Booking]:
    """search bookings based on user, room and status """
    filters=[]
    if user_id is not None:
        filters.append(models.Booking.user_id == user_id)
    if room_id is not None:
        filters.append(models.Booking.room_id == room_id)
    if status:
        filters.append(models.Booking.status.ilike(f"%{status}%"))
    if filters:
        query = select(models.Booking).where(and_(*filters))
    else:
        query = select(models.Booking)
    result = await db.execute(query)
    return result.scalars().all()

async def count_bookings_by_status(db: AsyncSession, status: str) -> int:
    """count total number of bookings with a specific status in database"""
    result = await db.execute(select(func.count(models.Booking.id)).where(models.Booking.status==status))
    return result.scalar_one()


