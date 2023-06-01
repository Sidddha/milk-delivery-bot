from aiogram import types, Dispatcher

async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начать"),
        types.BotCommand("help", "Нужна помощь?"),
        types.BotCommand("admin_login", "Войти как администратор")
    ]) 