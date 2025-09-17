from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = "user"    
    class Config:
        from_attributes = True 

class UserCreate(UserBase):
    password: str
    class Config:

        from_attributes = True 

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    class Config:
        from_attributes = True

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price: int
    image_path: str
    class Config:
        from_attributes = True

class RoomCreate(RoomBase):
    class Config:
        from_attributes = True

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    price: Optional[int] = None
    image_path: Optional[str] = None
    class Config:
        from_attributes = True

class RoomOut(RoomBase):
    id: int
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    user_id: int
    room_id: int
    check_in_date: str
    check_out_date: str
    status: str
    class Config:
        from_attributes = True

class BookingCreate(BookingBase):
    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    status: Optional[str] = None
    class Config:
        from_attributes = True
class BookingOut(BookingBase):
    id: int
    class Config:
        from_attributes = True 

class PaymentBase(BaseModel):
    booking_id: int
    amount: int
    payment_date: str
    payment_method: str
    status: str
    class Config:
        from_attributes = True

class PaymentCreate(PaymentBase):
    class Config:
        from_attributes = True

class PaymentUpdate(BaseModel):
    amount: Optional[int] = None
    payment_date: Optional[str] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    class Config:
        from_attributes = True

class PaymentOut(PaymentBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True

class BookingInRoom(BaseModel):
    id: int
    check_in_date: str
    check_out_date: str
    status: str
    user_id: int
    
    class Config:
        from_attributes = True

class RoomWithBookings(RoomOut):
    bookings: List[BookingInRoom]
    
    class Config:
        from_attributes = True
