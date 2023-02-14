from datetime import datetime
from contextlib import suppress

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text, Command
from aiogram import Dispatcher
from aiogram.utils.exceptions import MessageNotModified

from keyboards import create_spending_menu_kb
from lexicon import RU_LEXICON
from database import create_sp_history_db, check_user_in_db, add_user_in_bd


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
        year = datetime.now().year
        add_user_in_bd(tg_id, year)
        await message.answer(RU_LEXICON['created_user'])


async def process_create_spending(message: Message):
    await message.answer(RU_LEXICON['/create_spending'])


# async def add_spending(message: Message):
#     if message.from_user.id in data:
#         date = datetime.now()
#         year = date.year
#         month = date.month

#         data[message.from_user.id][year][month - 1] += int(message.text)
#         await message.answer(RU_LEXICON['created_spending'])
#     else:
#         await message.answer(RU_LEXICON['not_user'])
            

# async def process_spending_menu(message: Message):
#     if message.from_user.id in data:
#         await message.answer('За какой период вы хотите посмотреть свои расходы?', reply_markup=create_spending_menu_kb())
#     else:
#         await message.answer(RU_LEXICON['not_user'])


# async def process_year_press(callback: CallbackQuery):
#     spending = sum(data[callback.from_user.id][datetime.now().year])
#     await callback.message.edit_text(text=f'Расходы в этом году: {spending}', reply_markup=create_spending_menu_kb())
#     await callback.answer()


# async def process_month_press(callback: CallbackQuery):
#     spending = data[callback.from_user.id][datetime.now().year][datetime.now().month - 1]
#     await callback.message.edit_text(text=f'Расходы в этом месяце: {spending}', reply_markup=create_spending_menu_kb())
#     await callback.answer()


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, Command(commands=['start']))
    dp.register_message_handler(process_help_command, Command(commands=['help']))
    dp.register_message_handler(process_create_user_command, Command(commands=['create_user']))
    dp.register_message_handler(process_create_spending, Command(commands=['create_spending']))
    # dp.register_message_handler(add_spending, lambda message: message.text.isdigit())
    # dp.register_message_handler(process_spending_menu, Command(commands=['spending_menu']))
    # dp.register_callback_query_handler(process_year_press, Text(equals='year'))
    # dp.register_callback_query_handler(process_month_press, Text(equals='month'))
    