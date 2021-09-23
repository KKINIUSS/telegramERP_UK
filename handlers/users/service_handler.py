import re
import datetime
from aiogram.types import Message, CallbackQuery
from keyboards.default.menu_customer import menu_customer
from loader import dp
from utils.format import format_phone
from states.service_state import choice_service as c_s, add_guest
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel
from states.login_at_user import user_status
import mariadb
from data.config import user, password, host, port, database
from keyboards.default.back_from_service import bac_service_menu

@dp.message_handler(text="Добавить гостя", state=user_status.logined)
async def add_geust(message: Message, state: FSMContext):
    await message.answer("Введите информацию о госте(ФИО, марку/номер машины)", reply_markup=bac_service_menu)
    await add_guest.get_name.set()

@dp.message_handler(state=add_guest.get_name)
async def get_name(message: Message, state: FSMContext):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    cur = conn.cursor()
    conn.commit()
    str_message = message.text
    if(str_message == 'Назад'):
        await message.answer("Нажмите 'Добавить гостя', чтобы выпустить пропуск.", reply_markup=menu_customer)
        conn.close()
        await user_status.logined.set()
    elif(len(str_message)>40):
        await message.answer("Невеный формат\nИнфорация о госте должна содержать не более 40 символов, повторите снова")
        await message.answer("Введите информацию о госте(ФИО, марку/номер машины)", reply_markup=bac_service_menu)
        conn.close()
        await add_guest.get_name.set()
    else:
        guest_name = message.text
        await state.update_data(guest_name=guest_name)
        cur.execute("select full_name from tabTelegramUsers where telegramid=?", [message.from_user.id])
        customers = cur.fetchall()
        customer = customers[0][0]
        data = await state.get_data()
        sql = "select count(name)+1 from tabTask"
        cur.execute(sql)
        answerDb = cur.fetchall()
        sql = "INSERT INTO tabTask (name, subject, creation, owner, status, exp_start_date, exp_end_date, modified) VALUES (%s, %s, %s, %s, 'Активен', %s, %s, %s)"
        count_task = "TASK-2021-" + str(answerDb[0][0])
        today = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        zavtra = today + delta
        mas = [count_task, data.get("guest_name"), today, customer, today, zavtra, today]
        cur.execute(sql, mas)
        conn.commit()
        await message.answer("Гость успешно добавлен", reply_markup=menu_customer)
        conn.close()
        await user_status.logined.set()

