from aiogram.fsm.state import StatesGroup, State


class RegisterUser(StatesGroup):
    language = State()
    name = State()
    phone = State()
    birthday = State()


class HolidayState(StatesGroup):
    month = State()
    add_holiday = State()
    add_holiday_date = State()
