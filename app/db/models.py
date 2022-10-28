import uuid

from sqlalchemy import Column, Integer, Text, Boolean, FLOAT, ForeignKey, BigInteger, LargeBinary, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.api.auth import UserBody
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    wallets = relationship("Wallet", backref="owner")

    def __init__(self, user: UserBody, wallets):
        self.login = user.login
        self.password = user.password
        self.wallets = wallets

    def to_dict(self):
        return {"id": self.id, "login": self.login, "email": self.email}


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(BigInteger, primary_key=True)
    token = Column(Text, nullable=False)
    exp = Column(BigInteger, nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    header = Column(Text)
    description = Column(Text, default="NotDescription")
    price = Column(Integer, default=100)

    def to_dict(self):
        return {"id": self.id, "header": self.header, "descript": self.description, "price": self.price}


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(BigInteger, primary_key=True)
    balance = Column(Integer, default=0)
    owner_id = Column(BigInteger, ForeignKey("users.id"))
    transactions = relationship("Transaction", backref="wallet")

    def to_dict(self):
        return {"id": self.id, "balance": self.balance, "owner_id": self.owner_id}


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(BigInteger, primary_key=True)
    amount = Column(FLOAT, nullable=False)
    wallet_id = Column(BigInteger, ForeignKey("wallets.id"))

    def to_dict(self):
        return {"id": self.id, "count": self.count, "wallet_id": self.wallet_id}


