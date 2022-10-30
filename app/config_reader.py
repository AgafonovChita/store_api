from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    APP_HOST: str
    APP_PORT: int

    SECRET_KEY: str
    PRIVATE_KEY: str

    TTL_ACCESS_TOKEN: int
    TTL_REFRESH_TOKEN: int

    DEV: bool

    class Config:
        env_file = "./.env_dev"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


config = Settings()
