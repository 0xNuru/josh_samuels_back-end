#!/usr/bin/env python3

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Measurement(BaseModel, Base):
    __tablename__ = "measurements"
    customer_id = Column(
        String, ForeignKey("customers.id"), nullable=False, primary_key=True
    )
    neck = Column(Float, nullable=True)
    shoulder = Column(Float, nullable=True)
    arm_hole = Column(Float, nullable=True)
    sleeve = Column(Float, nullable=True)
    back = Column(Float, nullable=True)
    front_chest = Column(Float, nullable=True)
    round_chest = Column(Float, nullable=True)
    waist = Column(Float, nullable=True)
    hip = Column(Float, nullable=True)
    crotch = Column(Float, nullable=True)
    thigh = Column(Float, nullable=True)
    knee = Column(Float, nullable=True)
    ankle = Column(Float, nullable=True)
    pant_length = Column(Float, nullable=True)
    images = Column(JSONB, nullable=True)

    customer = relationship("Customer", back_populates="measurement")
