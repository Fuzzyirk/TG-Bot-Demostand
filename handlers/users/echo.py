from aiogram import types
from loader import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer('Я такого еще не понимаю')
