from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_menu = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Вернуться в меню сотрудника")
    ]],
    resize_keyboard=True
)