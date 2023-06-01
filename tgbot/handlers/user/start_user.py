from aiogram import Dispatcher, types
from tgbot.utils.db_api.user import User
from tgbot.misc.throttling import rate_limit


@rate_limit(limit=1)
async def start(message: types.Message, user: User):
    await message.answer(f"Привет, {user.name}\n"
                        f"Здесь будет стандартное меню пользователя")


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*", is_user=True)


