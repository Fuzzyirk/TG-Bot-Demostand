from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начало работы"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("new", "Заказать новый стенд"),
        types.BotCommand("extend", "Продлить имеющейся стенд"),
        types.BotCommand("turnoff", "Выключение стенда"),
        types.BotCommand("template", "Снять шаблон"),
        types.BotCommand("problem", "Проблема со стендом"),
        types.BotCommand("cancel", "Отмена процесса заполнения заявки"),
        types.BotCommand("faq", "FAQ"),
    ])
