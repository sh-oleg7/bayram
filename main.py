import asyncio
import logging
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message, ReplyKeyboardRemove

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()

# Словари с текстами на русском и узбекском языках
texts = {
    'ru': {
        'language_prompt': "Выберите язык:",
        'name_prompt': "Введите ваше имя:",
        'phone_prompt': "Введите ваш номер телефона:",
        'birthday_prompt': "Введите дату вашего рождения:",
        'phone_request': "Поделиться номером телефона",
        'thanks_phone': "Спасибо за предоставление номера телефона: {}",
        'finish': "Регистрация завершена. Вот ваши данные: ",
        'birthday_format': "Введите вашу дату рождения в формате DD-MM-YYYY (например, 25-01-2000):",
        'all_holidays': "🎉 Все праздники",
        'month': "📅 Месяц",
        'add': "➕ Добавить",
        'delete': "❌ Удалить",
        'congratulations': "🎆 Поздравление",
        'settings': "⚙️ Настройки"  # Добавляем кнопку Настройки
    },
    'uz': {
        'language_prompt': "Tilni tanlang:",
        'name_prompt': "Ismingizni kiriting:",
        'phone_prompt': "Telefon raqamingizni kiriting:",
        'birthday_prompt': "Tug'ilgan sanangizni kiriting:",
        'phone_request': "Telefon raqamingizni ulashing",
        'thanks_phone': "Telefon raqamingiz uchun rahmat: {}",
        'finish': "Ro'yxatdan o'tish yakunlandi. Ma'lumotlaringiz: ",
        'birthday_format': "Tug'ilgan sanangizni DD-MM-YYYY formatida kiriting (masalan, 25-01-2000):",
        'all_holidays': "🎉 Barcha bayramlar",
        'month': "📅 Oyning bayramlari",
        'add': "➕ Qo'shish",
        'delete': "❌ O'chirish",
        'congratulations': "🎆  Tabriklar",
        'settings': "⚙️ Sozlamalar"  # Добавляем кнопку Настройки
    }
}


# Валидация имени (только буквы)
def validate_name(name):
    if re.match("^[A-Za-zА-Яа-яЁё]+$", name):
        return True
    return False


# Валидация номера телефона
def validate_phone_number(phone_number):
    pattern = r'^\+998[0-9]{9}$'
    if re.match(pattern, phone_number):
        return True
    return False


# Валидация даты рождения
def validate_birthdate(birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, "%d-%m-%Y")
        return True, "Дата корректна."
    except ValueError:
        return False, "Неверный формат даты. Используйте день-месяц-год (например, 25-01-2000)."


class RegisterUser(StatesGroup):
    language = State()
    name = State()
    phone = State()
    birthday = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="🇷🇺 Русский язык")],
        [types.KeyboardButton(text="🇺🇿 O'zbek tili")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(texts['ru']['language_prompt'], reply_markup=keyboard)
    await state.set_state(RegisterUser.language)


@router.message(RegisterUser.language)
async def register_name(message: types.Message, state: FSMContext):
    user_lang = 'ru' if "Русский" in message.text else 'uz'
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
    else:
        # Если пользователь вводит номер вручную
        phone_number = message.text

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

    await message.answer(finish_message, reply_markup=ReplyKeyboardRemove())

    # Кнопки, включая новую кнопку "Настройки"
    kb = [
        [KeyboardButton(text=texts[user_lang]['all_holidays']), KeyboardButton(text=texts[user_lang]['month'])],
        [KeyboardButton(text=texts[user_lang]['add']), KeyboardButton(text=texts[user_lang]['delete'])],
        [KeyboardButton(text=texts[user_lang]['congratulations'])],
        [KeyboardButton(text=texts[user_lang]['settings'])]  # Новая кнопка для настроек
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    print('test')
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=keyboard)


@router.message(lambda message: message.text == "🎉 Все праздники")
async def handle_settings(message: types.Message, state: FSMContext):
    await message.answer("test message in all holidays")
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')

    if message.text == texts[user_lang]['settings']:  # Проверяем, что выбрана кнопка "Настройки"
        # Здесь можно добавить любые действия для настроек, например:
        settings_message = "Выберите настройку:\n"
        settings_message += "1. Изменить язык\n"
        settings_message += "2. Изменить другие параметры (например, уведомления и т.д.)"

        # Кнопки для настроек
        kb = [
            [KeyboardButton(text="Изменить язык"), KeyboardButton(text="Изменить уведомления")],
            [KeyboardButton(text="Назад")]
        ]
        keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

        await message.answer(settings_message, reply_markup=keyboard)


@router.message(RegisterUser.language)
async def change_language(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')

    if message.text == "Изменить язык":
        # Приветственное сообщение с выбором языка
        kb = [
            [types.KeyboardButton(text="🇷🇺 Русский язык")],
            [types.KeyboardButton(text="🇺🇿 O'zbek tili")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer(texts[user_lang]['language_prompt'], reply_markup=keyboard)
        await state.set_state(RegisterUser.language)


# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token="8081320278:AAENVMKnl4hWbNo7XtEULq07NQuwHVPtIVE")  # Используй свой токен
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
