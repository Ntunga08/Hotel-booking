from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from app.models import models
from app.schemas import schemas
from app.core.security import get_password_hash

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        **user.dict(exclude={'password'}),
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    """Get a user by ID"""
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[models.User]:
    """Get a user by email"""
    result = await db.execute(
        select(models.User).where(models.User.email == email)
    )
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get all users with pagination"""
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_user(
    db: AsyncSession, 
    user_id: int, 
    user: schemas.UserUpdate
) -> Optional[models.User]:
    """Update a user's information"""
    update_data = user.dict(exclude_unset=True)
    
    result = await db.execute(
        update(models.User)
        .where(models.User.id == user_id)
        .values(**update_data)
        .returning(models.User)
    )
    await db.commit()
    return result.scalars().first()

async def delete_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    """Delete a user"""
    result = await db.execute(
        delete(models.User)
        .where(models.User.id == user_id)
        .returning(models.User)
    )
    await db.commit()
    return result.scalars().first()

async def verify_user(db: AsyncSession, email: str, password: str) -> Optional[models.User]:
    """Verify user credentials"""
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

