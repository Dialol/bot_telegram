from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import save_client_data_to_db
from config_reader import config
from logger_setup import logger
from bot_instance import bot

current_user_id = None
router = Router()


class ClientInfoForm(StatesGroup):
    name = State()
    city = State()
    birthdate = State()


class ClientState(StatesGroup):
    waiting_for_reply = State()


@router.message()
async def handle_user_messages(message: types.Message, state: FSMContext):
    attempts = await state.get_data()
    attempt_count = attempts.get("attempt_count", 0)
    if message.from_user.id in config.OPERATORS:
        global current_user_id
        logger.info(f"message from {message.from_user.id}: {message.text}")

        if current_user_id is not None:
            await collect_client_information(message, state)
        elif current_user_id is None:
            try:
                user_id = int(message.text)
                current_user_id = user_id
                await message.answer(f'ID пользователя {user_id} сохранен.',
                                     reply_markup=get_main_menu_keyboard())
                logger.info(f"User ID {user_id} saved")
            except ValueError:
                await message.answer(
                    "Пожалуйста, введите корректный ID (число).")
    else:
        if attempt_count < 1:
            if message.text:
                for operator_id in config.OPERATORS:
                    await bot.send_message(
                        operator_id, f"Ответ от клиента: {message.text}")
            elif message.document:
                if message.document.mime_type == "application/pdf":
                    for operator_id in config.OPERATORS:
                        await bot.send_document(
                            operator_id, message.document.file_id)
                else:
                    await message.answer("Допустимы только PDF файлы.")
            elif message.photo:
                for operator_id in config.OPERATORS:
                    await bot.send_photo(
                        operator_id, message.photo[-1].file_id)
            else:
                await message.answer(
                    "Разрешены только файлы формата JPEG и PDF.")
            await state.update_data(attempt_count=attempt_count + 1)
            await message.answer("Ваше сообщение отправлено оператору.")
        else:
            await message.answer(
                "Вы уже отправили ответ, больше сообщений отправить нельзя.")


async def ask_for_user_name(message: types.Message, state: FSMContext):
    global current_user_id
    if current_user_id is not None:
        await message.answer('Введите имя пользователя:')
        await state.set_state(ClientInfoForm.name)
    else:
        await message.answer("ID клиента не установлен.")


async def request_passport(message: types.Message, state: FSMContext):
    global current_user_id
    if current_user_id is not None:
        try:
            await bot.send_message(
                current_user_id,
                "Добрый день. Отправьте фотографию паспорта (.jpg или .png)")
            await state.set_state(ClientState.waiting_for_reply)
            await state.update_data(attempt_count=0)
            await message.answer("Сообщение отправлено клиенту.")
        except Exception as e:
            await message.answer("Произошла ошибка при отправке сообщения.")
            print(e)
    else:
        await message.answer("ID клиента не установлен.")


async def request_passport2(message: types.Message):
    global current_user_id
    if current_user_id is not None:
        try:
            await bot.send_message(
                current_user_id,
                "Добрый день. Отправьте фотографию паспорта (.jpg или .png)")
            await message.answer("Сообщение отправлено клиенту.")
        except Exception as e:
            await message.answer("Произошла ошибка при отправке сообщения.")
            print(e)
    else:
        await message.answer("ID клиента не установлен.")


async def request_passport3(message: types.Message):
    global current_user_id
    if current_user_id is not None:
        try:
            await bot.send_message(
                current_user_id,
                "Добрый день. Отправьте фотографию паспорта (.jpg или .png)")
            await message.answer("Сообщение отправлено клиенту.")
        except Exception as e:
            await message.answer("Произошла ошибка при отправке сообщения.")
            print(e)
    else:
        await message.answer("ID клиента не установлен.")


async def collect_client_information(message: types.Message,
                                     state: FSMContext):
    state_name = await state.get_state()

    if state_name is None:
        await message.answer("Введите полное ФИО:")
        await state.set_state(ClientInfoForm.name)
    elif state_name == ClientInfoForm.name:
        await state.update_data(name=message.text)
        await message.answer("Введите город:")
        await state.set_state(ClientInfoForm.city)
    elif state_name == ClientInfoForm.city:
        await state.update_data(city=message.text)
        await message.answer("Введите дату рождения (в формате ГГГГ-ММ-ДД):")
        await state.set_state(ClientInfoForm.birthdate)
    elif state_name == ClientInfoForm.birthdate:
        await state.update_data(birthdate=message.text)
        user_data = await state.get_data()
        name = user_data.get('name')
        city = user_data.get('city')
        birthdate = user_data.get('birthdate')
        save_client_data_to_db(current_user_id, name, city, birthdate)
        await message.answer(f"""
                             Данные клиента:
                             ФИО: {name}
                             Город: {city}
                             Дата рождения: {birthdate}
                             """)
        await state.clear()


def get_main_menu_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Ввести ID клиента',
                                        callback_data='enter_client_id')],
            [types.InlineKeyboardButton(text='Запросить паспорт',
                                        callback_data='request_passport')],
            [types.InlineKeyboardButton(text='Запросить паспорт2',
                                        callback_data='request_passport2')],
            [types.InlineKeyboardButton(text='Запросить паспорт3',
                                        callback_data='request_passport3')],
            [types.InlineKeyboardButton(text='Добавить информацию',
                                        callback_data='add_info')]
        ]
    )
