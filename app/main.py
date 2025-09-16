from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import engine, get_db
from app.api import room


app = FastAPI(title="Hotel Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(room.router, prefix="/v1/rooms")
app.include_router(user.router, prefix="/v1/users")
app.include_router(booking.router, prefix="/v1/bookings")
app.include_router(payment.router, prefix="/v1/payments")
app.include_router(auth.router, prefix="/v1/auth")
