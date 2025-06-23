
import telebot
import requests

# Replace this with your actual bot token from @BotFather
BOT_TOKEN = 'os.getenv("BOT_TOKEN")'
bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://ashlynn.serv00.net/Ashlynnterabox.php?url="

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome!\nSend me any Terabox video link and I will give you the direct download link.")

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    user_msg = message.text.strip()
    if "terabox" in user_msg:
        bot.reply_to(message, "🔄 Processing your link...")
        try:
            response = requests.get(API_URL + user_msg)
            if response.status_code == 200:
                download_link = response.text.strip()
                bot.send_message(message.chat.id, f"✅ Download Link:\n{download_link}")
            else:
                bot.send_message(message.chat.id, "❌ Failed to fetch download link. Try again later.")
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Error occurred:\n{str(e)}")
    else:
        bot.reply_to(message, "❗Please send a valid Terabox link.")

bot.polling()
