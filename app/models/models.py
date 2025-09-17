from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, nullable=False)
    room_type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image_path = Column(String, nullable=True)
    
    # Relationships
    bookings = relationship("Booking", back_populates="room")


class User(Base):  # Changed from 'user' to 'User'
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    role = Column(String, nullable=False)

    bookings = relationship('Booking', back_populates='user')  # Changed from 'Bookings' to 'bookings'


class Booking(Base):
    __tablename__ = 'bookings'  # Fixed from __Booking__ to __tablename__
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in_date = Column(String, nullable=False)
    check_out_date = Column(String, nullable=False)
    status = Column(String, nullable=False)

    user = relationship('User', back_populates='bookings')  # Updated to match User class
    room = relationship('Room', back_populates='bookings')  # Updated to match Room class
    payments = relationship('Payment', back_populates='booking')


class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_date = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False)

    booking = relationship('Booking', back_populates='payments')


