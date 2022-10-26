import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from loader import dp
from aiogram import types
from states import StateExtend
from loader import bot
from keyboards.inline import kb_aprove, kb_comment
from utils import jira_api


@dp.message_handler(Command("extend"), state=None)
@dp.message_handler(text='Продлить стенд', state=None)
async def extend_stand(message: types.Message):
    await message.answer("Какой стенд необходимо продлить? \n Например: “demo01”, "
                         "“http://demo.fisgroup.ru:18001/web” \n"
                         "Для отмены заявки всегда можете нажать /cancel", reply_markup=ReplyKeyboardRemove())
    await StateExtend.StateExtend1.set()


@dp.message_handler(state=StateExtend.StateExtend1)
async def extend_end_date(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["stand"] = answer
        data["user_id"] = message.from_user.id
        data['user_full'] = message.from_user.full_name
        data['user_login'] = message.from_user.username
    await message.answer("Укажите дату до которой нужно продлить стенд(обязательный формат dd.mm.yyyy)\n"
                         "Если стенд используется для презентации укажите так же время по МСК"
                         "(обязательный формат hh:mm)")
    await StateExtend.StateExtend2.set()


@dp.message_handler(state=StateExtend.StateExtend2)
async def extend_comment(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        datetime.datetime.strptime(answer.strip().split(' ')[0], '%d.%m.%Y')
        async with state.proxy() as data:
            data["date"] = answer
        await message.answer("Напишите ваш дополнительный комментарий", reply_markup=kb_comment)
        await StateExtend.StateExtend3.set()
    except ValueError:
        await message.reply('Некорректный формат даты. Повторите ввод в формате dd.mm.yyyy hh:mm')


@dp.message_handler(state=StateExtend.StateExtend3)
async def extend_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["comment"] = message.text
    data = await state.get_data()
    stand = data.get("stand")
    date = data.get("date")
    await message.answer(f"Будет создана заявка на продление стенда {stand} до {date}", reply_markup=kb_aprove)
    await StateExtend.StateExtend4.set()


@dp.callback_query_handler(state=StateExtend.StateExtend3)
async def extend_finish(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["comment"] = callback.data
    data = await state.get_data()
    user_id = data.get("user_id")
    stand = data.get("stand")
    date = data.get("date")
    await bot.send_message(user_id, f"Будет создана заявка на продление стенда {stand} до {date}",
                           reply_markup=kb_aprove)
    await StateExtend.StateExtend4.set()


@dp.callback_query_handler(state=StateExtend.StateExtend4)
async def extend_aprove(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    decision = callback.data
    if decision == 'cancel_aprove':
        await bot.send_message(user_id, "Заявка отменена")
        await state.finish()
    elif decision == 'aprove':
        data = await state.get_data()
        stand = data.get("stand")
        date = data.get("date")
        comment = data.get("comment")
        user_full = data.get("user_full")
        user_login = data.get("user_login")
        description = f'Продлить стенд {stand} до {date}.\n' \
                      f'Заявитель {user_full} {user_login}.\n' \
                      f'Дополнительный комментарий:\n{comment}'
        jira_api.create_task(f'Продлить стенд {stand}', data, description)
        await bot.send_message(user_id, f"Заявка создана")
        await state.finish()
