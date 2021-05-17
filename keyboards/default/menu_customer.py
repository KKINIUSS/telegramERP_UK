from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_customer = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Сделать запрос"),
        ],
        [
            KeyboardButton(text="Выйти"),
        ]
    ],
    resize_keyboard=True
)

