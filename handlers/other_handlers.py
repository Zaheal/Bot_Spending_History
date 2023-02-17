from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from lexicon import RU_LEXICON


# Реагирует на любое сообщение пользователя, не запланированное функционалом бота
async def process_show_users(message: Message):
    await message.answer(text=RU_LEXICON['not_founded'])


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(process_show_users)
