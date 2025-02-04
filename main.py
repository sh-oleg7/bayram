import asyncio
import logging
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message, ReplyKeyboardRemove

from database import create_user, create
from database import create_new_record



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
        'settings': "⚙️ Настройки",  # Добавляем кнопку Настройки
        'holidays_in_month': "Праздники в этом месяце:",  # Новый текст для праздников месяца
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
        'settings': "⚙️ Sozlamalar",  # Добавляем кнопку Настройки
        'holidays_in_month': "Ushbu oydagi bayramlar:",  # Новый текст для праздников месяца
    }
}

# Пример данных о праздниках для всех 12 месяцев
holidays_by_month = {
    'ru': {
        '❄️ Январь': ['Новый год (1 января)', 'Рождество (7 января)'],
        '❄️ Февраль': ['День всех влюбленных (14 февраля)'],
        '🌸 Март': ['Международный женский день (8 марта)'],
        '🌸 Апрель': ['День труда (1 мая)'],
        '🌸 Май': ['Победа в Великой Отечественной войне (9 мая)', 'День России (12 июня)'],
        '🏖️ Июнь': ['День молодежи (27 июня)'],
        '🏖️ Июль': ['День металлурга (15 июля)'],
        '🏖️ Август': ['День ВДВ (2 августа)'],
        '🍁 Сентябрь': ['День знаний (1 сентября)'],
        '🍁 Октябрь': ['День учителя (5 октября)'],
        '🍁 Ноябрь': ['День народного единства (4 ноября)'],
        '❄️ Декабрь': ['Новый год (31 декабря)'],
    },
    'uz': {
        '❄️ January': ['Yangi yil (1 yanvar)', 'Rojdestvo (7 yanvar)'],
        '❄️ February': ['Sevishganlar kuni (14 fevral)'],
        '🌸 March': ['Xalqaro ayollar kuni (8 mart)'],
        '🌸 April': ['Mehnat bayrami (1 may)'],
        '🌸 May': ['Haqiqiy mustaqillik bayrami (9 may)', 'Rossiya kuni (12 iyun)'],
        '🏖️ June': ['Yoshlar kuni (27 iyun)'],
        '🏖️ July': ['Metallurglar kuni (15 iyul)'],
        '🏖️ August': ['VDV kuni (2 avgust)'],
        '🍁 September': ['Bilimlar kuni (1 sentyabr)'],
        '🍁 October': ['O\'qituvchilar kuni (5 oktabr)'],  # Исправлено здесь
        '🍁 November': ['Xalqaro birlik kuni (4 noyabr)'],
        '❄️ December': ['Yangi yil (31 dekabr)'],
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
        [types.KeyboardButton(text="🇷🇺 Русский язык")],  # Уменьшаем размер кнопок
        [types.KeyboardButton(text="🇺🇿 O'zbek tili")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(texts['ru']['language_prompt'], reply_markup=keyboard)
    await state.set_state(RegisterUser.language)


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


class HolidayState(StatesGroup):
    month = State()
    add_holiday = State()
    add_holiday_date = State()

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


@router.message(lambda message: message.text == "📅 Месяц")
async def this_month(message: types.Message, state: FSMContext):
    import datetime

    # Создаем словарь с месяцами
    months_dict = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }

    # Получаем текущий месяц
    current_month_number = datetime.datetime.now().month

    # Находим название месяца через словарь
    current_month_name = months_dict[current_month_number]

    await message.answer(f"Текущий месяц: {current_month_name}")


@router.message(
    lambda message: message.text in holidays_by_month['ru'].keys() or message.text in holidays_by_month['uz'].keys())
async def holidays_in_month(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_lang = user_data.get('language', 'ru')

    month_name = message.text

    # Получаем список праздников для выбранного месяца
    holidays = holidays_by_month[user_lang].get(month_name, [])

    if holidays:
        holidays_text = '\n'.join(holidays)
    else:
        holidays_text = "Нет праздников в этом месяце."

    # Отправляем сообщение с праздниками
    await message.answer(f"{texts[user_lang]['holidays_in_month']} {month_name}:\n{holidays_text}")


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
    create(holiday_name, holiday_date_str, user_id)

    # Возвращаемся в главное меню
    kb = [
        [KeyboardButton(text=texts[user_lang]['all_holidays']), KeyboardButton(text=texts[user_lang]['month'])],
        [KeyboardButton(text=texts[user_lang]['add']), KeyboardButton(text=texts[user_lang]['delete'])],
        [KeyboardButton(text=texts[user_lang]['congratulations']), KeyboardButton(text=texts[user_lang]['settings'])]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await state.clear()
    await message.answer("Выберите действие:", reply_markup=keyboard)




# Запуск процесса поллинга новых апдейтов
async def main():
    bot = Bot(token="8081320278:AAENVMKnl4hWbNo7XtEULq07NQuwHVPtIVE")
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

