from pydantic import BaseModel


class UserStatusBody(BaseModel):
    user_id: int
    is_active: bool
    is_admin: bool = False


class AddProductBody(BaseModel):
    header: str
    description: str
    price: int


class EditProductBody(BaseModel):
    product_id: int
    header: str
    description: str
    price: int


class DeleteProductBody(BaseModel):
    product_id: int



