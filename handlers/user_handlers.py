from datetime import datetime
import calendar

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command
from aiogram import Dispatcher

from keyboards import create_spending_menu_kb
from lexicon import RU_LEXICON
from database import create_sp_history_db, check_user_in_db, add_user_in_db, add_wallet_in_db, update_wallet,\
                    check_wallet_in_db, show_lust_spending, show_month_spending, show_year_spending


async def process_start_command(message: Message):
    await message.answer(RU_LEXICON['/start'])


async def process_help_command(message: Message):
    await message.answer(RU_LEXICON['/help'])


async def process_create_user_command(message: Message):
    create_sp_history_db()
    tg_id = message.from_user.id
    if check_user_in_db(tg_id):
        await message.answer(RU_LEXICON['already_user'])
    else:
        add_user_in_db(tg_id)
        await message.answer(RU_LEXICON['created_user'])


async def process_create_spending_command(message: Message):
    year = datetime.now().year
    tg_id = message.from_user.id
    if not check_wallet_in_db(tg_id=tg_id, year=year):
        add_wallet_in_db(tg_id, year)
    await message.answer(RU_LEXICON['/create_spending'])
    # добавить FMS


async def add_spending(message: Message):
    tg_id = message.from_user.id
    date = datetime.now()
    year = date.year
    if check_user_in_db(tg_id) and check_wallet_in_db(tg_id, year):
        month = calendar.month_name[date.month].lower()
        spent_money = int(message.text.split(' ', 1))

        update_wallet(tg_id, year, month, spent_money)
        await message.answer(RU_LEXICON['created_spending']) # Обнови lexicon
    else:
        await message.answer(RU_LEXICON['not_user'])
            

async def process_spending_menu_command(message: Message):
    if check_user_in_db(tg_id=message.from_user.id) and check_wallet_in_db(tg_id=message.from_user.id, year=datetime.now().year):
        await message.answer('За какой период вы хотите посмотреть свои расходы?', reply_markup=create_spending_menu_kb())
    else:
        await message.answer(RU_LEXICON['not_user_or_wallet'])


async def process_period_press(callback: CallbackQuery):
    tg_id = callback.from_user.id
    date = datetime.now()
    year = date.year
    if callback.data.startswith('lust'):
        spending = show_lust_spending(tg_id, year)
        await callback.message.edit_text(text=f'Твоя последняя запись: {spending}р', reply_markup=create_spending_menu_kb())
        await callback.answer()
    elif callback.data.startswith('month'):
        month = calendar.month_name[date.month].lower()
        spending = show_month_spending(tg_id, year, month)
        await callback.message.edit_text(text=f'Потрачено за этот месяц: {spending}р', reply_markup=create_spending_menu_kb())
        await callback.answer()
    else:
        spending = show_year_spending(tg_id, year)
        await callback.message.edit_text(text=f'Потрачено за этот год: {spending}р', reply_markup=create_spending_menu_kb())
        await callback.answer()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, Command(commands=['start']))
    dp.register_message_handler(process_help_command, Command(commands=['help']))
    dp.register_message_handler(process_create_user_command, Command(commands=['create_user']))
    dp.register_message_handler(process_create_spending_command, Command(commands=['create_spending']))
    dp.register_message_handler(add_spending, lambda message: message.text.isdigit())
    dp.register_message_handler(process_spending_menu_command, Command(commands=['spending_menu']))
    dp.register_callback_query_handler(process_period_press, Text(endswith='period'))
    