from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_spending_menu_kb() -> InlineKeyboardMarkup:
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup()

    buttons = [
        InlineKeyboardButton(text='В этом месяце', callback_data='month_period'),
        InlineKeyboardButton(text='В этом году', callback_data='year_period'),
        InlineKeyboardButton(text='Последний расход', callback_data='lust_period')
    ]

    kb.add(*buttons)

    return kb

