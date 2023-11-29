from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


country_1 = InlineKeyboardButton(text="🇷🇺 Россия", callback_data="country:Россия")
country_2 = InlineKeyboardButton(text="🇺🇸 США", callback_data="country:США")
country_5 = InlineKeyboardButton(text="🇹🇷 Турция", callback_data="country:Турция")
country_3 = InlineKeyboardButton(text="🇬🇧 Великобритания", callback_data="country:Великобритания")
country_4 = InlineKeyboardButton(text="🇺🇿 Узбекистан", callback_data="country:Узбекистан")
skip = InlineKeyboardButton(text="Пропустить", callback_data="country:skip")

counry_keyboard = InlineKeyboardMarkup(inline_keyboard=[[country_1, country_2], [country_3, country_4], [country_5, skip]])