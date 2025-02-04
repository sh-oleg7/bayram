import re
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


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
