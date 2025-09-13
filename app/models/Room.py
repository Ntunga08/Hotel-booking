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
    username = Column(String, unique=True, index=True, nullable=False)
    email = (String, unique=True, index=True, nullable=False )
    hashed_password = Column(String, nullable=False)