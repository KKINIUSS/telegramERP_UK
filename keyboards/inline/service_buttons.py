from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_service import service_callback
from database.connect_db import conn

cur = conn.cursor()
cur.execute("SELECT name FROM tabProject;")
str = cur.fetchall()

services = []
a = []
for i  in range (len(str)):
    a.append(str[i][0])
print(a)

for i in range (len(a)):
    b = []
    b.append(InlineKeyboardButton(text=(a[i]), callback_data=service_callback.new(name=a[i])))
    services.append(b)
service_buttons = InlineKeyboardMarkup(
    inline_keyboard=services
)

#InlineKeyboardButton(text="Добавить гостя", callback_data=service_callback.new(name="guests"))