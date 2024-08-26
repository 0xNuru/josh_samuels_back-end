#!/usr/bin/env python3

import enum

from sqlalchemy import Column, Enum, ForeignKey, String, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.user import User


class GenderEnum(enum.Enum):
    M = "Male"
    F = "Female"


class Customer(User):
    """customers table"""

    __tablename__ = "customers"
    id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    first_name: str = Column(String(128), nullable=False)
    last_name: str = Column(String(128), nullable=False)
    date_of_birth = Column(String, nullable=True)
    gender = Column(Enum(GenderEnum, name="genders"), nullable=True)
    address: str = Column(String(256), nullable=True)

    measurement = relationship("Measurement", back_populates="customer")
    cart = relationship("Cart", back_populates="customer")
