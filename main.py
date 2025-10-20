import os
import logging
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("8298012658:AAFtEXokf6SeIzTQdGu65SKxMc-qobUuOR4")
GEMINI_API_KEY = os.getenv("AIzaSyCFA__HwMSDMW759nyiyRvVHkv9Pr7EsjM")

# Gemini chat function
def get_gemini_response(prompt):
    try:
        res = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Error: {e}"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I’m *ItfanAi* — your smart digital friend.\nAsk me anything!", parse_mode="Markdown")

# Handle user messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user.first_name
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    reply = get_gemini_response(text)
    await update.message.reply_text(f"🤖 {reply}")

# Pollinations Image Command
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("🖼️ Usage: /image <your prompt>")
        return
    img_url = f"https://image.pollinations.ai/prompt/{query.replace(' ', '%20')}"
    await update.message.reply_photo(img_url, caption=f"🎨 Prompt: {query}")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
