import openai

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackGame
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from environs import Env


router = Router()

class GPTState(StatesGroup):
    gpt_state = State()

env = Env()
env.read_env()

openai.api_key = env.str('GPT_KEY')


@router.message(Command(commands=['gpt']), StateFilter(default_state))
async def start_with_gpt(message: Message, state: FSMContext):
    await state.set_state(GPTState.gpt_state)
    await message.answer('Здравствуйте! <b><i>Я Chat GPT</i></b>\n\nЧто вас интересует?\n\nДля возврашения в началное состаяние отправьте /cancel',
                         parse_mode='HTML')
    

@router.message(StateFilter(GPTState.gpt_state))
async def process_with_gpt(message: Message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message.text,
        max_tokens=1000,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    generated_text = response.choices[0].text.strip()

    await message.reply(generated_text)
    await message.answer('Для возврашения в началное состаяние отправьте /cancel')
