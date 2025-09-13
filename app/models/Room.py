from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key =True,index=True )
    room_number = Column(String, unique=True, index=True, nullable=False)
    room_type =Column(String, nullbale=False)
    price = Column(Integer, nullable=False)
    image_path = Column(String, nullable=False)


class user(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Booking(Base):
    __Booking__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in_date = Column(String, nullable=False)
    check_out_date = Column(String, nullable=False)
    status = Column(String, nullable=False)



