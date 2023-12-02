from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.fsm.state import State, StatesGroup


class UserFilter(StatesGroup):
    search_query = State()
    genre_name = State()
    country = State()
    year = State()
    

async def set_main_menu(bot: Bot):
    commands = {
        '/start': 'Перезапуск бота',
        '/cancel': 'Остановить текущее состаяние бота',
        '/filtermovie': 'Фильтрация фильмов в Кинопоиске',
        '/searchmovie': 'Поиск фильма по еазванию',
        '/gpt': 'Использование Chat GPT 3.5 turbo',
    }
    main_menu = [
        BotCommand(
            command=command,
            description=description,
        )
        for command, description in commands.items()
    ]
    await bot.set_my_commands(main_menu)