from pydantic import BaseModel
from typing import List


class CreateProduct(BaseModel):
    name: str
    price: float
    description: str
    category: str
    images: List[str]

    class Config:
        from_attributes = True


class FabricPriceData(BaseModel):
    product_id: str
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
