from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_spending_menu_kb() -> InlineKeyboardMarkup:
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(text='За выбранный месяц', callback_data='month_period'),
        InlineKeyboardButton(text='За выбранный год', callback_data='year_period'),
        InlineKeyboardButton(text='За выбранный день', callback_data='day_period'),
        InlineKeyboardButton(text='Последний расход', callback_data='lust_period')
    ]

    kb.add(*buttons)

    return kb

