from pydantic import BaseModel, EmailStr


class UserBody(BaseModel):
    login: str
    password: str





