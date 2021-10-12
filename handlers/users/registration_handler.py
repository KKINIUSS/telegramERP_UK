from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline.reg_buttons import end_reg
from loader import dp
from states.registration import registration as reg
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel
from keyboards.default import menu
from data.config import location_site as loc
from datetime import datetime
import re
from utils.format import format_phone
import mariadb
from data.config import user, password, host, port, database
mes = ''

@dp.message_handler(text="Зарегистрироваться", state=reg.start)
async def enter_reg(message: Message):
    await message.answer(f"Вы выбрали {message.text}", reply_markup=ReplyKeyboardRemove())
    await message.answer("Введите ФИО")
    await reg.fio.set()


@dp.message_handler(state=reg.fio)
async def reg_fio(message: Message, state: FSMContext):
    pattern = r'[а-яА-ЯёЁ]+'
    if re.match(pattern, message.text):
        fio = message.text
        markup = ReplyKeyboardMarkup(resize_keyboard=False).add(KeyboardButton('Нажмите по кнопке, чтобы отправить свой номер телефона',
                           request_contact=True))
        await message.answer("Нажмите на кнопку, чтобы отправить свой номер телефона", reply_markup=markup)
        await state.update_data(fio=fio)
        await state.update_data(telegramid=message.from_user.id)
        await reg.phone.set()
    else:
        await message.answer("Невеный формат\nПожалуйста, вводите ФИО без цифр и только русскими буквами")
        await reg.fio.set()


@dp.message_handler(state=reg.phone, content_types=["contact"])
async def reg_phone(message: Message, state: FSMContext):
    r = message.text
    pattern = r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})'
    phone = message.contact.phone_number
    await message.answer("Введите адрес", reply_markup=ReplyKeyboardRemove())
    await state.update_data(phone=phone)
    await reg.address.set()


@dp.message_handler(state=reg.address)
async def reg_address(message: Message, state: FSMContext):
    address = message.text
    await message.answer("Отправьте 3 страницу паспорта")
    await state.update_data(address=address)
    await state.update_data(telegram_id=message.from_user.id)
    await reg.passport.set()


@dp.message_handler(state=reg.passport, content_types=['photo'])
async def reg_passport(message, state: FSMContext):
    passport = message.photo[-1]
    await passport.download(destination=loc + "passport_" + str(message.from_user.id) + ".jpg")
    await state.update_data(path_pas="/files/passport_" + str(message.from_user.id) + ".jpg")
    data = await state.get_data()
    await message.answer("Пожалуйста, проверте верна ли введеная информация\n"\
                        "ФИО: " + data.get("fio") + "\n"
                        "Номер телефона: " + data.get("phone") + "\n"\
                        "Адрес: " + data.get("address") + "\n", reply_markup=end_reg)
    await reg.check.set()


@dp.callback_query_handler(text_contains="reg", state=reg.check)
async def reg_check(call: CallbackQuery, state: FSMContext):
    conn = mariadb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    cur = conn.cursor()
    now = datetime.now()
    callback_data = call.data
    data = await state.get_data()
    if callback_data == "reg:True":
        await call.message.answer("Ваша заявка отправлена на рассмотрение оператором", reply_markup=menu)
        mas = [data.get("telegram_id"), now, "Administrator", "На рассмотрении", data.get("fio"), data.get("phone"),
               data.get("address"), data.get("path_pas"), call.from_user.id]
        cur.execute("INSERT INTO tabTelegramUsers "
                    "(name ,creation ,owner ,status ,full_name , phone, location, passport_image, telegramid) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", mas)
        conn.commit()
        conn.close()
        await state.finish()
    else:
        await call.message.answer("Начнём сначала! Введите ФИО.\n")
        conn.close()
        await reg.fio.set()
