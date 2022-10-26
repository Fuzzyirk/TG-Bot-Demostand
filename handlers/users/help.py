from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
# from utils.misc import rate_limit
from data.config import admins


# @rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
@dp.message_handler(text='Помощь')
async def bot_help(message: types.Message):
    if message.from_user.id in admins:
        text= [
            'Список команд: ',
            '/start - Начало работы',
            '/help - Получить справку',
            '/new - Заявка на заказ нового стенда',
            '/extend - Заявка на продление стенда',
            '/turnoff - Заявка на выключение стенда',
            '/template - Заявка на снятие шаблона',
            '/problem - Заявка по проблеме со стендом',
            '/cancel - Отмена при создании заявки',
            '/faq - FAQ',
            'add <Название шаблона> - Добавить шабон в список репозитория ds1',
            'show - показать шаблоны, находящиеся в репозитории ds1',
            'del <Название шаблона> - Удалить шабон из списка репозитория ds1',
            'newadmin <ID телеграмм> - добавить админа'
        ]
    else:
        text = [
            'Список команд: ',
            '/start - Начало работы',
            '/help - Получить справку',
            '/new - Заявка на заказ нового стенда',
            '/extend - Заявка на продление стенда',
            '/turnoff - Заявка на выключение стенда',
            '/template - Заявка на снятие шаблона',
            '/problem - Заявка по проблеме со стендом',
            '/cancel - Отмена при создании заявки',
            '/faq - FAQ',
        ]
    await message.answer('\n'.join(text))

