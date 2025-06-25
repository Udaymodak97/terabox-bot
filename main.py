import telebot
import requests

# ✅ Tumhara Bot Token
BOT_TOKEN = '7539266935:AAH5PBWrSfnD_Ac5xwk9F8lAZLHTbhOJ7MM'

# ✅ Tumhara RapidAPI Key
RAPIDAPI_KEY = 'd784df92f7mshe2284e3acf48d10p132bb5jsn152b126cb96f'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Welcome! Send me a TeraBox link to get the download link.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    user_link = message.text.strip()

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
                bot.send_message(message.chat.id, f"✅ Video link:\n{video_url}")
            else:
                bot.send_message(message.chat.id, "❌ Could not find video link in the response.")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ JSON parse error: {str(e)}")
    else:
        bot.send_message(message.chat.id, f"❌ API Error: {response.status_code}")

bot.remove_webhook()
bot.polling()
