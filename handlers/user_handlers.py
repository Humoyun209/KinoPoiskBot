from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from fsm import UserFilter
from db.models import Movie
from db.database import DataBase
from kinopoisk.api import KinoPoiskAPI

from keyboards.genre_kb import genre_keyboard
from keyboards.country_kb import counry_keyboard
from keyboards.movie_url_kb import get_movie_kb

from environs import Env


env = Env()
env.read_env()
router = Router()
db = DataBase("app/db.sqlite3")
api = KinoPoiskAPI(token=env.str("KINOPOISK_TOKEN"))


async def output_movies(message: Message, result: list[Movie], path_name: str):
    for movie in result:
        file_name = await api.download_image(movie.post_image_url, path_name)
        await message.answer_photo(
            photo=FSInputFile(f"app/images/{path_name}/{file_name}"),
            caption=f'<b>Имя:</b> {movie.name} ({movie.alternativeName})\n<b>Описание:</b> {movie.description[:150]}...\n<b>Рейтинг в кинопоиске: </b>{movie.rating_kp} / 10\n<b>Рейтинг в IMDB: </b>{movie.rating_imdb} / 10',
            parse_mode='HTML',
            reply_markup=get_movie_kb(movie.preview_url)
        )


@router.message(Command(commands=["start"]))
async def process_start(message: Message):
    await db.create_user(message.from_user.id, message.from_user.username)
    await message.answer("User is created")
    

@router.message(Command(commands=["cancel"]), ~StateFilter(default_state))
async def process_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Текуший процесс остановлен")


@router.message(Command(commands=["getMe"]))
async def get_me(message: Message):
    user_id, username = await db.get_me(message.from_user.id)
    await message.answer(
        f"<b>Your id:</b> {user_id}\n<b>Your username:</b> {username}",
        parse_mode="HTML",
    )


@router.message(Command(commands=["filtermovie"]), StateFilter(default_state))
async def find_movie(message: Message, state: FSMContext):
    await message.answer("Вы можете получить  5 высокорейтинговых фильмов в Кинопоиске \n\n<b><i>Выберите джанр:</i></b> ",
                         parse_mode='HTML',
                         reply_markup=genre_keyboard)
    await state.set_state(UserFilter.genre_name)
    

@router.message(Command(commands=["filtermovie"]), ~StateFilter(default_state))
async def find_movie(message: Message, state: FSMContext):
    await message.answer("Вы сейчас не можете фильтровать фильмы 😐\nЕсли хотите остановить процесс /cancel" )
    

@router.callback_query(StateFilter(UserFilter.genre_name), F.data.startswith('genre:'))
async def get_genre(cb: CallbackQuery, state: FSMContext):
    genre: str = cb.data.split(":")[1]
    if genre != 'skip':
        await state.update_data(**{'genre': genre})
    await state.set_state(UserFilter.year)
    await cb.message.answer('Отлично ✅, \n\nтепер введите год фильма (Если имеется, если нет пишите "skip")\nЗначение может быть 1945-2023')
    await cb.message.delete()
    

@router.message(StateFilter(UserFilter.year), lambda msg: (msg.text.isdigit() and 1945 < int(msg.text) <= 2023) or msg.text == "skip")
async def get_year(message: Message, state: FSMContext):
    if message.text != "skip":
        await state.update_data(**{"year": message.text})
    await state.set_state(UserFilter.country)
    await message.answer("Пожалуйста, выберите страна фильма \n(Если не имеется, нажмите на skip)",
                         reply_markup=counry_keyboard)


@router.callback_query(StateFilter(UserFilter.country), F.data.startswith('country:'))
async def get_result(cb: CallbackQuery, state: FSMContext):
    await state.update_data(**{"country": cb.data.split(":")[1]})
    filters = await state.get_data()
    await state.set_state(default_state)
    result: list[Movie] = await api.filter_movie(**filters)
    path_name = '_'.join(filters.values())
    await output_movies(cb.message, result, path_name)


@router.message(Command(commands=['/search']), StateFilter(default_state))
async def process_search(message: Message, state: FSMContext):
    await state.set_state(UserFilter.search_query)
    await message.answer("Введите ключевое слово фильма или сериала, который вам нужен\n\nОстановить текущий процесс /cancel")


@router.message(StateFilter(UserFilter.search_query))
async def get_movies_by_query(message: Message, state: FSMContext):
    await state.set_state(default_state)
    result: list[Movie] = await api.search_movie(message.text)
    path_name = f'query_{message.text}'
    await output_movies(message, result, path_name)