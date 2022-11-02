from typing import List
from app.services.repo.base import BaseSQLAlchemyRepo
from app.db.models import User, Wallet, Product, Transaction
from app.api.auth import UserSchema
from sqlalchemy import update, select
from sqlalchemy.dialects.postgresql import insert


class TransactionRepo(BaseSQLAlchemyRepo):
    async def payment_transaction(self, transaction_id: int,
                                  amount: int, wallet_id: int, owner_id: int):
        t = Wallet.__table__
        ins = insert(t)
        upsert = ins.on_conflict_do_update(constraint=t.primary_key,
                                           set_={
                                               "balance": ins.excluded.balance + amount,
                                               "owner_id": owner_id})

        await self._session.execute(upsert, {"id": wallet_id,
                                             "balance": amount,
                                             "owner_id": owner_id})

        await self._session.merge(
            Transaction(id=transaction_id, amount=amount, wallet_id=wallet_id))

        wallet = await self._session.get(Wallet, wallet_id)
        await self._session.commit()
        return wallet


