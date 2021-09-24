from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_concierge = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список гостей"), KeyboardButton(text="Отправить сообщение охране")
        ],
        [
            KeyboardButton(text="Найти гостя"),
        ]
    ],
    resize_keyboard=True
)

