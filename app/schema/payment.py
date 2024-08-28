from pydantic import BaseModel, EmailStr


class Order_id(BaseModel):
    id: str

    class Config:
        from_attributes = True
