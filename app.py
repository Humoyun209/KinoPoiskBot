from environs import Env
import logging

from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as admin_router

import asyncio
from aiogram import Dispatcher, Bot


env = Env()
env.read_env()


async def main():
    dp: Dispatcher = Dispatcher()
    bot: Bot = Bot(token=env.str('TOKEN'))
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s - [%(asctime)s] - %(name)s - %(message)s')

    dp.include_router(router=user_router)
    dp.include_router(router=admin_router)

    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())