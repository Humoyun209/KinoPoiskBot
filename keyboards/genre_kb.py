from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


genre_1 = InlineKeyboardButton(text="🥷 Криминал", callback_data="genre:криминал")
genre_2 = InlineKeyboardButton(text="🌄 Фантастик", callback_data="genre:фантастик")
genre_3 = InlineKeyboardButton(text="😁 Комедия", callback_data="genre:комедия")
genre_4 = InlineKeyboardButton(text="❤️ Мелодрама", callback_data="genre:мелодрама")

genre_keyboard = InlineKeyboardMarkup(inline_keyboard=[[genre_1, genre_2], [genre_3, genre_4]])