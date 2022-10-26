from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_comment = InlineKeyboardMarkup(row_width=1)
inline_no_comment = InlineKeyboardButton('No comments 🤐', callback_data='Комментарий отсутствует')
kb_comment.row(inline_no_comment)