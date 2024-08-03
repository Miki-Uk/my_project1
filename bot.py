import asyncio
import logging
import sys
from config import BOT_TOKEN as TOKEN
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import Message
from commands import FILMS_COMMAND
from keyboards import films_keyboard_markup, FilmCallback
from aiogram.types import Message, CallbackQuery
from models import Film
from aiogram.types import URLInputFile
from data import get_films
from keyboards import films_keyboard_markup
from commands import (
    FILMS_COMMAND,
    START_COMMAND,
    FILMS_BOT_COMMAND,
    START_BOT_COMMAND,
)



dp = Dispatcher()






@dp.message(Command("start"))
async def start(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        f"Перелік фільмів. Натисніть на назву фільму для отримання деталей.",
        reply_markup=markup
    )



    await message.answer(
            text="Some text",
            reply_markup=markup
    )




@dp.message(FILMS_COMMAND)
async def films(message: Message) -> None:
    data = get_films()
    markup = films_keyboard_markup(films_list=data)
    await message.answer(
        f"Перелік фільмів. Натисніть на назву фільму для отримання деталей.",
        reply_markup=markup
    )



async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await bot.set_my_commands(
        [
            FILMS_BOT_COMMAND,
            START_BOT_COMMAND,
        ]
    )

# @dp.callback_query(FilmCallback.filter())
# async def callb_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
#     await callback.message.answer(text=f"{callback_data=}")



@dp.callback_query(FilmCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    film_id = callback_data.id
    film_data = get_films(film_id=film_id)
    film = Film(**film_data)


    text = f"Фільм: {film.name}\n" \
           f"Опис: {film.description}\n" \
           f"Рейтинг: {film.rating}\n" \
           f"Жанр: {film.genre}\n" \
           f"Актори: {', '.join(film.actors)}\n"
   
    await callback.message.answer_photo(
        caption=text,
        photo=URLInputFile(
            film.poster,
            filename=f"{film.name}_poster.{film.poster.split('.')[-1]}"
        )
    )













async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())