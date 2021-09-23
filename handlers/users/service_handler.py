import re
import datetime
from aiogram.types import Message, CallbackQuery
from keyboards.default.menu_customer import menu_customer
from keyboards.inline.service_buttons import service_buttons
from loader import dp
from utils.format import format_phone
from states.service_state import choice_service as c_s, add_guest
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel
from states.login_at_user import user_status
from database.connect_db import conn, cur
from keyboards.default.back_from_service import bac_service_menu

@dp.message_handler(text="Сделать запрос", state=user_status.logined)
async def enter_service(message: Message):
        await message.answer(text=f"Вы выбрали {message.text}")
        await message.answer(text="Пожалуйста, выберете один из пунктов", reply_markup=service_buttons)
        await c_s.choice.set()

@dp.callback_query_handler(text_contains="serv:Добавить гостя", state=c_s.choice)
async def add_geust(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите информацию о госте(ФИО, марку/номер машины)", reply_markup=bac_service_menu)
    await add_guest.get_name.set()

@dp.message_handler(state=add_guest.get_name)
async def get_name(message: Message, state: FSMContext):
    str_message = message.text
    if len(str_message)>40:
        await message.answer("Невеный формат\nИнфорация о госте должна содержать не более 40 символов, повторите снова")
        await message.answer("Введите информацию о госте(ФИО, марку/номер машины)", reply_markup=bac_service_menu)
        await add_guest.get_name.set()
    else:
        print(1)
        guest_name = message.text
        await state.update_data(guest_name=guest_name)
        cur.execute("select full_name from tabTelegramUsers where telegramid=?", [message.from_user.id])
        customers = cur.fetchall()
        customer = customers[0][0]
        data = await state.get_data()
        sql = "select count(name)+1 from tabTask"
        cur.execute(sql)
        answerDb = cur.fetchall()
        sql = "INSERT INTO tabTask (name, subject, project, creation, owner, status, exp_start_date, exp_end_date) VALUES (%s, %s, %s, %s, %s, 'Активен', %s, %s)"
        count_task = "TASK-2021-" + str(answerDb[0][0])
        from datetime import timedelta
        today = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        zavtra = today + delta
        mas = [count_task, data.get("guest_name"), "Добавить гостя", str(datetime.datetime.now()), customer, today, zavtra]
        cur.execute(sql, mas)
        conn.commit()
        await message.answer("Гость успешно добавлен", reply_markup=menu_customer)
        await user_status.logined.set()

@dp.message_handler(state=add_guest.get_phone)
async def get_phone(message: Message, state: FSMContext):
    print(1)
    #r = message.text
    #pattern =r"\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b"
    mas = []
    #if re.match(pattern, r) and ((len(r) == 11 and (r[0] == '8') or (len(r) == 12 and r[0] == '+'))):
    cur.execute("select full_name from tabTelegramUsers where name = %s" %message.from_user.id)
    customer = cur.fetchall()[0][0]
        #phone = r
        #phone = format_phone(r)
        #if len(phone) == 12:
        #    for i in range(1, 11):
        #        phone = phone.replace("+7", "8")
        #await state.update_data(phone=phone)
    data = await state.get_data()
    sql = "select count(name)+1 from tabTask "
    cur.execute(sql)
    answerDb = cur.fetchall()
    sql = "INSERT INTO tabTask (name, subject, project, creation, owner, status) VALUES (%s, %s, %s, %s, %s, 'Open')"
    count_task = "TASK-2021-" + str(answerDb[0][0])
    mas.append(count_task)
    mas.append(data.get("guest_name") + " " + data.get("phone"))
    mas.append("Добавить гостя")
    mas.append(str(datetime.datetime.now()))
    mas.append(customer)
    cur.execute(sql, mas)
    conn.commit()
    await message.answer("Гость успешно добавлен", reply_markup=menu_customer)
    await user_status.logined.set()
    #else:
    #    await message.answer("Неверный формат номера телефона. Пожалуйста, введите номер правильно.")
    #    await add_guest.get_phone.set()

