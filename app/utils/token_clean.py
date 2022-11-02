from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text
from app.services.repo.query.raw_sql import delete_expired_tokens


async def token_clean(engine: AsyncEngine):
    async with engine.begin() as connection:
        await connection.execute(text(delete_expired_tokens))
