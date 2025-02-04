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

