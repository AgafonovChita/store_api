from pydantic import BaseModel, EmailStr


class BuyBody(BaseModel):
    wallet_id: int
    product_id: int




