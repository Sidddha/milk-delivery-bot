import typing

from aiogram.dispatcher.filters import BoundFilter
from tgbot.utils.db_api import db_commands as db


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        try:
            user = await db.select_user(id=obj.from_user.id)
            if user.status is None:
                return False
            else:
                print(f"========== status = {user.status}")
                if user.status== "ADMIN":
                    return self.is_admin
        except AttributeError:
            pass