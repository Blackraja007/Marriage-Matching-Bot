import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext

# Load bot token from environment variables
TOKEN = os.getenv("7866619287:AAEY7KG15VuWA5DeqCxKqoIZOOReH-0Bums")
bot = Bot(token=TOKEN)

# Flask app initialization
app = Flask(__name__)

# Telegram Dispatcher
dispatcher = Dispatcher(bot, None, workers=4, use_context=True)

# Logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("வணக்கம்! திருமண பொருத்தம் Telegram Bot-க்கு வரவேற்கிறேன்! உங்கள் ராசி & நட்சத்திரம் அனுப்புங்கள்.")

# Message handler
def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    update.message.reply_text(f"நீங்கள் அனுப்பிய தகவல்: {user_input}")

# Handlers registration
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook setup
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route("/")
def home():
    return "Telegram Bot Webhook Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
