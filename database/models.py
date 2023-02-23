from datetime import datetime
from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    tg_id: Mapped[int] = mapped_column(primary_key=True)

    wallets: Mapped[List["Wallet"]] = relationship(back_populates="owner")

    
    def __repr__(self) -> str:
        return f"tg_id='{self.tg_id}'"


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    create_year: Mapped[int] = mapped_column(default=datetime.now().year)
    create_month: Mapped[int] = mapped_column(default=datetime.now().month)
    create_day: Mapped[int] = mapped_column(default=datetime.now().day)
    cost: Mapped[int]
    description: Mapped[str]
    user_tg_id = mapped_column(ForeignKey("user.tg_id"))

    owner: Mapped["User"] = relationship(back_populates="wallets")


    def __repr__(self) -> str:
        return f'{self.id}, {self.create_year}-{self.create_month}-{self.create_day}, {self.cost} {self.description}'

