#!/usr/bin/env python3

import base64
import binascii
from typing import Optional
import uuid

import boto3

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config.config import settings
from app.engine.load import load
from app.models.measurements import Measurement
from app.models.user import User
from app.models.cart import Cart  # This is to avoid sqlalchemy.exc.InvalidRequestError
from app.models.customer import Customer
from app.schema.customer import (
    CreateCart,
    CreateCustomer,
    ShowCustomer,
    UpdateCustomer,
    MeasurementSchema,
)
from app.utils import auth


router = APIRouter(prefix="/customer", tags=["Customer Management"])
s3_client = boto3.client(
    "s3",
    region_name=settings.S3_REGION,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: CreateCustomer, http_request: Request, db: Session = Depends(load)
):
    """
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
    return {"first_name": request.first_name, "email": email, "message": message}


@router.patch("/update_measurement", status_code=status.HTTP_200_OK)
def update_measurement(
    request: MeasurementSchema,
    db: Session = Depends(load),
    user: User = Depends(auth.get_current_user),
):
    """
    Parameters:
    - request (UpdateMeasurement): An object containing the updated measurement details.
    - db (Session): A database session object.
    - user (User): The current user object.

    Returns:
    - Measurement: An object containing the updated measurement details.

    This function first checks if a measurement record exists for the current user.
    If a record exists, it updates the existing record with the provided details.
    If no record exists, it creates a new measurement record for the user.

    If the 'image' field is provided in the request, the function checks if the value is a valid base64-encoded image.
    If it is, the function converts the base64 string to binary and stores the image header separately.

    If any error occurs during the process, an HTTPException is raised with an appropriate status code and error message.
    """
    measurements = (
        db.query_eng(Measurement).filter(Measurement.customer_id == user.id).first()
    )
    if measurements:
        image_urls = measurements.images or []
        print(image_urls)
        for key, value in request.model_dump(exclude_unset=True).items():
            if value not in (None, ""):
                if key == "images":
                    for index, image_base64 in enumerate(value):
                        if image_base64.startswith("data:image"):
                            try:
                                header, image_data = image_base64.split(";base64,")
                                file_extension = header.split("/")[1]
                                image_data = base64.b64decode(image_data)
                                clean_email = user.email.replace(" ", "_")
                                unique_filename = f"{clean_email + str(uuid.uuid4())[:6]}.{file_extension}"

                                s3_client.put_object(
                                    Bucket=settings.S3_BUCKET_NAME,
                                    Key=unique_filename,
                                    Body=image_data,
                                    ContentType=f"image/{file_extension}",
                                )

                                file_url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.S3_REGION}.amazonaws.com/{unique_filename}"
                                image_urls.append(file_url)
                                print("in loop after apppend")
                                print(image_urls)

                            except Exception as e:
                                raise HTTPException(
                                    status_code=400,
                                    detail=f"Failed to process image {index+1}: {str(e)}",
                                )
                    setattr(measurements, key, image_urls)
                else:
                    setattr(measurements, key, value)
        db.add(measurements)
        db.refresh(measurements)
        return measurements
    else:
        image_urls = []
        for index, image_base64 in enumerate(request.images):
            try:
                header, image_data = image_base64.split(";base64,")
                file_extension = header.split("/")[1]
                image_data = base64.b64decode(image_data)
                clean_email = user.email.replace(" ", "_")
                unique_filename = (
                    f"{clean_email + str(uuid.uuid4())[:6]}.{file_extension}"
                )

                s3_client.put_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    Key=unique_filename,
                    Body=image_data,
                    ContentType=f"image/{file_extension}",
                )

                # Construct the file URL
                file_url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.S3_REGION}.amazonaws.com/{unique_filename}"
                image_urls.append(file_url)

            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to process image {index+1}: {str(e)}",
                )
        new_measurements = Measurement(
            customer_id=user.id,
            images=image_urls,
            **request.model_dump(exclude="images"),
        )
        db.add(new_measurements)
        return new_measurements


@router.get(
    "/get_measurements",
    response_model=MeasurementSchema,
    status_code=status.HTTP_200_OK,
)
def get_measurements(
    db: Session = Depends(load), user: User = Depends(auth.get_current_user)
):
    measurement = (
        db.query_eng(Measurement).filter(Measurement.customer_id == user.id).first()
    )
    return measurement


@router.post("/add_to_cart", status_code=status.HTTP_201_CREATED)
def add_product(
    request: CreateCart,
    db: Session = Depends(load),
    user: User = Depends(auth.get_current_user),
):
    new_product = Cart(
        customer_id=user.id, product_id=request.product_id, quantity=request.quantity
    )
    db.add(new_product)
    return new_product


@router.get("/profile", response_model=ShowCustomer, status_code=status.HTTP_200_OK)
def get_profile(
    db: Session = Depends(load), user: User = Depends(auth.get_current_user)
):
    """
    Parameters:
    - db (Session): A database session object.
    - user (User): The current user object.

    Returns:
    - User: An object containing the current user's profile details.

    This function retrieves the user's profile details from the database using the provided user object.
    """
    customer = db.query_eng(Customer).filter(Customer.id == user.id).first()
    return {
        **user.__dict__,
        **customer.__dict__,
    }


@router.patch("/update_profile", status_code=status.HTTP_200_OK)
def update_profile(
    request: UpdateCustomer,
    db: Session = Depends(load),
    user: User = Depends(auth.get_current_user),
):
    customer = db.query_eng(Customer).filter(Customer.id == user.id).first()
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)

    db.add(customer)
    return {"message": "Profile updated successfully!"}


@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_customers(
    db: Session = Depends(load), user: User = Depends(auth.check_authorization("admin"))
):
    return db.query_eng(Customer).all()


@router.get("/measurement/{id}", status_code=status.HTTP_200_OK)
def get_measurement_by_id(
    id: str,
    db: Session = Depends(load),
    user: User = Depends(auth.check_authorization("admin")),
):
    measurement = (
        db.query_eng(Measurement).filter(Measurement.customer_id == id).first()
    )
    if measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement


@router.get("/cart", status_code=status.HTTP_200_OK)
def get_cart(
    db: Session = Depends(load),
    user: Optional[User] = Depends(auth.get_current_user),
):
    if user:
        cart = db.query_eng(Cart).filter(Cart.customer_id == user.id).first()
        return cart
