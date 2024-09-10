import asyncio
import logging
from aiogram import Dispatcher
from handlers import main_handlers, callback_handlers, state_handlers
from bot_instance import bot
from database import init_db
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config_reader import config

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

dp.include_router(main_handlers.router)
dp.include_router(callback_handlers.router)
dp.include_router(state_handlers.router)


@dp.message()
async def handle_all_messages(message: Message, state: FSMContext):
    # Обработка сообщений от всех пользователей
    if message.from_user.id in config.OPERATORS:
        # Если сообщение от оператора, обрабатываем в зависимости от состояния
        await state_handlers.handle_user_messages(message, state)
    else:
        # Если сообщение от клиента, передаем на обработку функции
        await state_handlers.process_client_message(message)


async def main():
    logging.info("Starting polling")
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
