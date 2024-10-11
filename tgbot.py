import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logging.debug('Приложение загружено')

load_dotenv()  # Загрузка переменных окружения из .env файла

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("Токен не загружен! Проверьте файл .env.")

async def start(update: Update, context):
    await update.message.reply_text("Добро пожаловать! Нажмите на кнопку, чтобы начать работу с приложением.")

async def handle_webapp_data(update: Update, context):
    try:
        if update.message.web_app_data and update.message.web_app_data.data:
            data = update.message.web_app_data.data
            logging.info(f"Полученные данные из Mini App: {data}")
            await update.message.reply_text("Данные из Mini App успешно получены!")
        else:
            logging.error("Ошибка: данные не были получены.")
            await update.message.reply_text("Ошибка: данные не были получены.")
    except Exception as e:
        logging.error(f"Ошибка при обработке данных: {e}")
        await update.message.reply_text("Произошла ошибка при обработке данных.")

def main():
    # Инициализация приложения
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавление обработчиков
    application.add_handler(CommandHandler('start', start))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data)
    )

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
