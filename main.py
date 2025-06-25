import telebot
import requests

# ✅ Your Telegram Bot Token
BOT_TOKEN = '7539266935:AAH5PBWrSfnD_Ac5xwk9F8lAZLHTbhOJ7MM'

# ✅ Your RapidAPI Key
RAPIDAPI_KEY = 'd784df92f7mshe2284e3acf48d10p132bb5jsn152b126cb96f'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Welcome! Send me a TeraBox link to get the download video link.")

@bot.message_handler(func=lambda message: True)
def fetch_link(message):
    link = message.text.strip()

    if not link.startswith("http"):
        bot.send_message(message.chat.id, "❗ Please send a valid TeraBox URL.")
        return

    bot.send_chat_action(message.chat.id, "typing")

    url = "https://terabox-downloader-direct-download-link-generator.p.rapidapi.com/fetch"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "terabox-downloader-direct-download-link-generator.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    payload = {
        "url": link
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            video_url = data.get("video_url") or data.get("download_link")

            if video_url:
                bot.send_message(message.chat.id, f"✅ Video Link:\n{video_url}")
            else:
                bot.send_message(message.chat.id, "❌ Video URL not found in response.")
        else:
            bot.send_message(message.chat.id, f"❌ API Error: {response.status_code}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Something went wrong:\n{str(e)}")

# 🟢 Start polling
bot.remove_webhook()
bot.polling()
