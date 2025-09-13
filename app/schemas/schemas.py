from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = "user"    
    class Config:
        orm_mode = True 

class UserCreate(UserBase):
    password: str
    class Config:
        orm_mode = True 

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price: int
    image_path: str
    class Config:
        orm_mode = True

class RoomCreate(RoomBase):
    class Config:
        orm_mode = True

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    price: Optional[int] = None
    image_path: Optional[str] = None
    class Config:
        orm_mode = True

class RoomOut(RoomBase):
    id: int
    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    user_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    status: str
    class Config:
        orm_mode = True

class BookingCreate(BookingBase):
    class Config:
        orm_mode = True

class BookingUpdate(BaseModel):
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    status: Optional[str] = None
    class Config:
        orm_mode = True
class BookingOut(BookingBase):
    id: int
    class Config:
        orm_mode = True 

class PaymentBase(BaseModel):
    booking_id: int
    amount: int
    payment_date: str
    payment_method: str
    status: str
    class Config:
        orm_mode = True