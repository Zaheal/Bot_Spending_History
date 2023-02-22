from models import *



engine = db.create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=engine)


u1 = User(tg_id=8988)
ex1 = Expense(cost=100, description='lulia', owner=u1)
ex2 = Expense(cost=200, description='kebab', owner=u1)
w1 = Wallet(lust=231, lust_desc='lulia', owner=u1)
print(w1)