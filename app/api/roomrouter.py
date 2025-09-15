from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, db
from app.db import session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

@router.post("/", response_model=schemas.Room)
async def create_room(room: schemas.RoomCreate, db: AsyncSession = Depends(session.get_db)):
    db_room = await crud.room.get_room_by_number(db, room.room_number)
    if db_room:
        raise HTTPException(status_code=400, detail="Room already exists")
    return await crud.room.create_room(db=db, room=room)

@router.get("/{room_id}", response_model=schemas.Room)
async def read_room(room_id: int, db: AsyncSession = Depends(session.get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.get("/", response_model=list[schemas.Room])
async def read_rooms(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(session.get_db)):
    rooms = await crud.room.get_rooms(db, skip=skip, limit=limit)
    return rooms

@router.put("/{room_id}", response_model=schemas.Room)
async def update_room(room_id: int, room: schemas.RoomUpdate, db: AsyncSession = Depends(session.get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.room.update_room(db=db, room_id=room_id, room=room)

@router.delete("/{room_id}", response_model=schemas.Room)
async def delete_room(room_id: int, db: AsyncSession = Depends(session.get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.room.delete_room(db=db, room_id=room_id)

@router.get("/search/", response_model=list[schemas.Room])
async def search_rooms(room_type: str = None, min_price: int = None, max_price: int = None, db: AsyncSession = Depends(session.get_db)):
    rooms = await crud.room.search_rooms(db, room_type=room_type, min_price=min_price, max_price=max_price)
    return rooms

@router.post("/{room_id}/upload-image/", response_model=schemas.Room)
async def upload_room_image(room_id: int, image_path: str, db: AsyncSession = Depends(session.get_db)):
    db_room = await crud.room.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return await crud.room.update_room_image(db=db, room_id=room_id, image_path=image_path)

@router.get("/available/", response_model=list[schemas.Room])
async def get_available_rooms(check_in_date: str, check_out_date: str, db: AsyncSession = Depends(session.get_db)):
    rooms = await crud.room.get_available_rooms(db, check_in_date=check_in_date, check_out_date=check_out_date)
    return rooms

@router.get("/with-bookings/", response_model=list[schemas.RoomWithBookings])
async def get_rooms_with_bookings(db: AsyncSession = Depends(session.get_db)):
    rooms = await crud.room.get_rooms_with_bookings(db)
    return rooms







