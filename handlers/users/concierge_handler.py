from datetime import datetime, timedelta
from aiogram.types import Message
from aiogram.utils.markdown import bold

from states.employee_state import employer
from loader import dp
from aiogram.dispatcher import FSMContext
from database.connect_db import cur, conn
from keyboards.default.back_concierge import back_menu
from states.employee_state import send_message
from loader import bot
from keyboards.default.menu_concierge import menu_concierge

@dp.message_handler(text = "Список гостей", state=employer.work)
async def show_guests(message: Message, state=FSMContext):
    await message.answer("Таблица гостей: \n")
    params = [datetime.now() - timedelta(hours=24), datetime.now()]
    conn.commit()
    sql = "select subject from tabTask where project='Добавить гостя' and creation between ? and ?"
    cur.execute(sql, params)
    str = cur.fetchall()
    a = []
    for i in range(len(str)):
        a.append(str[i][0])
    str = "\n".join(a)
    await message.answer(str)
@dp.message_handler(text="Найти гостя", state=employer.work)
async def ans_find_guest(message: Message, state=FSMContext):
    await message.answer("Введите имя гостя.")
    await employer.find.set()


@dp.message_handler(state=employer.find)
async def find_guest(message: Message, state=employer.find):
    params = "%" + message.text + "%"
    cur.execute("select subject from tabTask where project='Добавить гостя' and subject like '%s'" % params)
    print(params)
    str = cur.fetchall()
    print(str)
    a = []
    if str != []:
        for i in range(len(str)):
            a.append(str[i][0])
        str = "\n".join(a)
        await message.answer(str)
        await employer.work.set()
    else:
        await message.answer("Гость не найден")
        await employer.work.set()

@dp.message_handler(text="Отправить сообщение охране", state=employer.work)
async def call_security(message:Message, sate=FSMContext):
    await message.answer("Введите сообщение для охраны", reply_markup=back_menu)
    await send_message.security.set()


@dp.message_handler(text="Вернуться в меню сотрудника", state= send_message.security)
async def back_emp_menu(message: Message, state=FSMContext):
    await message.answer(text="Вы вышли в меню сотрудника", reply_markup=menu_concierge)
    await employer.work.set()


@dp.message_handler(state=send_message.security)
async def send_message_security(message: Message, state=FSMContext):
    text = message.text
    conn.commit()
    cur.execute("select telegramid from tabEmployee where telegramid!=%d" %message.from_user.id )
    data = cur.fetchall()
    print(data)
    cur.execute("select middle_name, first_name, last_name, employment_type, location from tabEmployee where "
                "telegramid=%d" % message.from_user.id)
    mas = cur.fetchall()
    from_employee = "Сообщение от: " + mas[0][0] + " " + mas[0][1] + " " + mas[0][2] + "\nДолжность: " + mas[0][3] + \
                    "\nМестоположение: " + mas[0][4] + "\nТекст сообщения: %s" %text
    if (data):
        for i in data:
            await bot.send_message(i[0], from_employee)
        await message.answer(text="Сообщение отправлено", reply_markup=menu_concierge)
        await employer.work.set()
    else:
        await message.answer("Нет охранников", reply_markup=menu_concierge)
        await employer.work.set()