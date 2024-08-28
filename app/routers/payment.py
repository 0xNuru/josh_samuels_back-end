import hashlib
import hmac
import json

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.engine.load import load
from app.config.config import settings
from app.models.product import Product
from app.models.cart import Cart
from app.schema.payment import Order_id
from app.utils.payment import accept_payments


router = APIRouter(prefix="/payment", tags=["Payment Management"])


@router.post("/initialize-transactions", status_code=status.HTTP_200_OK)
def initialize_payment(request: Order_id, db: Session = Depends(load)):
    order = db.query_eng(Cart).filter(Cart.id == request).first()
    product = db.query_eng(Product).filter(Product.id == order.product_id).first()
    access_code = accept_payments(
        email=order.email, order_id=order.id, amount=product.price
    )
    if access_code is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request"
        )
    return {"access_code": access_code}


@router.post("/paystack_webhook")
async def paystack_webhook(request: Request, db: Session = Depends(load)):
    try:
        payload = await request.body()

        paystack_signature = request.headers.get("x-paystack-signature")
        if not paystack_signature:
            raise HTTPException(status_code=400, detail="Missing Paystack signature")

        # Generate our signature using HMAC and compare with Paystack's signature
        calculated_signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode("utf-8"), payload, hashlib.sha512
        ).hexdigest()

        if not hmac.compare_digest(calculated_signature, paystack_signature):
            raise HTTPException(status_code=400, detail="Invalid Paystack signature")

        # Parse the payload into JSON
        payload_data = json.loads(payload)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")

    event = payload_data.get("event")
    data = payload_data.get("data")

    if event == "charge.success":
        reference = data.get("reference")
        try:
            # Find the order based on the unique reference number
            order = db.query_eng(Cart).filter(Cart.id == reference).first()

            if not order:
                raise HTTPException(status_code=404, detail="Order not found.")

            # Update order status and other details
            order.status = "paid"
            order.paid_at = data.get("paid_at")
            order.amount_paid = data.get("amount")

            db.add(order)

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error updating order: {str(e)}"
            )

    return {"status": "success"}
