import asyncio
import datetime
import requests
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

from config import tg_bot_token, open_weather_token

bot = Bot(tg_bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привіт!  {message.from_user.full_name}\nНапиши мені назву міста і я надішлю зведення "
                         f"погоди!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )

        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивися у вікно, не зрозумію, що там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\nВітер: {wind} м/с\n"
                            f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\n"
                            f"Тривалість дня: {length_of_the_day}\n"f"***Гарного дня!***")

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
