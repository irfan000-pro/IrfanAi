import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai
import requests

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
POLLINATION_API_KEY = os.getenv("POLLINATION_API_KEY")

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! Send me text to use Gemini, or /image <prompt> to generate AI images!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("⚠️ Error: " + str(e))

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /image <your prompt>")
        return

    prompt = " ".join(context.args)
    try:
        url = "https://api.pollinations.ai/prompt/" + requests.utils.quote(prompt)
        response = requests.get(url)
        if response.status_code == 200:
            await update.message.reply_photo(url)
        else:
            await update.message.reply_text("⚠️ Failed to generate image.")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("❌ Error generating image: " + str(e))

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", generate_image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot is running 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
