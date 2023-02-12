from aiogram.types import Message
from aiogram.dispatcher.filters import Text, Command
from aiogram import Dispatcher

from lexicon import RU_LEXICON


async def process_start_command(message: Message):
    await message.answer(RU_LEXICON['/start'])


async def process_help_command(message: Message):
    await message.answer(RU_LEXICON['/help'])





def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, Command(commands=['start']))
    dp.register_message_handler(process_help_command, Command(commands=['help']))

