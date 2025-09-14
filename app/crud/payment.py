from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from sqlalchemy import update, delete
from typing import List, Optional
from sqlalchemy import and_, or_
from sqlalchemy import func

"""payment CRUD operations """
async def create_payment(db: AsyncSession, payment: schemas.PaymentCreate) -> models.Payment:
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

async def get_payment(db: AsyncSession, payment_id: int) -> Optional[models.Payment]:
    """get payment by id"""
    result = await db.execute(select(models.Payment).where(models.Payment.id == payment_id))
    return result.scalars().first()

async def get_payments(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Payment]:
    result = await db.execute(select(models.Payment).offset(skip).limit(limit))
    return result.scalars().all()

