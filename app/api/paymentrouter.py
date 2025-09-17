from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import schemas
from app.crud import payment as crud
from app.db.session import get_db
from app.services.pesapal_service import PesapalService

router = APIRouter(
    tags=["payments"]
)

pesapal_service = PesapalService()

@router.post("/initiate", response_model=schemas.PaymentOut)
async def initiate_payment(
    payment: schemas.PaymentCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # Initialize Pesapal payment
    payment_url = await pesapal_service.initiate_payment(
        amount=payment.amount,
        description=f"Payment for booking {payment.booking_id}",
        callback_url="/api/v1/payments/callback"
    )
    
    # Create payment record
    db_payment = await crud.create_payment(db=db, payment=payment)
    
    # Add background task to check payment status
    background_tasks.add_task(
        pesapal_service.check_payment_status,
        payment_id=db_payment.id
    )
    
    return {"payment_url": payment_url, "payment": db_payment}

@router.get("/callback")
async def payment_callback(
    pesapal_merchant_reference: str,
    pesapal_transaction_tracking_id: str,
    db: AsyncSession = Depends(get_db)
):
    # Verify payment with Pesapal
    payment_status = await pesapal_service.verify_payment(
        merchant_reference=pesapal_merchant_reference,
        tracking_id=pesapal_transaction_tracking_id
    )
    
    # Update payment status in database
    await crud.update_payment_status(
        db=db,
        payment_id=pesapal_merchant_reference,
        status=payment_status
    )
    
    return {"status": "success"}

@router.get("/{payment_id}", response_model=schemas.PaymentOut)
async def read_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    db_payment = await crud.get_payment(db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.get("/booking/{booking_id}", response_model=List[schemas.PaymentOut])
async def get_booking_payments(booking_id: int, db: AsyncSession = Depends(get_db)):
    payments = await crud.get_payments_by_booking(db, booking_id=booking_id)
    return payments