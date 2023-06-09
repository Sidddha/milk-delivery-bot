from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.utils.db_api.user import User
from aiogram.dispatcher.storage import FSMContext
from tgbot.misc.states import NewUser
from loader import bot, config
from tgbot.utils.db_api import db_commands 
from tgbot.keyboards import callback_datas, registration_keyboard
from tgbot.keyboards.registration_keyboard import registration_callback

db = db_commands
btn = registration_keyboard.Button
callback = callback_datas.order_callback

async def start_unknown(message: types.Message, user: User, state: FSMContext):
    """ Вызывается если пользователь неизвестен. """
    await message.answer(f"Здравствуйте, {user.name}. Похоже вы здесь впервые. Для того чтобы сделать заказ укажите ваш номер телефона и адрес для доставки.",
                         reply_markup=btn.request_phone_number)
    await state.reset_state(with_data=False)
    async with state.proxy() as data:
        data["phone"] = 0
        data["address"] = 0
        data["geo"] = 0

async def get_phone_number(cq: types.CallbackQuery, state: FSMContext, phone: types.ContentType.CONTACT):
    await cq.answer()
    data = await state.get_data()   
    data["phone"] = phone
    await state.update_data(data=data, kwargs="phone")
    await types.Message.answer(f"Хорошо, теперь напишите ваш адрес или просто поделитесь геолокацией.", 
                               reply_markup=btn.request_geo)
    await NewUser.address.set()




new_order_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Новый заказ", callback_data=callback.new(order="new_order"))
        ]
    ]
) 


async def get_geo(cq: types.CallbackQuery, state: FSMContext, geo: types.ContentType.LOCATION):
    await cq.answer()
    data = await state.get_data()   
    data["geo"] = geo
    await state.update_data(data=data, kwargs="geo")  
    await state.reset_state(with_data=False)
  
    await bot.send_message(chat_id=cq.message.chat.id, text=f"Спасибо! Теперь вы можете сделать заказ.", 
                               reply_markup=new_order_keyboard)    
    await db.add_user(id=cq.from_user.id, name=cq.from_user.username, phone=data["phone"], address=data["address"], geo=data["geo"], status="USER")

async def get_address(message: types.Message, state: FSMContext):
    data = await state.get_data()   
    data["address"] = message.text
    await state.update_data(data=data, kwargs="address")  
    await state.reset_state(with_data=False)
  
    await message.answer(f"Спасибо! Теперь вы можете сделать заказ.", 
                               reply_markup=new_order_keyboard)    
    await db.add_user(id=message.from_user.id, name=message.from_user.username, phone=data["phone"], address=data["address"], geo=data["geo"], status="USER")


def register_unknown(dp: Dispatcher):
    dp.register_message_handler(start_unknown, commands=["start"], state="*")
    dp.register_callback_query_handler(get_phone_number, registration_callback.filter(reg="request_phone_number"), state="*")
    dp.register_callback_query_handler(get_geo, registration_callback.filter(reg="request_geo"), state="*")
    dp.register_message_handler(get_address, state=NewUser.address)

