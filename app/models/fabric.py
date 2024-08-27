from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Fabric(BaseModel, Base):
    __tablename__ = "fabrics"
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    images = Column(JSONB, nullable=True)

    prices = relationship("FabricPrice", back_populates="fabric")
