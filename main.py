import logging
import requests
from telegram import Update, ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8298012658:AAFtEXokf6SeIzTQdGu65SKxMc-qobUuOR4"
GEMINI_API_KEY = "AIzaSyCFA__HwMSDMW759nyiyRvVHkv9Pr7EsjM"

logging.basicConfig(level=logging.INFO)

async def gemini_chat(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {e}"

def pollinations_image(prompt):
    return f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salam! Main ItfanAibot hoon 🤖\nUse /image <prompt> to make AI images 🎨")

async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Example: /image cat flying in sky 🐱☁️")
        return
    prompt = " ".join(context.args)
    await update.message.reply_photo(pollinations_image(prompt), caption=f"🖼️ {prompt}")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        await update.message.reply_text("Private chat only 🚫")
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    reply = await gemini_chat(update.message.text)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("🤖 ItfanAibot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
