from pydantic import BaseModel


class UserBody(BaseModel):
    login: str
    password: str





