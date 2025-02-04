import logging

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message, ReplyKeyboardRemove
from dotenv import load_dotenv

from database import create_user
from handlers.state import RegisterUser
from handlers.text import texts
from utils import validate_name, validate_phone_number, validate_birthdate

load_dotenv()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(RegisterUser.language)
async def register_name(message: types.Message, state: FSMContext):
    user_lang = 'ru' if "🇷🇺" in message.text else 'uz'
    await state.update_data(language=user_lang)  # Сохраняем язык

    await message.answer(texts[user_lang]['name_prompt'], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegisterUser.name)


@router.message(RegisterUser.name)
async def register_name(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')

    name = message.text

    # Проверяем, состоит ли имя только из букв
    if not validate_name(name):
        await message.answer("Пожалуйста, введите имя, состоящее только из букв. Попробуйте снова.")
        return

    await state.update_data(name=name)

    contact_button = KeyboardButton(text=texts[user_lang]['phone_request'], request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[contact_button]], resize_keyboard=True)

    await message.answer(texts[user_lang]['phone_prompt'], reply_markup=keyboard)
    await state.set_state(RegisterUser.phone)


@router.message(RegisterUser.phone)
async def handle_contact(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')  # Получаем язык из состояния

    # Если пользователь прислал контакт
    if message.contact:
        phone_number = message.contact.phone_number
        phone_number = phone_number.replace("+", "")
        phone_number = "+" + phone_number
    else:
        # Если пользователь вводит номер вручную
        phone_number = message.text
    print(phone_number)
    # Если номер телефона был введен вручную, проверим его формат
    if not validate_phone_number(phone_number):
        await message.answer("Неверный номер телефона. Пожалуйста, введите номер в формате +998XXXXXXXXX.")
        return

    await state.update_data(phone=phone_number)

    await message.answer(texts[user_lang]['thanks_phone'].format(phone_number), reply_markup=ReplyKeyboardRemove())

    # Пояснение к формату даты
    await message.answer(texts[user_lang]['birthday_format'])
    await state.set_state(RegisterUser.birthday)


@router.message(RegisterUser.birthday)
async def register_birthday(message: types.Message, state: FSMContext):
    birthdate_str = message.text
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')

    valid, message_text = validate_birthdate(birthdate_str)
    if not valid:
        await message.answer(message_text)
        return

    await state.update_data(birthday=birthdate_str)

    data = await state.get_data()

    finish_message = f"{texts[user_lang]['finish']}\n" + \
                     f"Имя: {data['name']}\n" + \
                     f"Телефон: {data['phone']}\n" + \
                     f"Дата рождения: {data['birthday']}"

    create_user(data['name'], data['phone'], message.from_user.id, data['birthday'])

    await message.answer(finish_message, reply_markup=ReplyKeyboardRemove())

    # Кнопки, включая новую кнопку "Настройки"
    kb = [
        [KeyboardButton(text=texts[user_lang]['all_holidays']), KeyboardButton(text=texts[user_lang]['month'])],
        [KeyboardButton(text=texts[user_lang]['add']), KeyboardButton(text=texts[user_lang]['delete'])],
        [KeyboardButton(text=texts[user_lang]['congratulations']), KeyboardButton(text=texts[user_lang]['settings'])]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await state.clear()
    await message.answer("Выберите действие:", reply_markup=keyboard)
