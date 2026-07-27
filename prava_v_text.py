import os
import telebot
import requests
import base64
from dotenv import load_dotenv  # Добавлено

# Загружаем переменные из файла .env
load_dotenv()  # Добавлено

# Бот забирает токен из настроек хостинга Bothost
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Получаем API-ключ ocr.space из кода (убедитесь, что ваш ключ вставлен верно)
OCR_API_KEY = "K88446889388957" 

print("Запуск надежного Base64 распознавателя...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне четкую фотографию водительского удостоверения, и я извлечу из него текст.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        status_msg = bot.reply_to(message, "Скачиваю фото и начинаю распознавание. Пожалуйста, подождите...")

        # Скачиваем файл во временную память
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Кодируем скачанное фото в Base64 string
        base64_image = base64.b64encode(downloaded_file).decode('utf-8')

        # Формируем надежный POST запрос
        payload = {
            'apikey': OCR_API_KEY,
            'language': 'rus',
            'isOverlayRequired': False,
            'base64Image': f"data:image/jpeg;base64,{base64_image}"
        }
        
        response = requests.post('https://ocr.space', data=payload).json()

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
            # Если API вернул ошибку, пишем подробности в консоль сервера
            print(f"Ошибка API: {response}")
            bot.edit_message_text("❌ Ошибка сервера распознавания. Попробуйте загрузить фото еще раз.", message.chat.id, status_msg.message_id)

    except Exception as e:
        print(f"Ошибка в блоке обработки: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке фото.")

if __name__ == '__main__':
    bot.infinity_polling()
