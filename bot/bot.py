import os
import logging
import requests
import csv
import io
from dotenv import load_dotenv

from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv("TG_BOT_TOKEN")
API_URL = os.getenv("DJANGO_API_URL")

logger = logging.getLogger("sensor_bot")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """*/start* - почати роботу з ботом
*/help* - список команд
*/get_data* - отримати CSV з даними сенсора
*/stats* - статистика сенсора"""
    await update.message.reply_text(text, parse_mode="Markdown")

async def post_init(application):
    commands = [
        BotCommand("start", "Почати роботу з ботом"),
        BotCommand("help", "Список команд"),
        BotCommand("get_data", "Отримати CSV з даними сенсора"),
        BotCommand("stats", "Статистика сенсора"),
    ]
    await application.bot.set_my_commands(commands)

async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()

        data = response.json()

        file = io.StringIO()
        fieldnames = ['id', 'device_id', 'time', 'distance']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

        csv_data = file.getvalue().encode('utf-8')
        document_file = io.BytesIO(csv_data)
        document_file.name = "events.csv"

        total_count = len(data)
        caption_text = f"Звіт з {total_count} подій"
        logger.info(f"Сформовано звіт: {total_count} подій") # logger logic
        await update.message.reply_document(document=document_file, caption=caption_text)

    except requests.RequestException:
        logger.warning("Backend недоступний")
        await update.message.reply_text("⚠️ Сервер бекенду тимчасово недоступний ⚠️")

    except Exception as error:
        logger.warning(f"Помилка при формуванні звіту {error}") # logger logic
        await update.message.reply_text("Виникла помилка при формуванні звіту")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()

        data = response.json()
        total_count = len(data)

        if len(data) != 0:
            last_event = data[-1]
            message = f"Всього подій: {total_count}\nОстання подія: {last_event['time']}, {last_event['distance']} мм"
            await update.message.reply_text(message)

        else:
            await update.message.reply_text("Подій не виявлено")

    except requests.RequestException:
        await update.message.reply_text("⚠️ Сервер бекенду тимчасово недоступний ⚠️")

    except Exception as error:
        await update.message.reply_text("Виникла помилка при формуванні звіту")    


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("get_data", get_data))
    app.add_handler(CommandHandler("stats", stats))

    logger.info("🤖 Bot launched!")
    app.run_polling()