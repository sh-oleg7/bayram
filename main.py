import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from handlers.text import texts, holidays_by_month

load_dotenv()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()

TOKEN = os.getenv("BOT_TOKEN", "")
bot = Bot(token=TOKEN)
dp = Dispatcher()


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


# Запуск процесса поллинга новых апдейтов
async def main():
    from handlers import register_handlers

    dp.include_router(router)
    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
