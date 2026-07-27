import os
import telebot
import easyocr
from PIL import Image

import os
import telebot

# Бот сам заберет токен из настроек хостинга, которые вы ввели на сайте
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


print("Запуск распознавателя текста (это может занять время в первый раз)...")
reader = easyocr.Reader(['ru', 'en'])
print("Бот успешно запущен и готов к работе!")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне четкую фотографию водительского удостоверения, и я постараюсь извлечь из него текст.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Отправляем статус, что бот обрабатывает изображение
        bot.send_chat_action(message.chat.id, 'typing')
        status_msg = bot.reply_to(message, "Скачиваю фото и начинаю распознавание. Пожалуйста, подождите...")

        # Получаем id файла с самым большим разрешением
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем временное изображение
        image_path = f"tmp_{message.chat.id}.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Распознаем текст с помощью EasyOCR
        result = reader.readtext(image_path, detail=0)

        # Удаляем временный файл с диска
        if os.path.exists(image_path):
            os.remove(image_path)

        # Формируем и отправляем ответ
        if result:
            # Соединяем строки в единый понятный текст
            extracted_text = "\n".join(result)
            
            response = (
                f"📝 **Распознанный текст:**\n\n"
                f"{extracted_text}\n\n"
                f"⚠️ _Внимание: OCR-системы могут допускать ошибки в буквах и цифрах, перепроверьте результат вручную._"
            )
            bot.edit_message_text(response, message.chat.id, status_msg.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ Не удалось найти разборчивый текст на изображении. Попробуйте сделать фото при лучшем освещении.", message.chat.id, status_msg.message_id)

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке фото. Убедитесь, что файл является корректным изображением.")

if __name__ == '__main__':
    bot.infinity_polling()
