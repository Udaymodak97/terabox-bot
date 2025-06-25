import telebot
import requests
import os

# 📌 Replace this with your own bot token
BOT_TOKEN = '📌 YOUR_BOT_TOKEN_HERE'

# 📌 Replace this with your actual RapidAPI key
RAPIDAPI_KEY = '📌 YOUR_RAPIDAPI_KEY_HERE'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Welcome! Send me a TeraBox link to download the video.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    user_link = message.text.strip()

    # Check if it is a TeraBox link
    if not user_link.startswith("http"):
        bot.send_message(message.chat.id, "❗ Please send a valid TeraBox link.")
        return

    url = "https://terabox-direct-download.p.rapidapi.com/download"
    querystring = {"url": user_link}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "terabox-direct-download.p.rapidapi.com"
    }

    bot.send_chat_action(message.chat.id, "typing")
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        try:
            data = response.json()
            video_url = data.get("video_url") or data.get("download_link")

            if video_url:
                bot.send_message(message.chat.id, f"✅ Here is your video link:\n{video_url}")
            else:
                bot.send_message(message.chat.id, "❌ Could not find video URL in the API response.")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Failed to parse API response: {str(e)}")
    else:
        bot.send_message(message.chat.id, f"❌ API Error: {response.status_code}")

# 📢 Start polling
bot.remove_webhook()
bot.polling()
