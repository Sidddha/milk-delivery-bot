from aiogram import Dispatcher, types


async def help(message: types.Message):
    await message.answer("Через этот бот вы можете заказать доставку молочной продукции. У нас широкий ассортимент и всегда свежий и натуральный товар.\n"
                    "Доставка осуществляется два раза в неделю в среду и субботу.\n"
                    "Чтобы сделать заказ нажмите /start\n"
                    "Если вы администратор нажмите /admin_login")
    
def register_help(dp: Dispatcher):
    dp.register_message_handler(help, commands="help", state="*")