from aiogram.dispatcher.filters.state import StatesGroup, State


class WBState(StatesGroup):
    name_article = State()