from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any

router = APIRouter()
security = HTTPBasic()

# Mock Database for users (username: password)
fake_db = {
    "test_username": "test_password"
}

class PaymentRequest(BaseModel):
    product_price: float = Field(..., alias="productPrice")
    account_balance: float = Field(..., alias="accountBalance")

    @field_validator("product_price", "account_balance")
    def must_be_positive(cls, value) -> float:
        if value < 0:
            raise ValueError("Value must be non-negative.")
        return round(value, 2)

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_password = fake_db.get(credentials.username)
    if correct_password is None or correct_password != credentials.password:
        raise HTTPException(
            status_code=401, detail="Invalid credentials"
        )
    return credentials.username

@router.post("/payment")
async def process_payment(payment: PaymentRequest, username: str = Depends(verify_credentials)) -> Dict[str, Any]:
    if payment.account_balance < payment.product_price:
        raise HTTPException(
            status_code=400, detail="Insufficient account balance."
        )
    updated_balance = payment.account_balance - payment.product_price
    return {
        "message": f"Payment of {payment.product_price} processed successfully for {username}.",
        "updatedAccountBalance": updated_balance
    }
