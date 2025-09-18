from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import roomrouter, userrouter, bookingrouter, paymentrouter

app = FastAPI(
    title="Hotel Management System",
    description="API for managing hotel rooms, bookings, and payments",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes and tags
app.include_router(
    userrouter.router,
    prefix="/v1/users",
    tags=["users"],
)

app.include_router(
    roomrouter.router,
    prefix="/v1/rooms",
    tags=["rooms"],
)

app.include_router(
    bookingrouter.router,
    prefix="/v1/bookings",
    tags=["bookings"],
)

app.include_router(
    paymentrouter.router,
    prefix="/v1/payments",
    tags=["payments"],
)

