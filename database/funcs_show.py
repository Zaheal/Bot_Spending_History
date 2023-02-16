import sqlite3
import calendar


def show_lust_spending(tg_id: int, year: int) -> int:
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        result = cur.execute("SELECT lust FROM wallets WHERE user_tg_id=? AND year=?", (tg_id, year)).fetchone()

        return result[0]
    except sqlite3.Error as er:
        print('Ошибка в show_lust_spending', er)
    finally:
        if db:
            db.close()


def show_month_spending(tg_id: int, year: int, month: str) -> tuple:
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        total: int = cur.execute(f"SELECT {month} FROM wallets WHERE user_tg_id=? AND year=?", (tg_id, year)).fetchone()[0]
        cost_with_desc: int = len(cur.execute("SELECT cost, description FROM descriptions WHERE year=? AND month=? AND user_tg_id=?", (year, month, tg_id)).fetchall())

        return cost_with_desc, total
    except sqlite3.Error as er:
        print('Ошибка в show_month_spending', er)
    finally:
        if db:
            db.close()


def show_year_spending(tg_id: int, year: int) -> int:
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        month_list: list = [month.lower() for month in calendar.month_name[1:]]
        result: int = 0
        for month in month_list:
            result += cur.execute(f"SELECT {month} FROM wallets WHERE user_tg_id=? AND year=?", (tg_id, year)).fetchone()[0]

        return result
    except sqlite3.Error as er:
        print('Ошибка в show_month_spending', er)
    finally:
        if db:
            db.close()


def show_day_spending(tg_id: int, year: int, month: str, day: int) -> tuple:
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cost_with_desc = cur.execute("SELECT cost, description FROM descriptions WHERE year=? AND month=? AND day=? AND user_tg_id=?", (year, month, day, tg_id)).fetchall()

        return cost_with_desc
    except sqlite3.Error as er:
        print('Ошибка в show_day_spending', er)
    finally:
        if db:
            db.close()
