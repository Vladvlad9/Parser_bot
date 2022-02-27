import json

from aiogram import types

from loader import dp
from utils import WBParser


@dp.message_handler(commands=['json_file'])
async def name_brand(message: types.Message):
    result = await WBParser.get_response(str(18409417), True)
    if result:
        with open("data_file.json", "w", encoding='utf-8') as write_file:
            json.dump(result, write_file, indent=3, ensure_ascii=False)
        await message.answer('Файл создан')