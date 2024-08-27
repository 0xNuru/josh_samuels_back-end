from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel, Base


class FabricPrice(BaseModel, Base):
    __tablename__ = "fabric_prices"
    fabric_id = Column(String, ForeignKey("fabrics.id"), nullable=False)
    price = Column(Float, nullable=False)
    product_category_id = Column(
        String, ForeignKey("product_categories.id"), nullable=False
    )

    fabric = relationship("Fabric", back_populates="prices")
    product_category = relationship("ProductCategory", back_populates="prices")
