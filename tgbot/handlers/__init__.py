from .start_unknown import register_unknown
from .user.start_user import register_user
from .admin.start_admin import register_admin
from .errors import register_errors
from .admin.register_new_user import register_new_user
from .help import register_help
from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user(dp)
    register_unknown(dp)
    register_new_user(dp)
    register_help(dp)
    register_errors(dp)
