from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsGroup(BoundFilter):
    async def check(self, message=types.Message):
        return message.chat.type.isinstance(types.ChatType.GROUP)
