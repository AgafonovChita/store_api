
from typing import List
from app.services.repo.base import BaseSQLAlchemyRepo
from app.db.models import User, Wallet, Product, Transaction
from app.api.auth import UserSchema
from sqlalchemy import update, select


class TransactionRepo(BaseSQLAlchemyRepo):
    async def payment_transaction(self, transaction_id: int, amount: int, wallet_id: int, owner_id: int):

        wallet = await self._session.execute(select(Wallet).where(Wallet.id == wallet_id))
        if wallet.scalar():
            wallet = await self._session.get(Wallet, wallet_id)
            wallet.balance = wallet.balance + amount
        else:
            await self._session.merge(Wallet(id=wallet_id, balance=amount, owner_id=owner_id))
        await self._session.merge(Transaction(id=transaction_id, amount=amount, wallet_id=wallet_id))
        await self._session.commit()

    async def buy_transaction(self, amount: int, wallet_id: int):
        await self._session.merge(Transaction(amount=amount, wallet_id=wallet_id))

