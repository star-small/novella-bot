from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes, Message
from miscs.table import Products
from dotenv import load_dotenv
import time
import asyncio
import traceback
import os


load_dotenv("/etc/environment")
API_TOKEN = os.getenv("API_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PATH_TO_IMAGE = os.getenv("PATH_TO_IMAGE")
FILE_PATH = os.getenv("FILE_PATH")
DELAY_MIN = int(os.getenv("DELAY_MIN"))
admins = ["eukalyptusbonb0n", "Shahid228322", "Shk_turdiev", "novella_electric"]
loop_completed = False
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["post", "stop"])
async def post(message: types.Message):
    if message.from_user.username in admins:
        global stop_requested, loop_completed
        if message.text == "/stop":
            stop_requested = True
            await message.answer("Отправка остановлена.")
            return
        else:
            stop_requested = False

        try:
            products = Products()
            products.load_products(FILE_PATH)  # Загрузка товаров из файла
            post_count = len(products.get_products())
            status_message = (
                await message.answer(
                    f"Отправка продуктов: {post_count}\nВведите /stop для остановки."
                )
                if message.text == "/post"
                else None
            )
            for product in products.get_products():
                if stop_requested:
                    break
                print(stop_requested)
                post_count = post_count - 1
                img = open(PATH_TO_IMAGE + f"{product.image}", "rb")
                await bot.send_photo(
                    CHANNEL_ID, img, caption=product.get_message_text()
                )

                await status_message.edit_text(
                    f"Отправка продуктов: {post_count}\nВведите /stop для остановки."
                )
                await asyncio.sleep(DELAY_MIN * 60)  # 15 min
            if not stop_requested:
                await message.answer("Отправка завершена")
        except BaseException as e:
            await message.answer(e)
    else:
        await message.answer("Вход воспрещен!")


@dp.message_handler(commands=["help", "start"])
async def show_help(message: Message):
    if message.from_user.username in admins:
        await message.answer(
            "Введите комманду /post для публикации постов из файла.\nЧтобы загрузить новый файл, просто отправьте его в этот чат.\nВведите /help для вызова сообщения помощи"
        )
    else:
        await message.answer("Вход воспрещён!")


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def doc_handler(message: Message):
    if message.from_user.username in admins:
        if message.document != None:
            await message.document.download(
                destination_file=FILE_PATH,
            )
            await message.answer("Файл загружен")
    else:
        await message.answer("Вход воспрещён")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
