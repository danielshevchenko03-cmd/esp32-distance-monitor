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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("*/start* - почати роботу з ботом\n*/help* - список команд\n*/get_data* - отримати CSV з даними датчика", parse_mode="Markdown")

async def post_init(application):
    commands = [
        BotCommand("start", "Почати роботу з ботом"),
        BotCommand("help", "Список команд"),
        BotCommand("get_data", "Отримати CSV з даними датчика"),
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

        await update.message.reply_document(document=document_file, caption="")

    except requests.RequestException:
        await update.message.reply_text("⚠️ Сервер бекенду тимчасово недоступний ⚠️")

    except Exception as error:
        await update.message.reply_text("Виникла помилка при формуванні звіту")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("get_data", get_data))

    print("🤖 Бот запущен!")
    app.run_polling()