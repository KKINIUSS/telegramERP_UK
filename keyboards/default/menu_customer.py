from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_customer = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить гостя"),
        ],
    ],
    resize_keyboard=True
)

