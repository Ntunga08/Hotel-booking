from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import schemas
from app.crud import user as crud
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(
    tags=["users"]
)

@router.get("/me", response_model=schemas.UserOut)
async def read_user_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserOut)
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    return await crud.update_user(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}", response_model=schemas.UserOut)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    return await crud.delete_user(db=db, user_id=user_id)