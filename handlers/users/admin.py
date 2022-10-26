from aiogram import types
from aiogram.dispatcher.filters import filters

from loader import dp
from logic.costants import ds1

from data.config import admins


@dp.message_handler(lambda msg: str(msg.text.lower()).startswith('add'))
async def append_template(message: types.Message):
    if message.from_user.id in admins:
        template = message.text.strip().split(' ')[1].lower()
        ds1.append(template)
        await message.answer(f'Привет, {template} Добавлен в репозиторий ds1')
    else:
        await message.answer(f'У вас нет доступа на управление шаблонами')


@dp.message_handler(lambda msg: str(msg.text.lower()).startswith('show'))
async def show_templates(message: types.Message):
    if message.from_user.id in admins:
        templates = ', '.join(ds1)
        await message.answer(f'Привет, шаблоны в ds1: {templates}')
    else:
        await message.answer(f'У вас нет доступа на управление шаблонами')


@dp.message_handler(lambda msg: str(msg.text.lower()).startswith('del'))
async def drop_template(message: types.Message):
    if message.from_user.id in admins:
        template = message.text.strip().split(' ')[1].lower()
        ds1.remove(template)
        await message.answer(f'Привет, шаблон {template} удален из ds1')
    else:
        await message.answer(f'У вас нет доступа на управление шаблонами')


@dp.message_handler(lambda msg: str(msg.text.lower()).startswith('newadmin'))
async def drop_template(message: types.Message):
    if message.from_user.id in admins:
        admin = int(message.text.strip().split(' ')[1].lower())
        admins.append(admin)
        await message.answer(f'Привет, админ добавлен')
    else:
        await message.answer(f'У вас нет доступа на управление админами')
