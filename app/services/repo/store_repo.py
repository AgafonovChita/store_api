
from typing import List
from app.services.repo.base import BaseSQLAlchemyRepo
from app.db.models import User, Wallet, Product
from app.api.auth import UserData
from sqlalchemy import update, select


class StoreRepo(BaseSQLAlchemyRepo):
    async def get_products(self) -> List[Product]:
        products = await self._session.execute(select(Product))
        await self._session.commit()
        return products.scalars()

    async def get_wallets(self, user_id) -> List[Wallet]:
        wallets = await self._session.execute(select(Wallet).where(Wallet.owner_id == user_id))
        await self._session.commit()
        return wallets.scalars()
