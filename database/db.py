import sqlite3


def create_sp_history_db():
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            tg_id INTEGER PRIMARY KEY
        );""")

        db.commit()

        cur.execute("""CREATE TABLE IF NOT EXISTS wallets(
            year INTEGER PRIMARY KEY,
            lust INTEGER DEFAULT 0,
            january INTEGER DEFAULT 0,
            february INTEGER DEFAULT 0,
            march INTEGER DEFAULT 0,
            april INTEGER DEFAULT 0,
            may INTEGER DEFAULT 0,
            june INTEGER DEFAULT 0,
            july INTEGER DEFAULT 0,
            august INTEGER DEFAULT 0,
            september INTEGER DEFAULT 0,
            october INTEGER DEFAULT 0,
            november INTEGER DEFAULT 0,
            december INTEGER DEFAULT 0,
            user_tg_id INTEGER NOT NULL,
            FOREIGN KEY (user_tg_id) REFERENCES users(tg_id)
        );""")

        db.commit()

        db.close()
    except sqlite3.Error as er:
        print('Ошибка в create_sp_history_db', er)
    finally:
        if db:
            db.close()


def check_user_in_db(tg_id: int) -> bool:
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute("SELECT tg_id FROM users WHERE tg_id=?", (tg_id, ))
        if cur.fetchone() is None:
            db.close()
            return False
        else:
            db.close()
            return True
        
    except sqlite3.Error as er:
        print('Ошибка в check_user_in_db', er)
    finally:
        if db:
            db.close()


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

        cur.execute("SELECT lust FROM wallets WHERE user_tg_id=? AND year=?", (tg_id, year))
        if cur.fetchone() is None:    
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

        cur.execute(f"UPDATE wallets SET {month}=?, lust=? WHERE user_tg_id=? AND year=?", (spent_money, spent_money, tg_id, year))

        db.commit()
        db.close()
    except sqlite3.Error as er:
        print('Ошибка в update_wallet', er)
    finally:
        if db:
            db.close()
