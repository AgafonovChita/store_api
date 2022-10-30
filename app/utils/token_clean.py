from sanic import Sanic
from app.services.repo import SQLAlchemyRepo, ServiceRepo


async def token_clean(repo: SQLAlchemyRepo):
    await repo.get_repo(ServiceRepo).clean_expire_refresh_tokens()
