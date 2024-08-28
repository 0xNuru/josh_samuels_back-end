from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class Cart(BaseModel, Base):
    __tablename__ = "cart"
    customer_id = Column(
        String, ForeignKey("customers.id"), nullable=False, primary_key=True
    )
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    stauts = Column(String, nullable=True)
    paid_at = Column(String, nullable=True)
    amount_paid = Column(Integer, nullable=True)

    customer = relationship("Customer", back_populates="cart")
    product = relationship("Product", back_populates="cart")
