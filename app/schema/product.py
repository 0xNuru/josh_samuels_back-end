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


class CreateFabric(BaseModel):
    name: str
    price: float
    category: str
    images: List[str]

    class Config:
        from_attributes = True
