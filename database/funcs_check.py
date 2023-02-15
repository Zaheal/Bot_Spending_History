import sqlite3


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


def check_wallet_in_db(tg_id: int, year: int) -> bool:
    try:
        db = sqlite3.connect(r"database/spending_history.db")
        cur = db.cursor()

        cur.execute("SELECT lust FROM wallets WHERE user_tg_id=? AND year=?", (tg_id, year))
        if cur.fetchone() is None:    
            db.close()
            return False
        else:
            db.close()
            return True

    except sqlite3.Error as er:
        print('Ошибка в check_wallet_in_db', er)
    finally:
        if db:
            db.close()