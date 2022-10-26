import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from keyboards.inline import kb_screen, kb_aprove
from loader import bot

from loader import dp
from aiogram import types
from states import StateProblem
from utils import jira_api


@dp.message_handler(Command("problem"), state=None)
@dp.message_handler(text='Со стендом проблема', state=None)
async def problem_stand(message: types.Message):
    await message.answer("Надеюсь вы подробно озникомились с /faq", reply_markup=ReplyKeyboardRemove())
    await message.answer("Напишите ссылку на стенд или номер стенда, с которым возникла проблема?\n"
                         "Для отмены заявки всегда можете нажать /cancel")
    await StateProblem.StateProblem1.set()


@dp.message_handler(state=StateProblem.StateProblem1)
async def problem_reporter(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["stand"] = answer
        data["user_id"] = message.from_user.id
        data["user_full"] = message.from_user.full_name
        data["user_login"] = message.from_user.username
    await message.answer("У кого возникла проблема(заказчик/сотрудник, логин, ФИО, организация). "
                         "Как работает сотрудник(офис, ВПН, ip)")
    await StateProblem.StateProblem2.set()


@dp.message_handler(state=StateProblem.StateProblem2)
async def problem_description(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["reporter"] = answer
    await message.answer("С какой проблемой вы столкнулись?")
    await StateProblem.StateProblem3.set()


@dp.message_handler(state=StateProblem.StateProblem3)
async def problem_screenshot(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["description"] = answer
    await message.answer("Прикрепите скриншот", reply_markup=kb_screen)
    await StateProblem.StateProblem4.set()


@dp.callback_query_handler(state=StateProblem.StateProblem4)
async def problem_finish_callback(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["screenshot"] = callback.data
    data = await state.get_data()
    stand = data.get("stand")
    reporter = data.get("reporter")
    description = data.get("description")
    user_id = data.get("user_id")
    screenshot = callback.data
    await bot.send_message(user_id, f"Будет создана заявка на устранение проблемы:\n{description}\n Со стендом {stand} "
                                    f"\nУ {reporter}", reply_markup=kb_aprove)
    await StateProblem.StateProblem5.set()


@dp.message_handler(content_types=['photo'], state=StateProblem.StateProblem4)
async def problem_finish_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    date = datetime.datetime.today().strftime('%d%m%Y_%H%M')
    stand = data.get("stand")
    reporter = data.get("reporter")
    description = data.get("description")
    user_login = data.get("user_login")
    screenshot = f'{date}_screenshot_{user_login}.jpg'
    async with state.proxy() as data:
        data["screenshot"] = screenshot
    await message.photo[-1].download(destination_file=f'files/screenshots/{screenshot}')
    await message.answer(f"Будет создана заявка на устранение проблемы:\n{description}\nСо стендом {stand} "
                         f"\nУ {reporter}", reply_markup=kb_aprove)
    await StateProblem.StateProblem5.set()


@dp.callback_query_handler(state=StateProblem.StateProblem5)
async def problem_aprove(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    decision = callback.data
    if decision == 'cancel_aprove':
        await bot.send_message(user_id, "Заявка отменена")
        await state.finish()
    elif decision == 'aprove':
        stand = data.get("stand")
        reporter = data.get("reporter")
        description = data.get("description")
        user_id = data.get("user_id")
        user_full = data.get("user_full")
        user_login = data.get("user_login")
        screenshot = data.get("screenshot")
        if screenshot == 'Скриншот не прикреплен':
            description = f'Проблема со стендом {stand}.\nЗаявитель {user_full} {user_login}.\nСуть проблемы:\n' \
                          f'{description}\nПроблема у {reporter}\n{screenshot}'
            jira_api.create_task(f'Проблема со стендом {stand}', data, description)
        else:
            description = f'Проблема со стендом {stand}.\nЗаявитель {user_full} {user_login}.\nСуть проблемы:\n' \
                          f'{description}\nПроблема у {reporter}'
            jira_api.create_task(f'Проблема со стендом {stand}', data, description, screenshot=screenshot)
        await bot.send_message(user_id, f"Заявка создана")
        await state.finish()
