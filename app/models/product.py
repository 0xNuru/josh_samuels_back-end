from sqlalchemy import Column, Float, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Product(BaseModel, Base):
    __tablename__ = "products"
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    stock_quantity = Column(Integer, default=0)
    product_image = Column(LargeBinary, nullable=True)
    product_image_header = Column(String, nullable=True)

    cart = relationship("Cart", back_populates="product")
