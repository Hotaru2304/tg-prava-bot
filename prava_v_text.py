import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
import easyocr

# Сюда вставьте токен вашего бота в кавычках
TOKEN = '8709476791:AAGW4u0nk0I3v7StyYAHq1RsvBTAGZzcxec'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Включаем читалку текста (для русского и английского языков)
reader = easyocr.Reader(['ru', 'en'], gpu=False)

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    # Бот пишет, что начал читать картинку
    status_msg = await message.answer("⏳ Вижу фото. Читаю текст...")

    # Скачиваем фотку к себе на сервер
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    temp_path = f"photo_{photo.file_id}.jpg"
    await bot.download_file(file_info.file_path, temp_path)

    # Нейросеть считывает буквы с картинки
    result = reader.readtext(temp_path, detail=0)

    # Удаляем скачанную фотку, чтобы не засорять сервер
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Собираем все строчки текста вместе
    recognized_text = "\n".join(result)

    if not recognized_text:
        await status_msg.edit_text("❌ Не смог разобрать буквы. Сделайте фото почетче.")
    else:
        await status_msg.edit_text(f"📋 Вот что удалось прочитать:\n\n{recognized_text}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
