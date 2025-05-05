from sqlalchemy.orm import relationship
from datetime import date, datetime
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
    city = Column(String)
    age = Column(Integer)


class TreeState(Base):
    __tablename__ = "tree_states"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date, default=date.today)
    emotion = Column(String)
    leaf_color = Column(String)
    has_flowers = Column(Boolean, default=False)
    falling_leaves = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
