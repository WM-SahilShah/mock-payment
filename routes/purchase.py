import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any

# Initialize router and security
router = APIRouter()
security = HTTPBasic()

# Mock Database for users (username: password)
fake_db = {
    "test_username": "test_password"
}

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class PaymentRequest(BaseModel):
    product_price: float = Field(..., alias="productPrice")
    account_balance: float = Field(..., alias="accountBalance")

    @field_validator("product_price", "account_balance")
    def must_be_positive(cls, value) -> float:
        if value < 0:
            logger.error("Validation failed: Value must be non-negative.")
            raise ValueError("Value must be non-negative.")
        return round(value, 2)

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_password = fake_db.get(credentials.username)
    if correct_password is None or correct_password != credentials.password:
        logger.warning(f"Failed login attempt - username: {credentials.username}, password: {credentials.password}")
        raise HTTPException(
            status_code=401, detail="Invalid credentials"
        )
    logger.info(f"User '{credentials.username}' authenticated successfully.")
    return credentials.username

@router.post("/payment")
async def process_payment(payment: PaymentRequest, username: str = Depends(verify_credentials)) -> Dict[str, Any]:
    logger.info(f"Processing payment request for user '{username}': {payment.dict(by_alias=True)}")
    
    if payment.account_balance < payment.product_price:
        logger.error(f"Payment failed for user '{username}': Insufficient account balance.")
        raise HTTPException(
            status_code=400, detail="Insufficient account balance."
        )
    
    updated_balance = payment.account_balance - payment.product_price
    logger.info(f"Payment of {payment.product_price} processed successfully for user '{username}'. Updated balance: {updated_balance:.2f}")
    
    return {
        "message": f"Payment of {payment.product_price} processed successfully for {username}.",
        "updatedAccountBalance": updated_balance
    }
