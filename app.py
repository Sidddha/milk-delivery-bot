import asyncio
import logging


from tgbot import filters
from tgbot import handlers
from tgbot.misc.set_bot_commands import set_default_commands
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot import middlewares
from loader import bot, logger, dp, db, config
from tgbot.utils.db_api import db_commands, db_gino


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    middlewares.setup(dp)


async def set_commands(dp):
    await set_default_commands(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    bot['config'] = config

    register_all_middlewares(dp, config)
    filters.register_all_filters(dp)
    handlers.register_handlers(dp)
    await set_commands(dp)
    await db.set_bind(config.db.url)
    await db_gino.on_startup(dp)
    await db.gino.create_all()
    await on_startup_notify(dp)

    # db.add_user(504168024, "Siddha", "USER")
    # db.update_status("ADMIN", 504168024)
    print(await db_commands.select_all_users())

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
