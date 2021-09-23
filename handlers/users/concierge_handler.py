from datetime import datetime, timedelta
from aiogram.types import Message
from aiogram.utils.markdown import bold

from states.employee_state import employer
from loader import dp
from aiogram.dispatcher import FSMContext
from keyboards.default.back_concierge import back_menu
from states.employee_state import send_message
from loader import bot
import mariadb
from data.config import user, password, host, port, database
from keyboards.default.menu_concierge import menu_concierge

@dp.message_handler(text = "Список гостей", state=employer.work)
async def show_guests(message: Message, state=FSMContext):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    cur = conn.cursor()
    await message.answer("Таблица гостей: \n")
    params = [datetime.now() - timedelta(hours=24), datetime.now()]
    conn.commit()
    sql = "select subject from tabTask where project='Добавить гостя' and status='Активен' and creation between ? and ?"
    cur.execute(sql, params)
    str = cur.fetchall()
    if(str):
        a = []
        for i in range(len(str)):
            a.append("• " + str[i][0])
        str = "\n".join(a)
    else:
        str = "На данный момент гостей нет."
    conn.close()
    await message.answer(str)
@dp.message_handler(text="Найти гостя", state=employer.work)
async def ans_find_guest(message: Message, state=FSMContext):
    await message.answer("Введите имя гостя.")
    await employer.find.set()

@dp.message_handler(state=employer.find)
async def find_guest(message: Message, state=FSMContext):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    cur = conn.cursor()
    params = "%" + message.text + "%"
    cur.execute("select subject from tabTask where status='Активен' and subject like '%s'" % params)
    str = cur.fetchall()
    a = []
    mes = f"Список гостей по запросу: {message.text}"
    if str != []:
        for i in range(len(str)):
            a.append("• " + str[i][0])
        mes += "\n".join(a)
        await message.answer(mes)
    else:
        await message.answer("Гость не найден")
    conn.close()
    await employer.work.set()

@dp.message_handler(text="Отправить сообщение охране", state=employer.work)
async def call_security(message:Message, sate=FSMContext):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    cur = conn.cursor()
    await send_message.security.set()
    conn.commit()
    cur.execute("select telegramid from tabEmployee where employment_type='Охрана'")
    data = cur.fetchall()
    cur.execute("select middle_name, first_name, last_name, employment_type, location from tabEmployee where "
                "telegramid=%d" % message.from_user.id)
    mas = cur.fetchall()
    from_employee = "Сообщение от: " + mas[0][0] + " " + mas[0][1] + " " + mas[0][2] + "\nДолжность: " + mas[0][3] + \
                    "\nМестоположение: " + mas[0][4]
    if data != [(None,)]:
        for i in data:
            await bot.send_message(i[0], from_employee)
        await message.answer("Введите сообщение для охраны", reply_markup=back_menu)
        conn.close()
        await send_message.security.set()
    else:
        await message.answer("Нет охранников", reply_markup=menu_concierge)
        conn.close()
        await employer.work.set()


@dp.message_handler(text="Назад", state= send_message.security)
async def back_emp_menu(message: Message, state=FSMContext):
    await message.answer(text="Вы возвращены в меню.", reply_markup=menu_concierge)
    await employer.work.set()


@dp.message_handler(state=send_message.security)
async def send_message_security(message: Message, state = FSMContext):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    cur = conn.cursor()
    text = message.text
    cur.execute("select middle_name, first_name, last_name from tabEmployee where "
                "telegramid=%d" % message.from_user.id)
    mas = cur.fetchall()
    cur.execute("select telegramid from tabEmployee where employment_type='Охрана'")
    data = cur.fetchall()
    for i in data:
        await bot.send_message(i[0], "<b>" + text + "</b>" + "\nот " + mas[0][0] + " " + mas[0][1][0]
                               + "." + mas[0][2][0] + ".")
    await message.answer(text="Сообщение отправлено", reply_markup=menu_concierge)
    conn.close()
    await employer.work.set()

