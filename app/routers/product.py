from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.engine.load import load
from app.models.product import Product
from app.models.user import User
from app.schema.product import CreateProduct
from app.utils import auth

router = APIRouter(prefix="/product", tags=["Product Management"])


@router.post("/add_product", status_code=status.HTTP_201_CREATED)
def add_product(
    request: CreateProduct,
    db: Session = Depends(load),
    user: User = Depends(auth.check_authorization("admin")),
):
    new_product = Product(
        name=request.name,
        description=request.description,
        price=request.price,
        category=request.category,
        stock_quantity=request.stock_quantity,
        # product_image=request.product_image,
    )
    db.add(new_product)
    return new_product
