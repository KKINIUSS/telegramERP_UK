from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from keyboards.default import menu
from loader import dp


@dp.message_handler(CommandStart())
async def show_menu(message: Message):
    mes = message.from_user.id
    await message.answer(f"Вас приветствует бот-помощник ЖК!", reply_markup=menu)

@dp.message_handler(text="отмена", state="*")
async def back_from_reg(message: Message, state=FSMContext):
    await message.answer("Вы вернулись в главное меню", reply_markup=menu)
    await state.finish()
