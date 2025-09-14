from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from sqlalchemy import update, delete
from typing import List, Optional
from sqlalchemy import and_, or_
from sqlalchemy import func

"""create new user in database"""
async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user 

async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    """recieve single user by id from database"""
    result = await db.execute(select(models.User).where(models.User.id==user_id))
    return result.scalars().first() 

async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    """recieve single user by email from database"""
    result = await db.execute(select(models.User).where(models.User.email==email))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.User]:
    """recieve all users from database"""
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

