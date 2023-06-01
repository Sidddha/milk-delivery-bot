from aiogram.dispatcher.filters import BoundFilter

import typing

from tgbot.utils.db_api import db_commands as db

class UserFilter(BoundFilter):
    key = 'is_user'

    def __init__(self, is_user: typing.Optional[bool] = None):
        self.is_user = is_user

    async def check(self, obj):
        try:
            user = await db.select_user(id=obj.from_user.id)
            if user.status is None:
                return False
            else:
                print(f"========== status = {user.status}")
                if user.status == "USER":
                    return self.is_user
        except AttributeError:
            pass