from app.services.repo.base import BaseSQLAlchemyRepo
from app.db.models import User, Wallet, RefreshToken
from app.api.auth import UserData
from sqlalchemy import update, select, delete


class RefreshTokenRepo(BaseSQLAlchemyRepo):
    async def save_refresh_token(self, token: str, exp: int):
        token = await self._session.merge(RefreshToken(token=token, exp=exp))
        await self._session.commit()
        return token

    async def update_refresh_token(self, token_id: int, token: str, exp: int):
        await self._session.execute(update(RefreshToken).
                                    where(RefreshToken.id == token_id).
                                    values(token=token, exp=exp))
        await self._session.commit()

    async def get_refresh_token(self, token: str):
        token = await self._session.execute(
            select(RefreshToken).where(RefreshToken.token == token))
        return token.scalar()

    async def delete_refresh_token(self, token: str):
        await self._session.execute(delete(RefreshToken).where(RefreshToken.token == token))
        await self._session.commit()

    async def check_refresh_token(self, token: str):
        return bool(await self.get_refresh_token(token=token))
