from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_faq = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изолированная/Обычная среда')
        ],
        [
            KeyboardButton(text='Для презентации/Доступа/Разработки')
        ],
        [
            KeyboardButton(text='Доступ к SSH'),
            KeyboardButton(text='Доступ к СП')
        ],
        [
            KeyboardButton(text='Доступ клиенту по VPN'),
        ],
        [
            KeyboardButton(text='Клиент не может войти на стенд'),
        ],
        [
            KeyboardButton(text='Не открывается http://demo.fisgroup.ru:180XX/web у сотрудника'),
        ],
        [
            KeyboardButton(text='Ошибка JDBCException: Cannot open connection'),
        ]
    ], resize_keyboard=True
)