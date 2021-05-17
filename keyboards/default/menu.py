from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Войти"), KeyboardButton(text="Зарегистрироваться"),
        ],
    ],
    resize_keyboard=True
)

