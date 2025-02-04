import logging

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()


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
