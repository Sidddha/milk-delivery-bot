from asyncpg import UniqueViolationError, UndefinedColumnError
from tgbot.utils.db_api.schemas.user import User
from tgbot.utils.db_api.db_gino import db


async def add_user(id: int, name: str, phone: int, address: str, geo: str, status: str = "UNKNOWN_USER"):
    try:
        user = User(id=id, name=name, phone=phone, addrsee=address, geo=geo, status=status)
        await user.create()
    except UniqueViolationError:
        print(f"User {name} already exist!")

async def select_all_users():
    # try:
    users = await User.query.gino.all()
    return users
    # except UndefinedColumnError:
async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user

async def update_status(id: int, status: str = "USER"):
    user = await User.get(id)
    await user.update(status=status).apply()

async def get_admins():
    admins = await User.query.where(User.status == "ADMIN").gino.all()
    return admins
