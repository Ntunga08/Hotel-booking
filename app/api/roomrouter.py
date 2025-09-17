from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import schemas
from app.services import room_service
from app.crud import room as crud
from app.db.session import get_db

# Remove the /rooms prefix since it will be added in main.py
router = APIRouter(
    tags=["rooms"]
)

@router.post("/", response_model=schemas.RoomOut)
async def create_room(room: schemas.RoomCreate, db: AsyncSession = Depends(get_db)):
    db_room = await crud.room.get_room_by_number(db, room.room_number)
    if db_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    return await crud.room.create_room(db=db, room=room)

@router.get("/{room_id}", response_model=schemas.RoomOut)
async def read_room(room_id: int, db: AsyncSession = Depends(get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.get("/", response_model=List[schemas.RoomOut])
async def get_rooms(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    rooms = await crud.room.get_rooms(db, skip=skip, limit=limit)
    return rooms

@router.put("/{room_id}", response_model=schemas.RoomOut)
async def update_room(room_id: int, room: schemas.RoomUpdate, db: AsyncSession = Depends(get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.room.update_room(db=db, room_id=room_id, room=room)

@router.delete("/{room_id}", response_model=schemas.RoomOut)
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.room.delete_room(db=db, room_id=room_id)

@router.get("/search", response_model=List[schemas.RoomOut])
async def search_rooms(room_type: str = None, min_price: int = None, max_price: int = None, db: AsyncSession = Depends(get_db)):
    rooms = await crud.room.search_rooms(db, room_type=room_type, min_price=min_price, max_price=max_price)
    return rooms

@router.post("/{room_id}/upload-image", response_model=schemas.RoomOut)
async def upload_room_image(room_id: int, image_path: str, db: AsyncSession = Depends(get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.room.update_room_image(db=db, room_id=room_id, image_path=image_path)

@router.get("/available", response_model=List[schemas.RoomOut])
async def get_available_rooms(check_in_date: str, check_out_date: str, db: AsyncSession = Depends(get_db)):
    rooms = await crud.room.get_available_rooms(db, check_in_date=check_in_date, check_out_date=check_out_date)
    return rooms

@router.get("/with-bookings", response_model=List[schemas.RoomWithBookings])
async def get_rooms_with_bookings(db: AsyncSession = Depends(get_db)):
    rooms = await crud.room.get_rooms_with_bookings(db)
    return rooms







