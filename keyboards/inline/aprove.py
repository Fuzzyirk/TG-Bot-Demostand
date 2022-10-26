from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_aprove = InlineKeyboardMarkup(row_width=1)
inline_aprove = InlineKeyboardButton('Создать заявку 📨', callback_data='aprove')
inline_cancel = InlineKeyboardButton('Отмена ❌', callback_data='cancel_aprove')
kb_aprove.row(inline_aprove, inline_cancel)
