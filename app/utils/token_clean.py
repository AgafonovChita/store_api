from sanic import Sanic
from app.services.repo import SQLAlchemyRepo, ServiceRepo
from sqlalchemy.ext.asyncio import AsyncEngine
from app.services.repo.query.raw_sql import delete_expired_tokens


async def token_clean(engine: AsyncEngine):
    with engine.begin() as connection:
        connection.execute(delete_expired_tokens)

