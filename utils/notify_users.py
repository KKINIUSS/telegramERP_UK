from aiogram import dispatcher
from database.connect_db import conn, cur
from aiogram import Dispatcher
from keyboards.default.menu import menu
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
async def on_startup_notify_users(dp:Dispatcher):
    text = "Бот был перезапущен, введите /start, чтобы продолжить."
    conn.commit()
    cur.execute("select name from tabTelegramUsers")
    data = cur.fetchall()
    btn = []
    btn.append([InlineKeyboardButton(text="Понятно", callback_data="Понятно")])
    bnt_inl = InlineKeyboardMarkup(
        inline_keyboard=btn,
    )
    for i in data:
        try:
            await dp.bot.send_message(i[0], text, reply_markup=bnt_inl)
        except:
            print("WARRING: user without telegramid")