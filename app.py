from subprocess import Popen
from aiogram import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, bot
from data.config import location_bot as loc
import middlewares, filters, handlers, database
from utils.notify_admins import on_startup_notify
import mariadb
from data.config import user, password, host, port, database
import sqlite3
import asyncio
from utils.notify_users import on_startup_notify_users
btn = []
btn.append([InlineKeyboardButton(text="Понятно", callback_data="Понятно")])
bnt_inl = InlineKeyboardMarkup(
    inline_keyboard=btn,
)



async def notify():
    while True:
        connSql3 = sqlite3.connect("buffer.db")
        curSql3 = connSql3.cursor()
        curSql3.execute("create table if not exists tabTelegramUsers (name text, status text,telegramidforeman text)")
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        cur = conn.cursor()
#        print("Ищу обновления))")
        cur.execute("select name, status from tabTelegramUsers")
        for name, status in cur:
            curSql3.execute("select * from tabTelegramUsers where name=?", [name])
            a = curSql3.fetchall()
            if(a):
                for nameBuf, statusBuf in a:
                    if(nameBuf == name):
                        if(status != statusBuf):
                            if(status == 'Отклонен'):
                                curSql3.execute("delete from Employer where name=?", [name])
                                connSql3.commit()
                                await bot.send_message(name,text=f"Данные учётной записи не корректны, свяжитесь с администратором системы.", reply_markup=ReplyKeyboardRemove())
                            elif(status == 'Подтвержден'):
                                curSql3.execute("update tabTelegramUsers set status=? where name=?", [status, name])
                                connSql3.commit()
                                await bot.send_message(name, text=f"Ваша учетная запись подтверждена!", reply_markup=bnt_inl)
            else:
                print(f"Завожу чувака с данными - Name: {name}, Status: {status}, TeleID: {tlForeman}")
                curSql3.execute("insert into Employer (name, status, telegramidforeman) values (?, ?, ?)", [name, status, tlForeman])
                connSql3.commit()
        conn.close()
        await asyncio.sleep(10)




async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    asyncio.create_task(notify())
   # await on_startup_notify_users(dispatcher)
   # set_wait_time(cur)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)