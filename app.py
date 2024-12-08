from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Dispatcher, CommandHandler
from decouple import config

# Load your bot token from environment variables
BOT_API_KEY = config("BOT_API")

# Initialize Flask and the Telegram Bot
app = Flask(__name__)
bot = Bot(token=BOT_API_KEY)
dispatcher = Dispatcher(bot, None, workers=0)

# Define the start command handler
def start(update: Update, context):
    if context.args:
        channel_2_msg_id = context.args[0]
        post_url = f'https://t.me/newtest020/{channel_2_msg_id}'
        keyboard = [
            [InlineKeyboardButton("Go to Channel 2 Post", url=post_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Click to go to the post in Channel 2:', reply_markup=reply_markup)
    else:
        update.message.reply_text("No message ID provided!")

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# Define the webhook route
@app.route(f"/{BOT_API_KEY}", methods=["POST"])
def webhook():
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, bot)
    dispatcher.process_update(update)
    return "OK", 200

# Define a simple index route for testing
@app.route("/", methods=["GET"])
def index():
    return "Bot is running on Vercel!", 200
