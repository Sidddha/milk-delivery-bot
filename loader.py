import asyncio.base_subprocess
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.utils.db_api.db_gino import db


logger = logging.getLogger(__name__)
# loop = asyncio.get_event_loop()
# db = Database(loop)
config = load_config(".env")
storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)


__all__ = ["bot", "storage", "dp", "db"]