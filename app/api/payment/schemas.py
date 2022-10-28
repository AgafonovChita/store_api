from pydantic import BaseModel, EmailStr


class PaymentBody(BaseModel):
    signature: str
    transaction_id: int
    user_id: int
    bill_id: int
    amount: int

