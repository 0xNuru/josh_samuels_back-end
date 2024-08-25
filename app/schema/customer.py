#!/usr/bin/env python

import re
from datetime import date

from pydantic import BaseModel, EmailStr, SecretStr, model_validator

from app.models.customer import GenderEnum


class CreateCustomer(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password1: SecretStr
    password2: SecretStr

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def verify_password_match(self):
        password1 = self.password1
        password2 = self.password2

        if password1 is None or password2 is None:
            raise ValueError("Both password fields must be provided.")

        password = password1.get_secret_value()
        confirm_password = password2.get_secret_value()

        if password != confirm_password:
            raise ValueError("The two passwords did not match.")

        password_regex = (
            """(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}"""
        )

        if not re.match(password_regex, confirm_password):
            raise ValueError(
                "Password must be at least 8 characters and include alphabets, numbers, and a special character."
            )

        return self


class ShowCustomer(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    gender: GenderEnum | None
    date_of_birth: date | None


class UpdateMeasurement(BaseModel):
    round_head: float
    neck: float
    shoulder: float
    sleeve: float
    flexed_biceps: float
    wrist: float
    back: float
    front_chest: float
    chest: float
    stomach: float
    hip: float
    waist: float
    crotch: float
    thigh: float
    knee: float
    ankle: float
    pant_length: float
    inseam: float
    # front_view_image: str
    # side_view_image: str

    class Config:
        from_attributes = True


class CreateCart(BaseModel):
    quantity: int
    product_id: str

    class Config:
        from_attributes = True
