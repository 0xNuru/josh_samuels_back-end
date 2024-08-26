import base64
from typing import List
import uuid

import boto3
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config.config import settings
from app.engine.load import load
from app.models.product import Product
from app.models.user import User
from app.schema.product import CreateFabric, CreateProduct
from app.utils import auth


router = APIRouter(prefix="/product", tags=["Product Management"])

s3_client = boto3.client(
    "s3",
    region_name=settings.S3_REGION,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
)


@router.post("/add_product", status_code=status.HTTP_201_CREATED)
def add_product(
    request: CreateProduct,
    db: Session = Depends(load),
    user: User = Depends(auth.check_authorization("admin")),
):
    """
    Adds a new product to the database, including uploading associated images to S3.
    are provided in the request body.
    The images are provided as a list of base64 encoded strings, which are decoded and uploaded
    to AWS S3. The resulting image URLs are then stored in the database along with the product details.

    Args:
        request (CreateProduct): A Pydantic model that includes the following fields:
            - name (str): The name of the product.
            - price (float): The price of the product.
            - description (str): A description of the product.
            - category (str): The category to which the product belongs.
            - images (List[str]): A list of base64 encoded images.

        db (Session): SQLAlchemy database session used for querying and committing changes.
        user (User): The authenticated user making the request, which must have 'admin' privileges.

    Raises:
        HTTPException: If an error occurs while processing any of the images, a 400 error is raised with details.

    Returns:
        Product:
    """
    image_urls = []

    for index, image_base64 in enumerate(request.images):
        try:
            header, image_data = image_base64.split(";base64,")
            file_extension = header.split("/")[1]
            image_data = base64.b64decode(image_data)
            clean_name = request.name.replace(" ", "_")
            clean_category = request.category.replace(" ", "_")
            unique_filename = f"{clean_name + clean_category + str(uuid.uuid4())[:6]}.{file_extension}"

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
                status_code=400, detail=f"Failed to process image {index+1}: {str(e)}"
            )

    new_product = Product(
        name=request.name,
        description=request.description,
        price=request.price,
        category=request.category,
        images=image_urls,
    )
    db.add(new_product)
    return new_product


@router.get("/get_products")
def get_products(db: Session = Depends(load)):
    """
    Retrieves all products from the database.

    Args:
        db (Session): SQLAlchemy database session used for querying.

    Returns:
        List[Product]: A list of all products in the database.
    """
    return db.query_eng(Product).all()


@router.post("/add_fabric", status_code=status.HTTP_201_CREATED)
def add_fabric(
    request: CreateFabric,
    db: Session = Depends(load),
    user: User = Depends(auth.check_authorization("admin")),
):
    """
    Adds a new fabric to the database, including uploading associated images to S3.
    are provided in the request body.
    The images are provided as a list of base64 encoded strings, which are decoded and uploaded
    to AWS S3. The resulting image URLs are then stored in the database along with the product details.

    Args:
        request (CreateFabric): A Pydantic model that includes the following fields:
            - name (str): The name of the fabric.
            - price (float): The price of the fabric.
            - category (str): The category to which the fabric belongs.
            - images (List[str]): A list of base64 encoded images.

        db (Session): SQLAlchemy database session used for querying and committing changes.
        user (User): The authenticated user making the request, which must have 'admin' privileges.

    Raises:
        HTTPException: If an error occurs while processing any of the images, a 400 error is raised with details.

    Returns:
        Fabric:
    """
    image_urls = []

    for index, image_base64 in enumerate(request.images):
        try:
            header, image_data = image_base64.split(";base64,")
            file_extension = header.split("/")[1]
            image_data = base64.b64decode(image_data)
            clean_name = request.name.replace(" ", "_")
            clean_category = request.category.replace(" ", "_")
            unique_filename = f"{clean_name + clean_category + str(uuid.uuid4())[:6]}.{file_extension}"

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
                status_code=400, detail=f"Failed to process image {index+1}: {str(e)}"
            )

    new_fabric = Product(
        name=request.name,
        price=request.price,
        category=request.category,
        images=image_urls,
    )
    db.add(new_fabric)
    return new_fabric
