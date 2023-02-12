from datetime import datetime

from aiogram.types import Message
from aiogram.dispatcher.filters import Text, Command
from aiogram import Dispatcher

from lexicon import RU_LEXICON
from database import data


async def process_start_command(message: Message):
    await message.answer(RU_LEXICON['/start'])


async def process_help_command(message: Message):
    await message.answer(RU_LEXICON['/help'])


async def process_create_user_command(message: Message):
    if message.from_user.id in data:
        await message.answer(RU_LEXICON['already_user'])
    else:
        data[message.from_user.id] = {datetime.now().year: []}
        await message.answer(RU_LEXICON['created_user'])










def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, Command(commands=['start']))
    dp.register_message_handler(process_help_command, Command(commands=['help']))
    dp.register_message_handler(process_create_user_command, Command(commands=['create_user']))
