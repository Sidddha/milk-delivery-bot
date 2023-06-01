from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminLogin(StatesGroup):
    password = State()
    request = State()
    attempts_limit = State()

class NewUser(StatesGroup):
    address = State()
