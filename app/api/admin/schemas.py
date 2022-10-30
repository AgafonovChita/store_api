from pydantic import BaseModel
from typing import List
from app.api.store.schemas import WalletSchema


class UserStatusSchema(BaseModel):
    user_id: int
    is_active: bool
    is_admin: bool = False


class UserSchema(BaseModel):
    user_id: int
    user_login: str
    is_active: bool
    is_admin: bool


class AddProductSchema(BaseModel):
    header: str
    description: str
    price: int


class EditProductSchema(BaseModel):
    product_id: int
    header: str
    description: str
    price: int


class DeleteProductSchema(BaseModel):
    product_id: int


class UserAndWalletSchema(BaseModel):
    user_id: int
    user_login: int
    wallets: List[WalletSchema]





