from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

concierge_menu = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text="Найти гостя"), KeyboardButton(text="список гостей"),
    ],
    [
        KeyboardButton(text="отмена"),
    ]
],
    resize_keyboard=True
)