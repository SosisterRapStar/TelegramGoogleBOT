import os
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.auth import AuthenticationError
from aiogram.types import InputFile

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.filters.command import Command
from aiogram import F


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token='YOU can import it from env') # мне было лень делать отдельный env файл
# Диспетчер
dp = Dispatcher()

pathForPhoto = "C:\/Users\/User\PycharmProjects\pythonProject\CreateFileBot\TelegramPhoto.jpg"
#Эм это типа промежуточного сохранения фотки или типа того до того как отправить ей на гугл


h = 0

@dp.message(F.photo)
async def download_photo(message: types.Message, bot: Bot):
    print(message.photo[-1].__dict__)

    await bot.download(
        message.photo[-1],
        destination=pathForPhoto
    )
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажмите для загрузки изображения",
        callback_data="photoDownLoader")
    )
    await message.reply("SizeOf:" + f"|{str(message.photo[-1].file_size)}|" + "bytes", reply_markup=builder.as_markup())




@dp.callback_query(Text("photoDownLoader"))
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(creat_file_in_drive(pathForPhoto))
@dp.callback_query(Text("fileDownLoader"))
async def send_random_value(callback: types.CallbackQuery):
    name = callback.message.reply_to_message.document.file_name
    await callback.message.answer(creat_document_in_drive(name))

gauth = None
@dp.message(F.document)
async def send_file(message: types.Message, bot: Bot):

    await bot.download(
        message.document,
        destination=universalPath + message.document.file_name
    )
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажмите для загрузки файла",
        callback_data="fileDownLoader")
    )
    await message.reply(f"{message.document.file_name}", reply_markup=builder.as_markup())




universalPath = "C:\/Users\/User\PycharmProjects\pythonProject\CreateFileBot\/"


def creat_document_in_drive(Document: str):
    global gauth
    if not gauth:
        gauth = GoogleAuth()
        try:
            gauth.LocalWebserverAuth()
        except AuthenticationError:
            print('Произошла ошибка авторизации. Убедитесь, что вы ввели правильный логин и пароль.')
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({"title": f"{Document}"})
    file.SetContentFile(Document)
    file.Upload()
    return "Файл загружен"


def creat_file_in_drive(Photo: str):
    global gauth
    if not gauth:
        gauth = GoogleAuth()
        try:
            gauth.LocalWebserverAuth()
        except AuthenticationError:
            print('Произошла ошибка авторизации. Убедитесь, что вы ввели правильный логин и пароль.')
    global h
    h += 1
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({"title": f"NewFileFromTelegram ({h}).jpg"})
    file.SetContentFile(Photo)
    file.Upload()
    return "Изображение загружено"






async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
