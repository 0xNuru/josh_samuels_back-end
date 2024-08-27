from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class ProductCategory(BaseModel, Base):
    __tablename__ = "product_categories"
    name = Column(String, unique=True, nullable=False)

    products = relationship("Product", back_populates="category")
    prices = relationship("FabricPrice", back_populates="product_category")
