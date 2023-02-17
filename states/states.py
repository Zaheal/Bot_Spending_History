from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMSpending(StatesGroup):
    waiting_spent = State()
    waiting_date = State()