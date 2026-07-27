import os
import telebot
import requests

# Бот забирает токен из настроек хостинга Bothost
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

print("Запуск стабильного распознавателя прав...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне четкую фотографию водительского удостоверения, и я извлечу из него текст.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        status_msg = bot.reply_to(message, "Скачиваю фото и начинаю распознавание. Пожалуйста, подождите...")

        # Получаем файл
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Отправляем файл напрямую в бесплатный OCR движок
        files = {'file': ('image.jpg', downloaded_file, 'image/jpeg')}
        payload = {
            'apikey': 'K88446889388957',  # бесплатный универсальный ключ
            'language': 'rus',        # распознаем русский язык
            'isOverlayRequired': False
        }
        
        response = requests.post('https://ocr.space', files=files, data=payload).json()

        if response.get("ParsedResults"):
            extracted_text = response["ParsedResults"][0]["ParsedText"]
            
            if extracted_text.strip():
                final_response = (
                    f"📝 **Распознанный текст:**\n\n"
                    f"{extracted_text.strip()}\n\n"
                    f"⚠️ _Перепроверьте результат вручную._"
                )
                bot.edit_message_text(final_response, message.chat.id, status_msg.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text("❌ Не удалось найти разборчивый текст на изображении. Попробуйте сделать фото при лучшем освещении.", message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Ошибка сервера распознавания. Попробуйте загрузить фото еще раз.", message.chat.id, status_msg.message_id)

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке фото.")

if __name__ == '__main__':
    bot.infinity_polling()
