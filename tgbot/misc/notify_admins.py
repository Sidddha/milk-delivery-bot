import logging

from aiogram import Dispatcher
from tgbot.utils.db_api import db_commands


async def on_startup_notify(dp: Dispatcher):
        admins = await db_commands.get_admins()
        for admin in admins:
            try:
                await dp.bot.send_message(admin.id, "Бот запущен и готов к работе")
            except Exception as err:
                logging.exception(err)

