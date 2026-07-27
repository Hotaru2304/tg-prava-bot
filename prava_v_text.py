import os
import telebot
import easyocr

# Бот забирает токен из настроек хостинга Bothost
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

print("Инициализация распознавателя текста...")
# Параметр download_enabled=True заставит хостинг один раз скачать нужные файлы при сборке
reader = easyocr.Reader(['ru', 'en'], download_enabled=True)
print("Бот успешно запущен и готов к обработке фотографий!")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне четкую фотографию водительского удостоверения, и я извлечу из него текст.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        status_msg = bot.reply_to(message, "Скачиваю фото и начинаю распознавание. Пожалуйста, подождите...")

        # Получаем файл с самым большим разрешением
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Временное имя файла для каждого пользователя
        image_path = f"tmp_{message.chat.id}.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Распознаем текст с помощью EasyOCR
        result = reader.readtext(image_path, detail=0)

        # Сразу удаляем временный файл с диска сервера
        if os.path.exists(image_path):
            os.remove(image_path)

        if result:
            extracted_text = "\n".join(result)
            response = (
                f"📝 **Распознанный текст:**\n\n"
                f"{extracted_text}\n\n"
                f"⚠️ _Перепроверьте результат вручную._"
            )
            bot.edit_message_text(response, message.chat.id, status_msg.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ Не удалось найти разборчивый текст на изображении. Попробуйте сделать фото при лучшем освещении.", message.chat.id, status_msg.message_id)

    except Exception as e:
        print(f"Ошибка в процессе обработки: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке фото. Попробуйте еще раз.")

if __name__ == '__main__':
    bot.infinity_polling()
