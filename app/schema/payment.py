from pydantic import BaseModel, EmailStr


class Payments(BaseModel):
    email: EmailStr
    amount: str

    class Config:
        from_attributes = True
