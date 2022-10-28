from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    login: str
    password: str





