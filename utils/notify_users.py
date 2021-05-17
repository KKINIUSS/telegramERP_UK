from aiogram import dispatcher
from database.connect_db import conn, cur
from aiogram import Dispatcher
from keyboards.default.menu import menu

async def on_startup_notify_users(dp:Dispatcher):
    text = "Пожалуйста войдите в аккаунт, нажав соответствующую кнопку"
    conn.commit()
    cur.execute("select name from tabTelegramUsers")
    data = cur.fetchall()
    cur.execute("select telegramid from tabEmployee")
    data += cur.fetchall()
    for i in data:
        try:
            await dp.bot.send_message(i[0], text, reply_markup=menu)
        except:
            print("WARRING: user without telegramid")