from pydantic import BaseModel, EmailStr
from pydantic import Field


class PaymentSchema(BaseModel):
    signature: str
    transaction_id: int
    user_id: int
    bill_id: int
    amount: int

