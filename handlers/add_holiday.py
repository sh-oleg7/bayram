import logging

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

from database import create_birthday_data
from handlers.state import HolidayState
from handlers.text import texts
from utils import validate_birthdate

load_dotenv()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(lambda message: message.text == "➕ Добавить")
async def add_holiday(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')

    # Запросим название праздника
    await message.answer("Введите название праздника:")
    await state.set_state(HolidayState.add_holiday)


@router.message(HolidayState.add_holiday)
async def get_holiday_name(message: types.Message, state: FSMContext):
    holiday_name = message.text

    # Сохраняем название праздника
    await state.update_data(holiday_name=holiday_name)

    # Запрашиваем дату
    await message.answer("Введите дату праздника в формате DD-MM-YYYY:")
    await state.set_state(HolidayState.add_holiday_date)


@router.message(HolidayState.add_holiday_date)
async def get_holiday_date(message: types.Message, state: FSMContext):
    holiday_date_str = message.text
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')
    holiday_name = user_data.get('holiday_name')
    user_id = message.from_user.id  # ID пользователя Telegram

    # Проверка формата даты
    valid, message_text = validate_birthdate(holiday_date_str)
    if not valid:
        await message.answer(message_text)
        return

    # Сохраняем дату праздника
    await state.update_data(holiday_date=holiday_date_str)

    # Выводим информацию о празднике
    await message.answer(f"Праздник добавлен!\n\n"
                         f"Название праздника: {holiday_name}\n"
                         f"Дата: {holiday_date_str}")

    # Используем функцию create() для добавления записи в базу
    create_birthday_data(holiday_name, holiday_date_str, user_id)

    # Возвращаемся в главное меню
    kb = [
        [KeyboardButton(text=texts[user_lang]['all_holidays']), KeyboardButton(text=texts[user_lang]['month'])],
        [KeyboardButton(text=texts[user_lang]['add']), KeyboardButton(text=texts[user_lang]['delete'])],
        [KeyboardButton(text=texts[user_lang]['congratulations']), KeyboardButton(text=texts[user_lang]['settings'])]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await state.clear()
    await message.answer("Выберите действие:", reply_markup=keyboard)
