import re
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.utils.db_api.user import User
from tgbot.keyboards.registration_keyboard import registration_callback, Button
from tgbot.keyboards.keyboard_constructor import keyboard_constructor
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import AdminLogin
from loader import bot, config
from tgbot.utils.db_api import db_commands 
import datetime

btn = Button()

ATTEMPTS = 3 # Количество попыток ввода пароля
TIMEOUT = 30 # Таймаут после израсходования попыток


async def admin_login(message: types.Message, user: User, state: FSMContext):
    await message.answer(f"Харибол! Введите пароль  администратора.",
                         reply_markup=keyboard_constructor(btn.enter_password, btn.cancel))
    await state.reset_state(with_data=False)
    async with state.proxy() as data:
        data["attempts"] = 0
        data["time"] = 0


async def enter_password(cq: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """ Предлагает ввести пароль администратора. Пароль задается в .env """
    await cq.answer()
    await cq.message.edit_text("Введите пароль", reply_markup=keyboard_constructor(btn.cancel))
    await AdminLogin.password.set()


async def get_password(message: types.Message, state: FSMContext):
    """ Проверка пароля и назначение пользователя админом если пароль верный."""
    password = int(message.text)
    if password == config.tg_bot.admin_password:
        await db_commands.update_status(message.from_user.id, "ADMIN")
        await state.finish()
        await message.answer("Пароль принят! Вы вошли как администратор.\n"
                             "Для начала работы отправьте /start")
    else:
        data = await state.get_data()
        attempt = data.get("attempts")
        attempt = attempt + 1
        data["attempts"] = attempt
        await state.update_data(data=data, kwargs="attempts")
        if attempt > ATTEMPTS - 1:
            now = datetime.datetime.now()
            delta = now + datetime.timedelta(minutes=TIMEOUT)
            data["time"] = delta
            await state.update_data(data=data, kwargs=("time"))
            await message.answer("Все, хватит. Думаю ты не знаешь пароль",
                                 reply_markup=keyboard_constructor(btn.send_request, btn.cancel))
            await AdminLogin.attempts_limit.set()
            print(await state.get_state())
            print(data)
        elif attempt == ATTEMPTS - 1:
            await message.answer("Осталась последняя попытка", reply_markup=keyboard_constructor(btn.cancel))
            await AdminLogin.password.set()
        else:
            await message.answer(f"Неверный пароль. Осталось попыток: {ATTEMPTS-attempt}", reply_markup=keyboard_constructor(btn.cancel))
            await AdminLogin.password.set()

async def attempts_limit(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        print(data)
        time = data.get("time")
        print(time)
        now = datetime.datetime.now()
        now.minute
        time.minute
        print(time - now)
        if now >= time:
            await state.reset_data()
        else:
            remain = str(time - now)
            output = re.findall(r':[0-9]{2}:', remain)
            result = output[0][1:-1]
            print(result)
            await message.answer(f"Попробуйте еще через {result} минут.", reply_markup=keyboard_constructor(btn.debug))
    except:
        pass

async def cancel(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.edit_text(f"Введи пароль доступа или отправь запрос администратору")
    await cq.message.edit_reply_markup(keyboard_constructor(btn.enter_password, btn.send_request, btn.cancel))
    await cq.answer(text="Всего хорошего!", show_alert=True)
    await state.reset_state(with_data=False)


def register_unknown(dp: Dispatcher):
    dp.register_message_handler(admin_login, commands=["admin_login"], state="*")
    dp.register_message_handler(attempts_limit, state=AdminLogin.attempts_limit)
    dp.register_callback_query_handler(cancel, registration_callback.filter(reg="cancel"), state="*")
    dp.register_callback_query_handler(enter_password, registration_callback.filter(reg="enter_password"))
    dp.register_message_handler(get_password, state=AdminLogin.password)