from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from tgbot.utils.db_api.user import User
from tgbot.utils.db_api import db_commands



class GetDBUser(BaseMiddleware):
    """ 
    Перехватывает сообщение и возвращает данные пользователя из бд. 
    Если пользователь не обнаружен добавляет в бд с пометкой 'UNKNOWN_USER'
    """
    async def on_process_message(self, message: types.Message, data: dict):
        user = await db_commands.select_user(id=message.from_user.id)
        if user is None:
            await db_commands.add_user(id=message.from_user.id,
                                       name=message.from_user.first_name)
            user = await db_commands.select_user(id=message.from_user.id)           
        data["user"] = User(id=user.id, name=user.name, status=user.status)

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        user = await db_commands.select_user(id=cq.from_user.id)
        if user is None:
            await db_commands.add_user(id=cq.from_user.id,
                                       name=cq.from_user.full_name)
            user = await db_commands.select_user(id=cq.from_user.id)
        data["user"] = User(id=user.id, name=user.name, status=user.status)
