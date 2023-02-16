from datetime import datetime
import calendar

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text, Command
from aiogram import Dispatcher

from keyboards import create_spending_menu_kb
from lexicon import RU_LEXICON
from database import create_users_db, create_wallets_db, create_descriptions_db,\
                    add_user_in_db, add_wallet_in_db, add_description_in_db, update_wallet,\
                    check_user_in_db, check_wallet_in_db, check_description_in_db,\
                    show_lust_spending, show_month_spending, show_year_spending


async def process_start_command(message: Message):
    await message.answer(RU_LEXICON['/start'])


async def process_help_command(message: Message):
    await message.answer(RU_LEXICON['/help'])


async def process_create_user_command(message: Message):
    create_users_db()
    create_wallets_db()
    create_descriptions_db()
    tg_id = message.from_user.id
    if check_user_in_db(tg_id):
        await message.answer(RU_LEXICON['already_user'])
    else:
        add_user_in_db(tg_id)
        await message.answer(RU_LEXICON['created_user'])


async def process_create_spending_command(message: Message):
    date = datetime.now()
    year = date.year
    tg_id = message.from_user.id
    if check_user_in_db(tg_id):
        if not check_wallet_in_db(tg_id):
            add_wallet_in_db(tg_id, year)
        await message.answer(RU_LEXICON['/create_spending'])
        # Добавить FMS
    else:
        await message.answer(RU_LEXICON['not_user'])
    # Добавить хэндлер на неправильное сообщение 


async def add_spending(message: Message):
    tg_id = message.from_user.id
    date = datetime.now()
    year = date.year
    if check_user_in_db(tg_id) and check_wallet_in_db(tg_id):
        month = calendar.month_name[date.month].lower()
        day = date.day
        spent_money = int(message.text.split(' ', 1)[0])
        description = message.text.split(' ', 1)[1]

        update_wallet(tg_id, year, month, spent_money)
        add_description_in_db(tg_id, year, month, day, spent_money, description)
        await message.answer(RU_LEXICON['created_spending'])
    else:
        await message.answer(RU_LEXICON['not_user_or_wallet'])
            

async def process_spending_menu_command(message: Message):
    tg_id = message.from_user.id
    if check_user_in_db(tg_id) and check_wallet_in_db(tg_id) and check_description_in_db(tg_id):
        await message.answer('За какой период вы хотите посмотреть свои расходы?', reply_markup=create_spending_menu_kb())
    else:
        await message.answer(RU_LEXICON['not_user_or_wallet'])


async def process_period_press(callback: CallbackQuery):
    tg_id = callback.from_user.id
    year = datetime.now().year
    if callback.data.startswith('lust'):
        spending = show_lust_spending(tg_id, year)
        await callback.message.edit_text(text=f'Твоя последняя запись: {spending}р', reply_markup=create_spending_menu_kb())
        await callback.answer()
    elif callback.data.startswith('year'):
        await callback.message.answer(text=RU_LEXICON['chosen_year'])
        await callback.answer()
    elif callback.data.startswith('month'):
        await callback.message.answer(text=RU_LEXICON['chosen_month'])
        await callback.answer()
    elif callback.data.startswith('day'):
        await callback.message.answer(text=RU_LEXICON['chosen_day'])
        await callback.answer()
    # Добавить FMS


async def process_total_show(message: Message):
    answer = message.text.split('.')
    tg_id = message.from_user.id
    if len(answer) == 1:
        spending = show_year_spending(tg_id, int(answer[0]))
        await message.answer(text=f'Total: {spending}р')
    elif len(answer) == 2:
        year = int(answer[1])
        month = calendar.month_name[(int(answer[0]))].lower()
        spending = show_month_spending(tg_id, year, month)
        await message.answer(text=f'Сделано записей: {spending[0]}.\nВсего затрат за месяц: {spending[1]}р.')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, Command(commands=['start']))
    dp.register_message_handler(process_help_command, Command(commands=['help']))
    dp.register_message_handler(process_create_user_command, Command(commands=['create_user']))
    dp.register_message_handler(process_create_spending_command, Command(commands=['create_spending']))
    dp.register_message_handler(add_spending, lambda message: len(message.text.split(' ')) == 2)
    dp.register_message_handler(process_spending_menu_command, Command(commands=['spending_menu']))
    dp.register_callback_query_handler(process_period_press, Text(endswith='period'))
    dp.register_message_handler(process_total_show, lambda message: message.text.split('.', 1)[0].isdigit())