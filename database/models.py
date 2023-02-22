from datetime import datetime
from typing import List

from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, Session
import sqlalchemy as db

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    tg_id: Mapped[int] = mapped_column(primary_key=True)

    wallets: Mapped[List["Wallet"]] = relationship(back_populates="owner")
    expenses: Mapped[List["Expense"]] = relationship(back_populates="owner")

    
    def __repr__(self) -> str:
        return f"tg_id='{self.tg_id}'"


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    create_date: Mapped[datetime] = mapped_column(default=datetime.now())
    lust: Mapped[int]
    lust_desc: Mapped[str]
    january: Mapped[int] = mapped_column(default=0)
    february: Mapped[int] = mapped_column(default=0)
    march: Mapped[int] = mapped_column(default=0)
    april: Mapped[int] = mapped_column(default=0)
    may: Mapped[int] = mapped_column(default=0)
    june: Mapped[int] = mapped_column(default=0)
    july: Mapped[int] = mapped_column(default=0)
    august: Mapped[int] = mapped_column(default=0)
    september: Mapped[int] = mapped_column(default=0)
    october: Mapped[int] = mapped_column(default=0)
    november: Mapped[int] = mapped_column(default=0)
    december: Mapped[int] = mapped_column(default=0)
    user_tg_id = mapped_column(db.ForeignKey("user.tg_id"))

    owner: Mapped["User"] = relationship(back_populates="wallets")

    
    def __init__(self, lust: int, lust_desc: str, owner: User):
        self.create_date = datetime.now()
        self.lust = lust
        self.lust_desc = lust_desc
        self.owner = owner
        self.user_tg_id = owner.tg_id


    def __repr__(self) -> str:
        return f'{self.id}, {self.create_date}, {self.lust} {self.lust_desc}, owner by {self.owner}, july={self.july}, user_tg_id={self.user_tg_id}'


class Expense(Base):
    __tablename__ = 'expense'

    create_date: Mapped[datetime] = mapped_column(primary_key=True, default=datetime.now())
    cost: Mapped[int]
    description: Mapped[str]
    user_tg_id = mapped_column(db.ForeignKey("user.tg_id"))

    owner: Mapped["User"] = relationship(back_populates="expenses")


    def __init__(self, cost: int, description: str, owner: User) -> None:
        self.create_date = datetime.now()
        self.cost = cost
        self.description = description
        self.owner = owner
        self.user_tg_id = owner.tg_id


    def __repr__(self) -> str:
        return f'{self.create_date}, {self.cost} {self.description}, {self.user_tg_id}, owner by {self.owner}'
