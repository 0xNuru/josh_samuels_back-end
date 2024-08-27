import base64
from typing import List
import uuid

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import joinedload, Session

from app.config.config import settings
from app.engine.load import load
from app.models.fabric import Fabric
from app.models.fabric_price import FabricPrice
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.user import User
from app.schema.product import (
    ProductCategorySchema,
    ProductSchema,
    FabricPriceData,
    FabricSchema,
)
from app.utils import auth


router = APIRouter(prefix="/product", tags=["Product Management"])

s3_client = boto3.client(
    "s3",
    region_name=settings.S3_REGION,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
)


@router.post("/add_category", status_code=status.HTTP_201_CREATED)
def add_category(
    request: ProductCategorySchema,
    db: Session = Depends(load),
    user: User = Depends(auth.check_authorization("admin")),
):
    """
    Adds a new product category to the database.

    Args:
        request (ProductCategorySchema): A Pydantic model that includes the following field:
            - name (str): The name of the product category.

        db (Session): SQLAlchemy database session used for querying and committing changes.
        user (User): The authenticated user making the request, which must have 'admin' privileges.

    Returns:
        ProductCategory: The newly created product category.
    """
    new_category = ProductCategory(name=request.name)
    db.add(new_category)
    return new_category


@router.post("/add_product", status_code=status.HTTP_201_CREATED)
def add_product(
    request: ProductSchema,
    db: Session = Depends(load),
    user: User = Depends(auth.check_authorization("admin")),
):
    """
    Adds a new product to the database, including uploading associated images to S3.
    are provided in the request body.
    The images are provided as a list of base64 encoded strings, which are decoded and uploaded
    to AWS S3. The resulting image URLs are then stored in the database along with the product details.

    Args:
        request (ProductSchema): A Pydantic model that includes the following fields:
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
            clean_category = request.category_id.replace(" ", "_")
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
    product_category = (
        db.query_eng(ProductCategory)
        .filter(ProductCategory.id == request.category_id)
        .first()
    )
    if not product_category:
        raise HTTPException(
            status_code=400, detail=f"Category '{request.category_id}' does not exist."
        )

    new_product = Product(
        name=request.name,
        description=request.description,
        price=request.price,
        category_id=product_category.id,
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


@router.get("/get_product/{id}")
def get_product(
    id: str,
    db: Session = Depends(load),
):
    return db.query_eng(Product).filter(Product.id == id).first()


@router.post("/add_fabric", status_code=status.HTTP_201_CREATED)
def add_fabric(
    request: FabricSchema,
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

    new_fabric = Fabric(name=request.name, category=request.category, images=image_urls)
    db.add(new_fabric)

    for price_data in request.prices:
        fabric_price = FabricPrice(
            fabric_id=new_fabric.id,
            product_category_id=price_data.product_category,
            price=price_data.price,
        )
        db.add(fabric_price)

    return new_fabric


@router.get(
    "/fabrics", response_model=List[FabricSchema], status_code=status.HTTP_200_OK
)
def get_fabrics(db: Session = Depends(load)):
    fabrics = (
        db.query_eng(Fabric)
        .options(joinedload(Fabric.prices).joinedload(FabricPrice.product_category))
        .all()
    )
    print(fabrics)
    if not fabrics:
        raise HTTPException(status_code=404, detail="No fabrics found")

    fabric_list = []
    for fabric in fabrics:
        prices = [
            FabricPriceData(
                product_category=price.product_category_id, price=price.price
            )
            for price in fabric.prices
        ]

        fabric_data = FabricSchema(
            name=fabric.name,
            category=fabric.category,
            prices=prices,
            images=fabric.images,
        )
        fabric_list.append(fabric_data)

    return fabric_list


@router.post("/upload_image", status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    file_name: str = Form(...),
    user: User = Depends(auth.check_authorization("admin")),
):
    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{file_name}_{str(uuid.uuid4())[:6]}.{file_extension}"

        s3_client.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=unique_filename,
            Body=file.file,
            ContentType=file.content_type,
        )

        file_url = f"https://{settings.S3_BUCKET_NAME}.s3.{settings.S3_REGION}.amazonaws.com/{unique_filename}"

        return {"url": file_url}

    except NoCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AWS credentials not found.",
        )
    except PartialCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Incomplete AWS credentials.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while uploading the image: {str(e)}",
        )
