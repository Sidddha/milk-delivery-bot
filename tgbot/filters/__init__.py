from .is_admin import AdminFilter
from .is_user import UserFilter
from aiogram import Dispatcher


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(UserFilter)
