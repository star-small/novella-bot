from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes, Message
from miscs.table import Products
import time
import traceback

API_TOKEN = "5862595528:AAFr3V90pCsGr0OvQ_5mggEJLrOfA7WaTtM"
CHANNEL_ID = "-1001884390827"
PATH_TO_IMAGE = "/home/troy/Projects/work/novella-bot/app/media/"
FILE_PATH = "/home/troy/Projects/work/novella-bot/app/files/test1.xlsx"
admins = ["eukalyptusbonb0n", "Shahid228322", "Shk_turdiev", "novella_electric"]


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["post"])
async def post(message: types.Message):
    if message.from_user.username in admins:
        try:
            products = Products()
            products.load_products(FILE_PATH)  # Загрузка товаров из файла
            post_count = len(products.get_products())
            status_message = await message.answer(f"Отправка продуктов: {post_count}")

            for product in products.get_products():
                post_count = post_count - 1
                img = open(PATH_TO_IMAGE + f"{product.image}", "rb")
                await bot.send_photo(
                    CHANNEL_ID, img, caption=product.get_message_text()
                )
                time.sleep(3)  # 15 min
                await status_message.edit_text(f"Отправка продуктов: {post_count}")
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
        if document := message.document:
            await document.download(
                destination_file="files/test1.xlsx",
            )
            await message.answer("Файл загружен")
    else:
        await message.answer("Вход воспрещён")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
