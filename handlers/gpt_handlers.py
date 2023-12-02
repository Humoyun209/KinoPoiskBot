from openai import AsyncOpenAI

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from environs import Env


router = Router()


class GPTState(StatesGroup):
    gpt_state = State()


env = Env()
env.read_env()

client = AsyncOpenAI(api_key=env.str("GPT_KEY"))


@router.message(Command(commands=["gpt"]), StateFilter(default_state))
async def start_with_gpt(message: Message, state: FSMContext):
    await state.set_state(GPTState.gpt_state)
    await message.answer(
        "Здравствуйте! <b><i>Я Chat GPT</i></b>\n\nЧто вас интересует?\n\nДля возврашения в началное состаяние отправьте /cancel",
        parse_mode="HTML",
    )


@router.message(StateFilter(GPTState.gpt_state))
async def process_with_gpt(message: Message):
    stream = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message.text
            }
        ],
        model="gpt-3.5-turbo",
        stream=True,
    )
    sent_msg = await message.answer("Вот ваш ответь: \n\n")
    result = "Вот ваш ответь: \n\n"
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer = chunk.choices[0].delta.content
            result += answer
        try:
            await sent_msg.edit_text(result)
        except Exception as e:
            pass
    
    await message.answer("Для возврашения в началное состаяние отправьте /cancel")






