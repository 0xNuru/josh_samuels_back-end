#!/usr/bin/env python3

import base64
import binascii

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.engine.load import load
from app.models.measurements import Measurement
from app.models.user import User
from app.models.customer import Customer
from app.schema.customer import CreateCustomer, UpdateMeasurement
from app.utils import auth



router = APIRouter(prefix="/customer", tags=["Customer Management"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: CreateCustomer, http_request: Request, db: Session = Depends(load)):
    """
    Registers a new customer user.

    Parameters:
    - request (CreateCustomer): An object containing the details of the new admin user.
    - db (Session): A database session object.

    Returns:
    - ShowCustomer: An object containing the details of the newly created custmer user.

    Raises:
    - HTTPException: If a user with the same phone number or email already exists.

    The function first checks if a user with the same phone number or email already exists in the database. 
    If such a user is found, it raises an HTTPException with a status code of 409 (Conflict) 
    and a message indicating the existence of the duplicate user.

    If no such user is found, the function hashes the password using the `auth.get_password_hash` 
    function and creates a new `custmer` object with the provided details. 
    It then adds the new admin user to the database session and returns the newly created admin user as an object.
    Note that password has to be at least 8 characters and include alphabets, numbers, and a special character.
    """
    phone = request.phone
    email = request.email.strip().lower()

    check_phone = db.query_eng(User).filter(User.phone == phone).first()
    check_email = db.query_eng(User).filter(User.email == email).first()

    if check_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": f"user with phone: {phone} exists"}],
        )
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[{"msg": f"user with email: {email} exists"}],
        )
    password_hash = auth.get_password_hash(request.password1.get_secret_value())
    message = await auth.send_verification_mail(email, http_request, request)

    new_customer = Customer(
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        email=request.email,
        password_hash=password_hash,
        role="customer",
    )
    db.add(new_customer)
    return {
        "first_name": request.first_name,
        "email": email,
        "message": message
        }

@router.patch("/update_measurement", status_code=status.HTTP_200_OK)
def update_measurement(request: UpdateMeasurement, db: Session = Depends(load), user: User = Depends(auth.get_current_user)):
    measurements = db.query_eng(Measurement).filter(Measurement.customer_id == user.id).first()
    if measurements:
        for key, value in request.model_dump(exclude_unset=True).items():
            if value not in (None, ""):
                if key == "image":
                    if value.startswith('data:image') and ';base64,' in value:
                        header, value = value.split(';base64,')
                    # convert base64 image to binary
                    try:
                        value = base64.b64decode(value)
                        setattr(measurements, "image_header", header)
                    except binascii.Error:
                        raise HTTPException(
                            status_code=400, detail=[{"msg": "Invalid base64-encoded string for image"}]
                        )
                setattr(measurements, key, value)        
        db.add(measurements)
        return (measurements)
    else:
        new_measurements = Measurement(
            customer_id=user.id,
            **request.model_dump()
        )
        db.add(new_measurements)
        return (new_measurements)
