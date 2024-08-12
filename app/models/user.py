#!/usr/bin/env python3

from sqlalchemy import Column, String, Boolean

from app.models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """users table"""

    __tablename__ = "users"
    email = Column(String(32), unique=True, nullable=False)
    phone: str = Column(String(32), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String(32), nullable=False)
   