from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base_model import BaseModel, Base


DEFAULT_STOCK_IMAGE_URL = "https://images.unsplash.com/photo-1629367494173-c78a56567877?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=927&q=80"


class Product(BaseModel, Base):
    __tablename__ = "products"
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(String, ForeignKey("product_categories.id"))
    images = Column(JSONB, nullable=True, default=lambda: [DEFAULT_STOCK_IMAGE_URL])

    cart = relationship("Cart", back_populates="product")
    category = relationship("ProductCategory", back_populates="products")
