# pip install aiogram
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

bot = Bot(token="2111527545:AAG8-aYEc0ul79vRkdWgp_dKcJIKIKXk098")

dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    print(message.text)
    await message.answer("Привет! Это бот для рандом котов!")


async def async_request(url, method, data=None, params=None, headers=None):
    async with aiohttp.request(method=method, url=url, params=params, data=data, headers=headers) as response:
        result = await response.json()
    return result


@dp.message_handler(Text(equals="Дай кота"))
async def get_cat(message: types.Message):
    cat_image = await async_request("https://api.thecatapi.com/v1/images/search", "GET")
    await message.answer_photo(cat_image[0]["url"])


@dp.message_handler(commands=["get_error"])
async def get_error(message: types.Message):
    raise RuntimeError

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
