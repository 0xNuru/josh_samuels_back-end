from pydantic import BaseModel
from typing import List


class ProductSchema(BaseModel):
    name: str
    price: float
    description: str
    category_id: str
    images: List[str]

    class Config:
        from_attributes = True


class FabricPriceData(BaseModel):
    product_category: str
    price: float

    class Config:
        from_attributes = True


class FabricSchema(BaseModel):
    name: str
    category: str
    prices: List[FabricPriceData]
    images: List[str]

    class Config:
        from_attributes = True


class ProductCategorySchema(BaseModel):
    name: str
