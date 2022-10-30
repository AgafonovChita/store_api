from pydantic import BaseModel, EmailStr


class BuyBody(BaseModel):
    wallet_id: int
    product_id: int


class ProductSchema(BaseModel):
    product_id: int
    header: str
    description: str
    price: str


class WalletSchema(BaseModel):
    wallet_id: int
    wallet_balance: int
