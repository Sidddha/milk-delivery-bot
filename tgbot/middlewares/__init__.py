from aiogram import Dispatcher

from .throttling import ThrottledMiddleware
from .database import GetDBUser


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottledMiddleware())
    dp.middleware.setup(GetDBUser())
