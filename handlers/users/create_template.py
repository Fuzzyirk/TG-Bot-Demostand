from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from keyboards.inline import kb_aprove
from loader import bot


from loader import dp
from aiogram import types
from states import StateTemplate
from utils import jira_api


@dp.message_handler(Command("template"), state=None)
@dp.message_handler(text='Снять шаблон', state=None)
async def template_stand(message: types.Message):
    await message.answer("Напишите ссылку на стенд или номер стенда, с которого нужно снять шаблон?\n"
                         "Для отмены заявки всегда можете нажать /cancel", reply_markup=ReplyKeyboardRemove())
    await StateTemplate.StateTemplate1.set()


@dp.message_handler(state=StateTemplate.StateTemplate1)
async def template_short_description(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["stand"] = answer
        data["user_id"] = message.from_user.id
        data['user_full'] = message.from_user.full_name
        data['user_login'] = message.from_user.username
    await message.answer("Напишите краткое описание(название) шаблона")
    await StateTemplate.StateTemplate2.set()


@dp.message_handler(state=StateTemplate.StateTemplate2)
async def template_description(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["short_description"] = answer
    await message.answer("Напишите описание шаблона с указанием логинов и паролей")
    await StateTemplate.StateTemplate3.set()


@dp.message_handler(state=StateTemplate.StateTemplate3)
async def template_platform(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["description"] = answer
    await message.answer("Какая версия платформы на стенде?")
    await StateTemplate.StateTemplate4.set()


@dp.message_handler(state=StateTemplate.StateTemplate4)
async def template_ram(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["platform"] = answer
    await message.answer("Сколько Гб памяти занимает шаблон(RAM)?")
    await StateTemplate.StateTemplate5.set()


@dp.message_handler(state=StateTemplate.StateTemplate5)
async def template_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["ram"] = message.text
    data = await state.get_data()
    stand = data.get("stand")
    short_description = data.get("short_description")
    platform = data.get("platform")
    await message.answer(f"Будет создана заявка на снятие шаблона со стенда {stand} с версией платформы {platform} и "
                         f"занимаемой памятью {message.text}GB\nКраткое описание:\n{short_description}",
                         reply_markup=kb_aprove)
    await StateTemplate.StateTemplate6.set()


@dp.callback_query_handler(state=StateTemplate.StateTemplate6)
async def template_aprove(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    decision = callback.data
    if decision == 'cancel_aprove':
        await bot.send_message(user_id, "Заявка отменена")
        await state.finish()
    elif decision == 'aprove':
        stand = data.get("stand")
        short_description = data.get("short_description")
        description = data.get("description")
        platform = data.get("platform")
        ram = data.get("ram")
        user_full = data.get("user_full")
        user_login = data.get("user_login")
        description = f'Снять шаблон со стенда {stand}\n' \
                      f'Заявитель - {user_full} {user_login}\n' \
                      f'RAM {ram}GB\n' \
                      f'Версия платформы {platform}\n' \
                      f'Краткое описание:\n{short_description}\n' \
                      f'Описание:\n{description}'
        jira_api.create_task(f'Снятие шаблона с {stand}', data, description)
        await bot.send_message(user_id, f"Заявка создана")
        await state.finish()
