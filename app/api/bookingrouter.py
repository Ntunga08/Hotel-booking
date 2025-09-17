from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import schemas
from app.crud import booking as crud
from app.db.session import get_db

router = APIRouter(
    tags=["bookings"]
)

@router.post("/", response_model=schemas.BookingOut)
async def create_booking(booking: schemas.BookingCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_booking(db=db, booking=booking)

@router.get("/{booking_id}", response_model=schemas.BookingOut)
async def read_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    db_booking = await crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.get("/", response_model=List[schemas.BookingOut])
async def get_bookings(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    bookings = await crud.get_bookings(db, skip=skip, limit=limit)
    return bookings

@router.put("/{booking_id}", response_model=schemas.BookingOut)
async def update_booking(booking_id: int, booking: schemas.BookingUpdate, db: AsyncSession = Depends(get_db)):
    db_booking = await crud.update_booking(db, booking_id=booking_id, booking=booking)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.delete("/{booking_id}", response_model=schemas.BookingOut)
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    db_booking = await crud.delete_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.get("/user/{user_id}", response_model=List[schemas.BookingOut])
async def get_user_bookings(user_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    bookings = await crud.get_bookings_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return bookings

@router.get("/room/{room_id}", response_model=List[schemas.BookingOut])
async def get_room_bookings(room_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    bookings = await crud.get_bookings_by_room(db, room_id=room_id, skip=skip, limit=limit)
    return bookings

@router.get("/status/{status}", response_model=List[schemas.BookingOut])
async def get_bookings_by_status(status: str, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    bookings = await crud.get_bookings_by_status(db, status=status, skip=skip, limit=limit)
    return bookings

@router.get("/search/", response_model=List[schemas.BookingOut])
async def search_bookings(user_id: int = None, room_id: int = None, status: str = None, db: AsyncSession = Depends(get_db)):
    bookings = await crud.search_bookings(db, user_id=user_id, room_id=room_id, status=status)
    return bookings

@router.get("/count/status/{status}", response_model=int)
async def count_status_bookings(status: str, db: AsyncSession = Depends(get_db)):
    count = await crud.count_bookings_by_status(db, status=status)
    return count