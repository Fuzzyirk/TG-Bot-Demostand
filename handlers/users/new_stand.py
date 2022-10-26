import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from keyboards.inline import kb_new, kb_type_all, kb_access, kb_comment, kb_aprove, kb_client
from loader import bot
from logic import ds1


from loader import dp
from aiogram import types
from states import StateNew
from utils import jira_api


@dp.message_handler(Command("new"), state=None)
@dp.message_handler(text='Новый стенд', state=None)
async def new_stand(message: types.Message):
    await message.answer("<b>для презентации</b> – когда запрашивают стенд только на несколько часов для показа "
                         "презентации клиенту\n<b>для доступа</b> – когда запрашивают для открытия доступа клиенту "
                         "для самостоятельного изучения\n<b>для доработок</b> – когда нужен стенд для модификации "
                         "существующего шаблона или создания нового на основе имеющегося/копии с разработческого",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Какой тип демостенда требуется?\n"
                         "Для отмены заявки всегда можете нажать /cancel", reply_markup=kb_new)
    await StateNew.StateNew1.set()


@dp.callback_query_handler(state=StateNew.StateNew1)
async def new_template(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    async with state.proxy() as data:
        data["purpose"] = answer
        data["user_id"] = callback.from_user.id
        data['user_full'] = callback.from_user.full_name
        data['user_login'] = callback.from_user.username
    await bot.send_message(callback.from_user.id, "Какой номер шаблона нужен? Например, FPL123")
    await StateNew.StateNew2.set()


@dp.message_handler(state=StateNew.StateNew2)
async def new_start_date(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["template"] = str(answer).strip().replace('фпл', 'fpl').replace(' ', '').lower()
    data = await state.get_data()
    purpose = data.get("purpose")
    if purpose == 'Презентации':
        await message.answer("Укажите дату и время(по МСК) с которого нужен стенд\n"
                             "<b>обязательный формат dd.mm.yyyy hh:mm</b>")
    else:
        await message.answer("Укажите дату с которой нужен стенд\n"
                             "<b>обязательный формат dd.mm.yyyy</b>")
    await StateNew.StateNew3.set()


@dp.message_handler(state=StateNew.StateNew3)
async def new_end_date(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    purpose = data.get("purpose")
    date = answer.strip().split(' ')[0].replace('\\', '.').replace('/', '.').replace('-', '.')
    try:
        answer = date + ' ' + answer.strip().split(' ')[1]
    except Exception as err:
        print(err)
    try:
        if purpose == 'Презентации':
            datetime.datetime.strptime(answer, '%d.%m.%Y %H:%M')
            await message.answer("Укажите дату и время(По МСК) по которые нужен стенд\n"
                                 "<b>обязательный формат dd.mm.yyyy hh:mm</b>")
        else:
            datetime.datetime.strptime(date, '%d.%m.%Y')
            await message.answer("Укажите дату по которую нужен стенд\n"
                                 "<b>обязательный формат dd.mm.yyyy</b>")
        async with state.proxy() as data:
            data["start_date"] = answer
        await StateNew.StateNew4.set()
    except ValueError:
        if purpose == 'Презентации':
            await message.reply('Некорректный формат даты. Повторите ввод в формате <b>dd.mm.yyyy hh:mm</b>')
        else:
            await message.reply('Некорректный формат даты. Повторите ввод в формате <b>dd.mm.yyyy</b>')
        return


@dp.message_handler(state=StateNew.StateNew4)
async def new_client(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    purpose = data.get("purpose")
    date = answer.strip().split(' ')[0].replace('\\', '.').replace('/', '.').replace('-', '.')
    try:
        answer = date + ' ' + answer.strip().split(' ')[1]
    except Exception as err:
        print(err)
    try:
        if purpose == 'Презентации':
            datetime.datetime.strptime(answer, '%d.%m.%Y %H:%M')
        else:
            datetime.datetime.strptime(date, '%d.%m.%Y')
        await message.answer("Наименование клиента?", reply_markup=kb_client)
        async with state.proxy() as data:
            data["end_date"] = answer
        await StateNew.StateNew5.set()
    except ValueError:
        if purpose == 'Презентации':
            await message.reply('Некорректный формат даты. Повторите ввод в формате dd.mm.yyyy hh:mm')
        else:
            await message.reply('Некорректный формат даты. Повторите ввод в формате dd.mm.yyyy')
        return


@dp.message_handler(state=StateNew.StateNew5)
async def new_access_message(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["client"] = answer
    await message.answer("Если кому-то нужны доступы до стенда, перечислите IP или логины профиля vpn(если есть) "
                         "кому нужны доступы через пробел", reply_markup=kb_access)
    await StateNew.StateNew6.set()


@dp.callback_query_handler(state=StateNew.StateNew5)
async def new_access_callback(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    async with state.proxy() as data:
        data["client"] = answer
    data = await state.get_data()
    user_id = data.get("user_id")
    await bot.send_message(user_id, "Если кому-то нужны доступы до стенда, перечислите IP или логины профиля "
                                    "vpn(если есть) кому нужны доступы через пробел", reply_markup=kb_access)
    await StateNew.StateNew6.set()


@dp.message_handler(state=StateNew.StateNew6)
async def new_type_mes(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["access"] = answer
    data = await state.get_data()
    template = data.get("template")
    if template not in ds1:
        async with state.proxy() as data:
            data["type"] = 'old'
        await message.answer("Ваш дополнительный комментарий", reply_markup=kb_comment)
        await StateNew.StateNew8.set()
    else:
        if str(answer).lower() == "нет":
            await message.answer("Нужна изолированная среда?", reply_markup=kb_type_all)
            await StateNew.StateNew7.set()
        else:
            async with state.proxy() as data:
                data["type"] = 'Обычная'
            await message.answer("Ваш дополнительный комментарий", reply_markup=kb_comment)
            await StateNew.StateNew8.set()


@dp.callback_query_handler(state=StateNew.StateNew6)
async def new_type_qu(callback: CallbackQuery, state: FSMContext):
    answer = callback.data
    async with state.proxy() as data:
        data["access"] = answer
    data = await state.get_data()
    template = data.get("template")
    user_id = data.get("user_id")
    if template not in ds1:
        async with state.proxy() as data:
            data["type"] = 'old'
        await bot.send_message(user_id, "Ваш дополнительный комментарий", reply_markup=kb_comment)
        await StateNew.StateNew8.set()
    else:
        await bot.send_message(user_id, "<b>Обычная</b> - внешняя ссылка(http://demo.fisgroup.ru:180XX/web). "
                                        "Доступ предоставляется по IP или VPN. Возможен доступ из нашей инфраструктуры "
                                        "по доп. портам (включая SSH).\n<b>Изолированная</b> - внешняя ссылка"
                                        "(http://demo.fisgroup.ru:190ХХ/web). Доступ открыт всем по ссылке,"
                                        " SSH и дополнительные порты исключены. Высокий риск потери стенда, риск для "
                                        "инфраструктуры минимален.")
        await bot.send_message(user_id, "В какой среде нужен стенд?", reply_markup=kb_type_all)
        await StateNew.StateNew7.set()


@dp.callback_query_handler(state=StateNew.StateNew7)
async def new_comment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    answer = callback.data
    if str(answer).lower() == "обычная":
        async with state.proxy() as data:
            data["type"] = 'Обычная'
        await bot.send_message(user_id, "Тогда укажите доступы", reply_markup=kb_access)
        await StateNew.StateNew6.set()
    elif str(answer).lower() == "изолированная":
        async with state.proxy() as data:
            data["type"] = "Изолированная"
        await bot.send_message(user_id, "Ваш дополнительный комментарий", reply_markup=kb_comment)
        await StateNew.StateNew8.set()


@dp.message_handler(state=StateNew.StateNew8)
async def new_finish_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["comment"] = message.text
    data = await state.get_data()
    purpose = data.get("purpose")
    template = data.get("template")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    client = data.get("client")
    access = data.get("access")
    text = f"Будет создана заявка на установку шаблона {template} для {purpose} с {start_date} до {end_date} " \
           f"для клиента {client}"
    if access != 'no access':
        text += f"\nДоступы будут предоставлены для:\n{access}\n"
    await message.answer(text, reply_markup=kb_aprove)
    await StateNew.StateNew9.set()


@dp.callback_query_handler(state=StateNew.StateNew8)
async def new_finish_callback(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["comment"] = callback.data
    data = await state.get_data()
    purpose = data.get("purpose")
    template = data.get("template")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    client = data.get("client")
    user_id = data.get("user_id")
    access = data.get("access")
    text = f"Будет создана заявка на установку шаблона {template} для {purpose} с {start_date} до {end_date} " \
           f"для клиента {client}"
    if access != 'no access':
        text += f"\nДоступы будут предоставлены для:\n{access}\n"
    await bot.send_message(user_id, text, reply_markup=kb_aprove)
    await StateNew.StateNew9.set()


@dp.callback_query_handler(state=StateNew.StateNew9)
async def new_aprove(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    decision = callback.data
    if decision == 'cancel_aprove':
        await bot.send_message(user_id, "Заявка отменена")
        await state.finish()
    elif decision == 'aprove':
        purpose = data.get("purpose")
        template = data.get("template")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        client = data.get("client")
        access = data.get("access")
        user_full = data.get("user_full")
        user_login = data.get("user_login")
        comment = data.get("comment")
        stand_type = data.get("type")
        description = f'Развернуть шаблон {template} для {purpose}\n' \
                      f'Требуется с {start_date} до {end_date}\n' \
                      f'Заказчик - {user_full} {user_login}\n' \
                      f'Клиент - {client}\n'
        if stand_type != 'old':
            description += f'Среда {stand_type}\n'
        if access != 'no access':
            description += f'Предоставить доступы к стенду:\n{access}\n'
        if comment != 'Комментарий отсутствует':
            description += f'Дополнительный комментариий:\n{comment}\n'
        jira_api.create_task(f'Развернуть шаблон {template} к {start_date}', data, description)
        await bot.send_message(user_id, f"Заявка создана")
        await state.finish()
