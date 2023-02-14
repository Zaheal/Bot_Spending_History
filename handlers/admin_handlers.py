# from aiogram import Dispatcher
# from aiogram.types import Message
# from aiogram.dispatcher.filters import Command, Text

# from database import data
# from configs import load_config, Config


# config: Config = load_config('.env')


# async def process_show_users(message: Message):
#     await message.answer(data)








# def register_admin_handlers(dp: Dispatcher):
#     dp.register_message_handler(process_show_users, Command(commands=['show']), lambda messege: messege.from_user.id == int(config.admins))
