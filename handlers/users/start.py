from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message
from keyboards.default import menu
from loader import dp
from database.connect_db import conn, cur
from keyboards.default.menu_customer import menu_customer
from keyboards.default.menu_concierge import menu_concierge
from states.login_at_user import user_status
from states.employee_state import employer
from states.registration import registration
@dp.message_handler(CommandStart())
async def show_menu(message: Message):
    conn.commit()
    cur.execute("select name, status, role from tabTelegramUsers where telegramid=?", [message.from_user.id])
    k = cur.fetchall()
    if(k[0][0]):
        if(k[0][1]=='Подтвержден'):
            if(k[0][2] == 'Житель'):
                await message.answer("Вас приветствует бот-помощник ЖК, выберите 'Добавить гостя', чтобы сделать пропуск.", reply_markup=menu_customer)
                await user_status.logined.set()
            elif(k[0][2] == 'Охранник'):
                await message.answer("Добрый день!", reply_markup=menu_concierge)
                await employer.work.set()
            else:
                await message.answer("Вам не выдана роль. Свяжитесь с администратором системы.")
        elif(k[0][1] == 'На рассмотрении'):
            await message.answer("Ваша учетная запись еще не подтверждена. Дождитесь уведомления, а затем введите /start.")
        else:
            await message.answer("Данные учётной записи не корректны, свяжитесь с администратором системы.")
    else:
        await message.answer("Добрый день, нажмите кнопку 'Зарегистрироваться', чтобы пройти регистрацию.", reply_markup=menu)
        await registration.start.set()
@dp.message_handler(text="отмена", state="*")
async def back_from_reg(message: Message, state=FSMContext):
    await message.answer("Вы вернулись в главное меню", reply_markup=menu)
    await state.finish()
