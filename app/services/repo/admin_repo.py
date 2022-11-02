from typing import List
from app.services.repo.base import BaseSQLAlchemyRepo
from app.db.models import User, Wallet, Product, Transaction
from app.api.auth import UserSchema
from sqlalchemy import update, select, delete
from sqlalchemy.orm import joinedload
from app.services.repo.query import raw_sql


class AdminRepo(BaseSQLAlchemyRepo):
    async def get_users_and_wallets(self):
        users = await self._session.execute(raw_sql.users_and_wallets_sql)
        await self._session.commit()
        return users.all()

    async def get_users(self):
        users = await self._session.execute(
            select([User.id, User.login, User.is_active, User.is_admin])
        )
        await self._session.commit()
        return users.all()

    async def get_user_by_id(self, user_id: int):
        user = await self._session.get(User, user_id)
        await self._session.commit()
        return user

    async def change_user_status(
            self, user_id: int, is_active: bool, is_admin: bool = False
    ):
        await self._session.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_active=is_active, is_admin=is_admin)
        )
        await self._session.commit()

    async def add_new_product(self, header: str, description: str, price: int):
        product = await self._session.merge(
            Product(header=header, description=description, price=price)
        )
        await self._session.commit()
        return product

    async def edit_product(self, product_id: int, header: str, description: str, price: int):
        product = await self._session.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(header=header, description=description, price=price)
            .returning(Product)
        )
        await self._session.commit()
        return product.fetchone()

    async def delete_product(self, product_id: int):
        product = await self._session.execute(delete(Product)
                                              .where(Product.id == product_id)
                                              .returning(Product))
        await self._session.commit()
        return product.fetchone()

    async def get_product_by_id(self, product_id: int) -> Product:
        return await self._session.get(Product, product_id)

    async def check_product_by_id(self, product_id: int) -> bool:
        return bool(await self.get_product_by_id(product_id=product_id))
