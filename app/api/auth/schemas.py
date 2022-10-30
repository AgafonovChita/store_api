from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str





