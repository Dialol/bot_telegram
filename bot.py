import asyncio
from logger_setup import logger
from aiogram import Dispatcher
from handlers import main_handlers, callback_handlers, state_handlers
from bot_instance import bot
from database import init_db

dp = Dispatcher()

dp.include_router(main_handlers.router)
dp.include_router(callback_handlers.router)
dp.include_router(state_handlers.router)


async def main():
    logger.info("Starting polling")
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
