from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def keyboard_constructor(*buttons):
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        text = button["text"]
        callback_data = button["callback_data"]
        keyboard.add(InlineKeyboardButton(text, callback_data=callback_data))
    return keyboard