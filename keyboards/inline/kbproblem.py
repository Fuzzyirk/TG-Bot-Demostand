from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_screen = InlineKeyboardMarkup(row_width=1)
inline_no_screen = InlineKeyboardButton('Скриншот не нужен/отсутствует ❌', callback_data='Скриншот не прикреплен')
kb_screen.row(inline_no_screen)