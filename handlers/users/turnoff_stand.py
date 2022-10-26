import datetime

from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from keyboards.inline import kb_aprove
from loader import bot
from utils import jira_api

from loader import dp
from aiogram import types
from states import StateTurnOff


@dp.message_handler(Command("turnoff"))
@dp.message_handler(text='Отключить стенд')
async def turnoff_stand(message: types.Message):
    await message.answer("Какой стенд необходимо выключить? \n "
                         "Например: “demo01”, “http://demo.fisgroup.ru:18001/web”\n"
                         "Для отмены заявки всегда можете нажать /cancel", reply_markup=ReplyKeyboardRemove())
    await StateTurnOff.StateTurnOff1.set()


@dp.message_handler(state=StateTurnOff.StateTurnOff1)
async def turnoff_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['stand'] = message.text
        data["user_id"] = message.from_user.id
        data['user_full'] = message.from_user.full_name
        data['user_login'] = message.from_user.username
    await message.answer(f"Будет создана заявка на выключение стенда {message.text}\n"
                         f"Стенд будет отключен, шаблон затерт",
                         reply_markup=kb_aprove)
    await StateTurnOff.StateTurnOff2.set()


@dp.callback_query_handler(state=StateTurnOff.StateTurnOff2)
async def turnoff_aprove(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    decision = callback.data
    if decision == 'cancel_aprove':
        await bot.send_message(user_id, "Заявка отменена")
        await state.finish()
    elif decision == 'aprove':
        stand = data.get("stand")
        user_full = data.get("user_full")
        user_login = data.get("user_login")
        date = datetime.datetime.today().strftime('%d-%m-%Y %H:%M')
        description = f'Выключить стенд {stand}.\n Заявитель {user_full} {user_login}.\n {date}'
        jira_api.create_task(f'Отключение стенда {stand}', data, description)
        await bot.send_message(user_id, f"Заявка создана")
        await state.finish()
