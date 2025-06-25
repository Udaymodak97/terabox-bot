import telebot
import http.client
import json

# === CONFIG ===
BOT_TOKEN = "7509061898:AAHBBfgfGrui17diDqNDtc41j0M3yYp4D8E"
RAPIDAPI_KEY = "d784df92f7mshe2284e3acf48d10p132bb5jsn152b126cb96f"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.strip()

    if "terabox.app" in user_text or "terabox" in user_text:
        try:
            bot.send_chat_action(message.chat.id, 'typing')

            # Prepare RapidAPI request
            conn = http.client.HTTPSConnection("terabox-downloader-direct-download-link-generator.p.rapidapi.com")

            payload = json.dumps({
                "url": user_text
            })

            headers = {
                'x-rapidapi-key': RAPIDAPI_KEY,
                'x-rapidapi-host': "terabox-downloader-direct-download-link-generator.p.rapidapi.com",
                'Content-Type': "application/json"
            }

            conn.request("POST", "/fetch", payload, headers)
            res = conn.getresponse()
            data = res.read()

            response_data = json.loads(data)

            # Check response format
            if isinstance(response_data, list) and len(response_data) > 0:
                download_link = response_data[0].get("download_url", "❌ Download link not found.")
            elif isinstance(response_data, dict):
                download_link = response_data.get("download_url", "❌ Download link not found.")
            else:
                download_link = "❌ Invalid response format."

            bot.reply_to(message, f"📥 Download Link:\n{download_link}")

        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")

    else:
        bot.reply_to(message, "🔗 Terabox link bhejo!")


print("🤖 Bot is running...")
bot.infinity_polling()
