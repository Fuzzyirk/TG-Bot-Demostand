from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_new = InlineKeyboardMarkup(row_width=3)
inline_presentation = InlineKeyboardButton('Презентация 📊', callback_data='Презентации')
inline_access = InlineKeyboardButton('Доступ 🧑‍💻', callback_data='Демо доступа')
inline_development = InlineKeyboardButton('Разработка 🛠', callback_data='Разработки')
kb_new.row(inline_presentation, inline_access, inline_development)

kb_type_all = InlineKeyboardMarkup(row_width=2)
inline_normal = InlineKeyboardButton('Обычная 🔓', callback_data='Обычная')
inline_isolation = InlineKeyboardButton('Изолированная 🔒', callback_data='Изолированная')
kb_type_all.row(inline_normal, inline_isolation)

kb_access = InlineKeyboardMarkup(row_width=1)
inline_no_access = InlineKeyboardButton('Доступы не нужны ❌', callback_data='no access')
kb_access.row(inline_no_access)

kb_client = InlineKeyboardMarkup(row_width=1)
inline_client = InlineKeyboardButton('Внутреннее использование 🪪', callback_data='FIS')
kb_client.row(inline_client)