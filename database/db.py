import sqlite3


def create_users_db():
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            tg_id INTEGER PRIMARY KEY
        );""")

        db.commit()
        db.close()
    except sqlite3.Error as er:
        print('Ошибка в create_users_db', er)
    finally:
        if db:
            db.close()


def create_wallets_db():
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

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
        print('Ошибка в create_wallets_db', er)
    finally:
        if db:
            db.close()


def create_descriptions_db():
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS descriptions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            month TEXT,
            day INTEGER,
            cost INTEGER,
            description TEXT,
            user_tg_id INTEGER NOT NULL,
            FOREIGN KEY (user_tg_id) REFERENCES users(tg_id)
        );""")

        db.commit()
        db.close()
    except sqlite3.Error as er:
        print('Ошибка в create_description_db:', er)
    finally:
        if db:
            db.close()
