import sqlite3


def add_user_in_db(tg_id: int):
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute("INSERT INTO users VALUES (?)", (tg_id, ))

        db.commit()
        db.close()
    except sqlite3.Error as er:
        print('Ошибка в add_user_in_db', er)
    finally:
        if db:
            db.close()


def add_wallet_in_db(tg_id: int, year: int):
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute("INSERT INTO wallets (year, user_tg_id) VALUES (?, ?)", (year, tg_id))

        db.commit()
        db.close()
    except sqlite3.Error as er:
        print('Ошибка в add_wallet_in_db', er)
    finally:
        if db:
            db.close()


def update_wallet(tg_id: int, year: int, month: str, spent_money: int):
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute(f"UPDATE wallets SET {month}={month}+?, lust=? WHERE user_tg_id=? AND year=?", (spent_money, spent_money, tg_id, year))

        db.commit()
        db.close()
    except sqlite3.Error as er:
        print('Ошибка в update_wallet', er)
    finally:
        if db:
            db.close()
