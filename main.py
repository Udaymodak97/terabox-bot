import telebot
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://tera-api-thory.vercel.app/api?api_key=7daysfreeapi&url="
"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome to TeraBox Bot! Send me any TeraBox link.")

@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("http"))
def handle_link(message):
    link = message.text.strip()
    try:
        response = requests.get(API_URL + link)
        data = response.json()
        if data.get("success"):
            bot.send_message(message.chat.id, "✅ Download Link:\n" + data["download_link"])
        else:
            bot.send_message(message.chat.id, "❌ Invalid link or no video found.")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {str(e)}")

bot.infinity_polling()
