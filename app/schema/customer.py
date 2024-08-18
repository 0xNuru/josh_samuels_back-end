#!/usr/bin/env python

import re

from pydantic import BaseModel, EmailStr, SecretStr, model_validator


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
    email: EmailStr

class UpdateMeasurement(BaseModel):
    round_head: float = None
    neck: float = None
    shoulder: float = None
    sleeve: float = None
    flexed_biceps: float = None
    wrist: float = None
    back: float = None
    front_chest: float = None
    chest: float = None
    stomach: float = None
    hip: float = None
    waist: float = None
    crotch: float = None
    thigh: float = None
    knee: float = None
    ankle: float = None
    pant_length: float = None
    inseam: float = None
    # front_view_image: str = None
    # side_view_image: str = None

    class Config:
        from_attributes = True