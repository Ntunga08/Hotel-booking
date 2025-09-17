from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from typing import List, Optional
from app.models import models
from app.schemas import schemas

"""payment CRUD operations """
async def create_payment(db: AsyncSession, payment: schemas.PaymentCreate) -> models.Payment:
    """Create a new payment record"""
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

async def get_payment(db: AsyncSession, payment_id: int) -> Optional[models.Payment]:
    """Get a payment by ID"""
    result = await db.execute(
        select(models.Payment).where(models.Payment.id == payment_id)
    )
    return result.scalars().first()

async def get_payments(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Payment]:
    """Get all payments with pagination"""
    result = await db.execute(
        select(models.Payment).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_payment(
    db: AsyncSession, 
    payment_id: int, 
    payment: schemas.PaymentUpdate
) -> Optional[models.Payment]:
    """Update a payment record"""
    update_data = payment.dict(exclude_unset=True)
    
    result = await db.execute(
        update(models.Payment)
        .where(models.Payment.id == payment_id)
        .values(**update_data)
        .returning(models.Payment)
    )
    await db.commit()
    return result.scalars().first()

async def delete_payment(db: AsyncSession, payment_id: int) -> Optional[models.Payment]:
    """Delete a payment record"""
    result = await db.execute(
        delete(models.Payment)
        .where(models.Payment.id == payment_id)
        .returning(models.Payment)
    )
    await db.commit()
    return result.scalars().first()

async def get_payments_by_booking(
    db: AsyncSession, 
    booking_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[models.Payment]:
    """Get all payments for a specific booking"""
    result = await db.execute(
        select(models.Payment)
        .where(models.Payment.booking_id == booking_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_payment_status(
    db: AsyncSession, 
    payment_id: int, 
    status: str
) -> Optional[models.Payment]:
    """Update payment status"""
    result = await db.execute(
        update(models.Payment)
        .where(models.Payment.id == payment_id)
        .values(status=status)
        .returning(models.Payment)
    )
    await db.commit()
    return result.scalars().first()

