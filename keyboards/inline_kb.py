from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_spending_menu_kb() -> InlineKeyboardMarkup:
    kb: InlineKeyboardMarkup = InlineKeyboardMarkup()

    buttons = [
        InlineKeyboardButton(text='В этом месяце', callback_data='month'),
        InlineKeyboardButton(text='В этом году', callback_data='year')
    ]

    kb.add(*buttons)

    return kb

