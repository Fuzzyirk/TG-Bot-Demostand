from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Новый стенд'),
            KeyboardButton(text='Снять шаблон')
        ],
        [
            KeyboardButton(text='Продлить стенд'),
            KeyboardButton(text='Отключить стенд')
        ],
        [
            KeyboardButton(text='Со стендом проблема')
        ],
        [
            KeyboardButton(text='Помощь'),
            KeyboardButton(text='FAQ')
        ]
    ], resize_keyboard=True
)