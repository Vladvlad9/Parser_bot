from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("get_brand", "Название бренда."),
        types.BotCommand("get_title", "Название товара"),
        types.BotCommand("json_file", "Создание json file"),
    ])
