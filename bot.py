import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from scraper import scrape_movies

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Movie Bot! Use /search <movie_name> to find movies.")

# Search command
def search(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Please provide a movie name. Usage: /search <movie_name>")
        return
    
    movie_name = " ".join(context.args)
    update.message.reply_text(f"Searching for '{movie_name}'...")
    
    # Call the scraper function
    movies = scrape_movies(movie_name)
    
    if movies:
        for movie in movies:
            update.message.reply_text(f"{movie['title']}\n{movie['link']}")
    else:
        update.message.reply_text("No results found or an error occurred.")

# Main function
def main():
    # Replace with your BotFather token
    BOT_TOKEN = "YOUR_BOT_TOKEN"
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Command Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
