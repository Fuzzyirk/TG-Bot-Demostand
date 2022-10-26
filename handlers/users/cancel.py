from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram import types
from states import StateExtend, StateNew, StateTurnOff, StateTemplate, StateProblem


@dp.message_handler(commands=['cancel'], state=StateExtend.all_states)
@dp.message_handler(commands=['cancel'], state=StateNew.all_states)
@dp.message_handler(commands=['cancel'], state=StateTurnOff.all_states)
@dp.message_handler(commands=['cancel'], state=StateTemplate.all_states)
@dp.message_handler(commands=['cancel'], state=StateProblem.all_states)
async def extend_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="Действие отменено. Для возобновления нажмите /start",
    )
