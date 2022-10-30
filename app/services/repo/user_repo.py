from app.services.repo.base import BaseSQLAlchemyRepo
from app.db.models import User, Wallet
from app.api.auth import UserSchema
from sqlalchemy import update, select


class UserRepo(BaseSQLAlchemyRepo):
    async def user_registration(self, user_data: UserSchema) -> User:
        wallet = Wallet(balance=100)
        user = await self._session.merge(User(user=user_data, wallets=[wallet]))
        await self._session.commit()
        return user

    async def get_user_by_login(self, login: str) -> User:
        login = await self._session.execute(select(User).where(User.login == login))
        return login.scalar()

    async def check_user_by_login(self, login: str) -> bool:
        return bool(await self.get_user_by_login(login=login))

    async def get_user_by_id(self, user_id: int) -> bool:
        return await self._session.get(User, user_id)

    async def check_user_by_id(self, user_id: int) -> bool:
        return bool(await self.get_user_by_id(user_id=user_id))

    async def activate_account(self, user_id: int) -> User:
        user = await self._session.execute(
            update(User).where(User.id == user_id).values(is_active=True)
        )
        await self._session.commit()
        return user
