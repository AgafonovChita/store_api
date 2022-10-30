from app.services.repo.base import BaseSQLAlchemyRepo
from app.services.repo.query import raw_sql


class ServiceRepo(BaseSQLAlchemyRepo):
    async def clean_expire_refresh_tokens(self):
        users = await self._session.execute(raw_sql.delete_expired_tokens)
        await self._session.commit()
