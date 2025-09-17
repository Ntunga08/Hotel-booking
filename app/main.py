from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import roomrouter, userrouter, bookingrouter, paymentrouterfrom app.api import roomrouter, userrouter, bookingrouter, paymentrouter

app = FastAPI(
    title="Hotel Management System",
    description="API for managing hotel rooms, bookings, and payments", for managing hotel rooms, bookings, and payments",
    version="1.0.0",   version="1.0.0",
))

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default portlocalhost:5173"],  # Vite default port
    allow_credentials=True,ue,
    allow_methods=["*"],
    allow_headers=["*"],   allow_headers=["*"],
))

# Include routers with proper prefixes and tagsith proper prefixes and tags
app.include_router(
    userrouter.router,
    prefix="/api/v1/users",1/users",
    tags=["users"]   tags=["users"]
))

app.include_router(
    roomrouter.router,
    prefix="/api/v1/rooms",1/rooms",
    tags=["rooms"]   tags=["rooms"]
))

app.include_router(
    bookingrouter.router,
    prefix="/api/v1/bookings",ookings",
    tags=["bookings"]   tags=["bookings"]
))

app.include_router(
    paymentrouter.router,
    prefix="/api/v1/payments",ayments",
    tags=["payments"]   tags=["payments"]
))

# Root endpoint
@app.get("/", tags=["root"])s=["root"])
async def root():ot():
    return {
        "message": "Welcome to Hotel Management System API",to Hotel Management System API",
        "docs": "/api/docs",
        "redoc": "/api/redoc"   "redoc": "/api/redoc"
    }    }

