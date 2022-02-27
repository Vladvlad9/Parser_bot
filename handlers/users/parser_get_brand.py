from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states.wb_parcer_get_article import WBState
from utils import WBParser


@dp.message_handler(commands=['get_brand'])
async def name_brand(message: types.Message):
    await message.answer(f"{message.from_user.full_name}, введи актикль")
    await WBState.next()


@dp.message_handler(state=WBState.name_article)
async def load_name(message: types.Message, state: FSMContext):
    await state.update_data(name_article=message.text)
    article = await state.get_data()
    result = await WBParser.get_response(str(article['name_article']))

    await message.answer(f"Название товара: {str(result['title'])}") if result else await message.answer(f"Товар не найден по введеному артиклю - {article}")

    await state.finish()
