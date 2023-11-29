from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_file import FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from fsm import UserFilter
from db.models import Movie
from db.database import DataBase
from kinopoisk.api import KinoPoiskAPI
from environs import Env


env = Env()
env.read_env()
router = Router()
db = DataBase("app/db.sqlite3")
api = KinoPoiskAPI(token=env.str("KINOPOISK_TOKEN"))


@router.message(Command(commands=["start"]))
async def process_start(message: Message):
    await db.create_user(message.from_user.id, message.from_user.username)
    await message.answer("User is created")


@router.message(Command(commands=["getMe"]))
async def get_me(message: Message):
    user_id, username = await db.get_me(message.from_user.id)
    await message.answer(
        f"<b>Your id:</b> {user_id}\n<b>Your username:</b> {username}",
        parse_mode="HTML",
    )


@router.message(Command(commands=["findMovie"]))
async def find_movie(message: Message):
    await message.answer("Введите что-нибуд из имени фильма")


@router.message()
async def get_result(message: Message):
    result: list[Movie] = await api.search_movie(message.text)
    for movie in result:
        file_name = await api.download_image(movie.post_image_url, message.text)
        await message.answer_photo(
            photo=FSInputFile(f"app/images/{message.text}/{file_name}"),
            caption=f'<b>Имя:</b> {movie["name"]} ({movie["alternativeName"]})\n<b>Описание:</b> {movie["description"][:150]}...\n<b>Рейтинг в кинопоиске: </b>{movie["rating"]["kp"]} / 10',
            parse_mode='HTML'
        )
