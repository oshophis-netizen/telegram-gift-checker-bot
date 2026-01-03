import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

if not BOT_TOKEN or not ADMIN_ID:
    print("❌ BOT_TOKEN или ADMIN_ID не установлены!")
    exit(1)

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    print("❌ ADMIN_ID должен быть числом!")
    exit(1)

# /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "друг"
    welcome_text = f"Hello, {name}! 👋\nBot is running on Render."
    await update.message.reply_text(welcome_text)

# Обработка файлов
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "пользователь"
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"📁 File from {name}, ID: {user.id}")
    await context.bot.forward_message(chat_id=ADMIN_ID,
                                      from_chat_id=update.effective_chat.id,
                                      message_id=update.message.message_id)
    await update.message.reply_text(f"📥 File received, {name}!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    print("🤖 Bot started on Render")
    application.run_polling()

if __name__ == "__main__":
    main()


