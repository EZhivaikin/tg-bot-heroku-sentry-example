import os

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
import sentry_sdk


bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

sentry_sdk.init(
    os.getenv("SENTRY"),
    traces_sample_rate=1.0
)


async def async_request(url, method, data=None, params=None, headers=None):
    async with aiohttp.request(method=method, url=url, params=params, data=data, headers=headers) as response:
        result = await response.json()
    return result


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Дай кота")
    keyboard.add(button_1)
    return keyboard


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    print(message.text)
    await message.answer("Привет!👋 Это бот для рандомных котиков!", reply_markup=get_keyboard())


@dp.message_handler(Text(equals="Дай кота"))
async def get_cat(message: types.Message):
    cat_image = await async_request("https://api.thecatapi.com/v1/images/search", "GET")
    await message.answer_photo(cat_image[0]["url"])


@dp.message_handler(commands=["get_error"])
async def get_error(message: types.Message):
    raise RuntimeError


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)