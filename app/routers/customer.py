#!/usr/bin/env python3

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.engine.load import load
from app.models.user import User
from app.models.customer import Customer
from app.schema.customer import CreateCustomer, ShowCustomer
from app.utils import auth


router = APIRouter(prefix="/customer", tags=["Customer Management"])

@router.post("/register", response_model=ShowCustomer, status_code=status.HTTP_201_CREATED)
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
    # message = await send_verification_mail(email, http_request, request)

    new_customer = Customer(
        phone=request.phone,
        email=request.email,
        password_hash=password_hash,
        role="customer",
    )
    db.add(new_customer)
    return new_customer
