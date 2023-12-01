from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_movie_kb(preview_url: str) -> InlineKeyboardMarkup:
    url_btn = InlineKeyboardButton(text='Смотреть в кинопоиске', url=preview_url)
    movie_kb = InlineKeyboardMarkup(inline_keyboard=[[url_btn]])
    return movie_kb