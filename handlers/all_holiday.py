import logging

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from dotenv import load_dotenv

from handlers.state import HolidayState
from handlers.text import texts, holidays_by_month

load_dotenv()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(lambda message: message.text == "🎉 Все праздники")
async def handle_all_holidays(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')

    # Разделим месяцы на 3 группы по 4 месяца
    months = list(holidays_by_month[user_lang].keys())
    months_grouped = [months[i:i + 3] for i in range(0, len(months), 3)]

    # Формируем клавиатуру с 3 рядами (по 4 месяца)
    months_buttons = [
        [KeyboardButton(text=month) for month in group] for group in months_grouped
    ]
    months_buttons.append([KeyboardButton(text="Назад")])  # Кнопка назад

    keyboard = ReplyKeyboardMarkup(keyboard=months_buttons, resize_keyboard=True)

    await message.answer(texts[user_lang]['all_holidays'], reply_markup=keyboard)
    await state.set_state(HolidayState.month)  # Переход в состояние выбора месяца


@router.message(HolidayState.month)
async def holiday_handler(message: Message, state: FSMContext):
    # Если выбрана кнопка "Назад", возвращаем в основное меню
    if message.text == "Назад":
        user_data = await state.get_data()
        user_lang = user_data.get('language', 'ru')

        kb = [
            [KeyboardButton(text=texts[user_lang]['all_holidays']), KeyboardButton(text=texts[user_lang]['month'])],
            [KeyboardButton(text=texts[user_lang]['add']), KeyboardButton(text=texts[user_lang]['delete'])],
            [KeyboardButton(text=texts[user_lang]['congratulations']),
             KeyboardButton(text=texts[user_lang]['settings'])]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await state.clear()
        await message.answer("Выберите действие:", reply_markup=keyboard)
