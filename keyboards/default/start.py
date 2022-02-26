from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def start_defaultKB() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                KeyboardButton(text="/get_brand"),
                KeyboardButton(text="/get_title")
            ]
        ]
    )
    return keyboard