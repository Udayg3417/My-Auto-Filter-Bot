import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fetching environment variables
BOT_TOKEN = os.getenv("7387135619:AAEG0w5cWndk0oKjoRShArEy5rK0OYCyUP8")
AUTH_CHANNEL_ID = int(os.getenv("-1002049964184"))

FILTER_KEYWORDS = ["spam", "scam", "badword"]

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if update.effective_chat.id == AUTH_CHANNEL_ID:
        update.message.reply_text('Hi! You are authorized to use this bot.')
    else:
        update.message.reply_text('You are not authorized to use this bot.')

def filter_message(update: Update, context: CallbackContext) -> None:
    """Filter messages based on keywords in the authorized channel."""
    if update.effective_chat.id == AUTH_CHANNEL_ID:
        for keyword in FILTER_KEYWORDS:
            if keyword in update.message.text.lower():
                update.message.delete()
                logger.info(f"Deleted message: {update.message.text}")
                break
    else:
        update.message.reply_text('You are not authorized to use this bot.')

def main() -> None:
    """Start the bot."""
    # Ensure the token is present
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN provided!")
        return

    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, filter_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
