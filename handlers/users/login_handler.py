import re
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from database.connect_db import cur, conn
from keyboards.default import menu
from keyboards.default.cansel import cancel
from keyboards.default.menu_customer import menu_customer
from keyboards.default.menu_concierge import menu_concierge
from loader import dp
from states.employee_state import employer
from states.login_at_user import user_status
from states.login_state import log_in
from utils.format import format_phone


@dp.message_handler(text="Войти", state=None)
async def log_in_begin(message: Message ):
    await message.answer("Введите свой телефон", reply_markup=cancel)
    await log_in.auth.set()


@dp.message_handler(state=log_in.auth)
async def login(message: Message, state=FSMContext):
    conn.commit()
    r = message.text
    pattern = r'(\+7|8|7).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})'
    mes = message.from_user.id
    if re.match(pattern, r) and (len(r) == 11 and r[0] == '8' or len(r) == 12 and r[0] == '+'):
        phone = format_phone(r)
        if len(phone) == 12:
            phone = phone.replace("+7", "8")
        mas =[]
        mas.append(mes)
        mas.append(phone)
        sql_employeer = "SELECT name FROM tabEmployee WHERE name = %s" % phone
        sql = "SELECT phone FROM tabTelegramUsers WHERE enable=1 and phone =%s" % phone
        cur.execute(sql)
        if (cur.fetchall()):
            await message.answer("Вы вошли в личный кабинет", reply_markup=menu_customer)
            await user_status.logined.set()
        else:
            cur.execute(sql_employeer)
            if (cur.fetchall()):
                await message.answer(text="Вы вошли в личный кабинет сотрудника", reply_markup=menu_concierge)
                cur.execute("update tabEmployee set telegramid=? where name=?", mas)
                conn.commit()
                await employer.work.set()
            else:
                await message.answer(text="Ошибка аутентификации", reply_markup=menu)
                await state.finish()
    else:
        await message.answer(text="Неверный формат телефона, пожалуйста повторите попытку")
        await log_in.auth.set()


@dp.message_handler(text = "Выйти", state="*")
async def log_out(message: Message, state=FSMContext):
    await message.answer("Вы вышли из аккаунта", reply_markup=menu)
    await state.finish()