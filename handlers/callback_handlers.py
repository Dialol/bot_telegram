from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from config_reader import config
from handlers.state_handlers import (ask_for_user_name,
                                     request_passport,
                                     request_passport2,
                                     request_passport3)


router = Router()


@router.callback_query(lambda c: c.data in
                       {'enter_client_id', 'request_passport',
                        'request_passport2', 'request_passport3',
                        'add_info'})
async def handle_buttons(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id in config.OPERATORS:
        data = callback.data
        if data == 'enter_client_id':
            await ask_for_user_name(callback.message, state)
        elif data == 'request_passport':
            await request_passport(callback.message)
        elif data == 'request_passport2':
            await request_passport2(callback.message)
        elif data == 'request_passport3':
            await request_passport3(callback.message)
        elif data == 'add_info':
            await ask_for_user_name(callback.message, state)
