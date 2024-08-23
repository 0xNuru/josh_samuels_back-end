from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    price: float
    description: str
    category: str
    stock_quantity: int
    # product_image: str

    class Config:
        from_attributes = True
