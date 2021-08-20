from subprocess import Popen
from aiogram import executor
from loader import dp
from database.connect_db import set_wait_time, cur
from data.config import location_bot as loc
import middlewares, filters, handlers, database
from utils.notify_admins import on_startup_notify
from utils.notify_users import on_startup_notify_users

async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    await on_startup_notify_users(dispatcher)
    Popen(["python3", loc + '/feedback.py'])
    Popen(["python3", loc + '/archive.py'])
    set_wait_time(cur)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)