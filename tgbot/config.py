from dataclasses import dataclass

import asyncio
from environs import Env
from os import environ
import dotenv


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    url: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    admin_password: int


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            # admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            admin_password=env.int("ADMIN_PASSWORD")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASSWORD'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            url=env.str('POSTGRES_URI')
        ),
        misc=Miscellaneous()
    )


# def add_admin(id: str):
#     env = Env()
#     env.read_env()

#     # Get a list of admin IDs from the ADMINS variable in the environment
#     admin_ids_string = env.str("ADMINS", default="")
#     admin_ids = [] if admin_ids_string == "" else list(map(int, admin_ids_string.split(',')))

#     # Add the new admin ID to the list
#     admin_ids.append(id)

#     # Set the ADMINS variable to the updated list of admin IDs
#     admin_ids_string = ",".join(str(i) for i in admin_ids)
#     environ["ADMINS"] = admin_ids_string
#     env("ADMINS", admin_ids_string)
#     # Write the changes back to the .env file
#     dotenv_file = dotenv.find_dotenv()
#     dotenv.set_key(dotenv_file, "ADMINS", admin_ids_string)
#     db.update_status(status="ADMIN", id=id)

# def remove_admin(id):
#     env = Env()
#     env.read_env()

#     # Get a list of admin IDs from the ADMINS variable in the environment
#     admin_ids_string = env.str("ADMINS", default="")
#     admin_ids = [] if admin_ids_string == "" else list(map(int, admin_ids_string.split(',')))

#     # Add the new admin ID to the list
#     admin_ids.remove(id)

#     # Set the ADMINS variable to the updated list of admin IDs
#     admin_ids_string = ",".join(str(i) for i in admin_ids)
#     environ["ADMINS"] = admin_ids_string
#     env("ADMINS", admin_ids_string)
#     # Write the changes back to the .env file
#     dotenv_file = dotenv.find_dotenv()
#     dotenv.set_key(dotenv_file, "ADMINS", admin_ids_string)
#     db.update_status(status="ADMIN", id=id)



