from pydantic import BaseModel, EmailStr


class BuyData(BaseModel):
    wallet_id: str
    product_id: str




