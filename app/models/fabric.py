from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base_model import BaseModel, Base


class Fabric(BaseModel, Base):
    __tablename__ = "fabrics"
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    images = Column(JSONB, nullable=True)
