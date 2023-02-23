from .db import *
from sqlalchemy import select

def create_user(tg_id: int) -> bool | None:
    try:
        user = User(tg_id=tg_id)
        session.add(user)
        session.commit()
    except Exception as er:
        print('Ошибка в create_user:', er)


def create_wallet(cost: int, description: str, user_tg_id: int) -> bool | None:
    try:
        wallet = Wallet(cost=cost, description=description, user_tg_id=user_tg_id)
        session.add(wallet)
        session.commit()
    except Exception as er:
        print('Ошибка в create_wallet:', er)


def show_year_expense(year: int, user_tg_id: int) -> tuple[int]:
    try:
        costs = session.execute(select(Wallet.cost).where(Wallet.create_year == year).where(Wallet.user_tg_id == user_tg_id)).all()
        expense = 0
        amount = len(costs)
        for cost in costs:
            expense += cost[0]
        return (amount, expense)
    except Exception as er:
        print('Ошибка в show_year_expense:', er)


def show_month_expense(year: int, month: int, user_tg_id: int) -> tuple[int]:
    try:
        costs = session.execute(select(Wallet.cost).where(Wallet.create_year == year).where(Wallet.create_month == month).where(Wallet.user_tg_id == user_tg_id)).all()
        expense = 0
        amount = len(costs)
        for cost in costs:
            expense += cost[0]
        return (amount, expense)
    except Exception as er:
        print('Ошибка в show_month_expense:', er)


def show_day_expense(year: int, month: int, day: int, user_tg_id: int) -> str:
    try:
        cost_desc = session.execute(select(Wallet.cost, Wallet.description).where(Wallet.create_year == year).where(Wallet.create_month == month).where(Wallet.create_day == day).where(Wallet.user_tg_id == user_tg_id)).all()
        string = ''
        for cost, desc in cost_desc:
            string += str(cost) + ' ' + desc + '\n'
        return string
    except Exception as er:
        print('Ошибка в show_day_expense:', er)


def show_lust_expense(user_tg_id: int):
    try:
        result = session.execute(select(Wallet.cost, Wallet.description).order_by(Wallet.id.desc())).first()
        return result
    except Exception as er:
        print('Ошибка в show_lust_expense:', er)


def check_user_in_db(tg_id: int) -> bool:
    try:
        stmt = select(User).where(User.tg_id == tg_id)
        if session.scalar(stmt):
            return True
        else:
            return False
    except Exception as er:
        print('Ошибка в check_user_in_db:', er)


def check_wallet_in_db(user_tg_id: int) -> bool:
    try:
        stmt = select(Wallet).where(Wallet.user_tg_id == user_tg_id)
        if session.scalar(stmt):
            return True
        else:
            return False
    except Exception as er:
        print('Ошибка в check_wallet_in_db:', er) 