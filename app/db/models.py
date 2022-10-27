import uuid

from sqlalchemy import Column, Integer, Text, Boolean, FLOAT, ForeignKey, BigInteger, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.api.user import UserData
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    wallets = relationship("Wallet", backref="owner")

    def __init__(self, user: UserData, wallets):
        self.login = user.login
        self.password = user.password
        self.wallets = wallets

    def to_dict(self):
        return {"id": self.id, "login": self.login, "email": self.email}


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(BigInteger, primary_key=True)
    balance = Column(FLOAT, default=0)
    owner_id = Column(BigInteger, ForeignKey("users.id"))
