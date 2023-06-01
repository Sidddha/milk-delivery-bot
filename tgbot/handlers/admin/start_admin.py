from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc.throttling import rate_limit

@rate_limit(limit=1)
async def admin_start(message: Message):
    await message.reply(f"Привет, {message.from_user.first_name}\n"
                        "Здесь будет расширенное меню администратора")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
