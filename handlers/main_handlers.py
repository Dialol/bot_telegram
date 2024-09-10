from aiogram import types, Router
from aiogram.filters.command import Command
from config_reader import config
from handlers.state_handlers import get_main_menu_keyboard
import logging

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logging.info(f"Start command received from {message.from_user.id}")
    if message.from_user.id in config.OPERATORS:
        await message.answer(
            "Привет оператор! Нажмите кнопку, чтобы продолжить.",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await message.answer("Привет, пользователь!")
