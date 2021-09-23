from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bac_service_menu = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Назад")
    ]],
    resize_keyboard=True
)