import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from configs import load_config, Config
from handlers import register_user_handlers, register_other_handlers


logger = logging.getLogger(__name__)


def register_all_handlers(dp: Dispatcher):
    register_user_handlers(dp)
    register_other_handlers(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Starting bot')

    config: Config = load_config('.env')

    bot: Bot = Bot(config.token)
    dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())

    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')
