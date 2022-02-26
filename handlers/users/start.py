import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

from keyboards.default.start import start_defaultKB
from loader import dp
from states.WBparcerGetArticle import WBState
from utils import wb_parser


class WBParser(object):
    @staticmethod
    async def get_result(html: str) -> dict:
        soup = bs(html, "lxml")
        return {
            "brand_name": soup.find(attrs={"data-link": "text{:product^brandName}"}).text,
            "title": soup.find(attrs={"data-link": "text{:product^goodsName}"}).text,
            "article": soup.find("span", id='productNmId').text,

        }

    @staticmethod
    async def get_response(article: str, is_json: bool = False) -> dict:
        url = f"https://wbx-content-v2.wbstatic.net/sellers/{article}.json" if is_json else f"https://www.wildberries.ru/catalog/{article}/detail.aspx?targetUrl=XS"
        async with ClientSession(headers={"UserAgent": UserAgent().random}).get(url) as response:
            if response.status == 200:
                if is_json:
                    return json.loads(await response.text())
                else:
                    return await WBParser.get_result(await response.text())
            else:
                return dict()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=await start_defaultKB())


@dp.message_handler(commands=['get_brand', 'get_title'])
async def name_brand(message: types.Message, state: FSMContext):
    await message.answer(f"{message.from_user.full_name}, введи актикль")
    async with state.proxy() as data:
        data['name_conamd'] = message.text
    await WBState.next()


@dp.message_handler(state=WBState.name_arcitle)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_arcitle'] = message.text
        name_conamd = data['name_conamd']

    article = data['name_arcitle']
    result = await WBParser.get_response(str(article))

    if not result:
        await message.answer(f"Товар не найден по введеному артиклю - {article}")
    else:
        if name_conamd == '/get_brand':
            await message.answer(f"Бренд: {str(result['brand_name'])}")
        else:
            await message.answer(f"Название товара: {str(result['title'])}")

    await state.finish()


@dp.message_handler(commands=['json_file'])
async def name_brand(message: types.Message, state: FSMContext):
    result = await WBParser.get_response(str(18409417), True)
    if result != '':
        with open("data_file.json", "w", encoding='utf-8') as write_file:
            json.dump(result, write_file, indent=3, ensure_ascii=False)
        await message.answer('Файл создан')

