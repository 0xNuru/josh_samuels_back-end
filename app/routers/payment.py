from fastapi import APIRouter, HTTPException, status

from app.schema.payment import Payments
from app.utils.payment import accept_payments


router = APIRouter(prefix="/payment", tags=["Payment Management"])


@router.post("/initialize-transactions", status_code=status.HTTP_200_OK)
def initialize_payment(request: Payments):
    access_code = accept_payments(email=request.email, amount=request.amount)
    if access_code is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request"
        )
    return {"access_code": access_code}
