from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bac_service_menu = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Выйти в меню жителя ЖК")
    ]],
    resize_keyboard=True
)