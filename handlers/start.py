import logging

from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from handlers.state import RegisterUser
from handlers.text import texts

load_dotenv()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="🇷🇺 Русский язык")],  # Уменьшаем размер кнопок
        [types.KeyboardButton(text="🇺🇿 O'zbek tili")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(texts['ru']['language_prompt'], reply_markup=keyboard)
    await state.set_state(RegisterUser.language)
