import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to scrape movie links
def scrape_movies(query):
    base_url = "https://hdmaal.tw/search?q="  # Replace with a legal website
    search_url = base_url + query.replace(" ", "+")
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse results (update this based on the website's structure)
        results = soup.find_all('a', class_='movie-link')  # Replace 'movie-link' with the actual class name
        movies = []

        for result in results[:5]:  # Limit to top 5 results
            title = result.text.strip()
            link = result['href']
            movies.append({"title": title, "link": link})

        return movies

    except Exception as e:
        print(f"Error: {e}")
        return []

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Movie Scraper Bot! Use /search <movie_name> to find movies.")

# Search command
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a movie name. Usage: /search <movie_name>")
        return

    movie_name = " ".join(context.args)
    await update.message.reply_text(f"Searching for '{movie_name}'...")
    movies = scrape_movies(movie_name)

    if movies:
        for movie in movies:
            await update.message.reply_text(f"{movie['title']}\n{movie['link']}")
    else:
        await update.message.reply_text("No results found or an error occurred.")

# Main function
def main():
    BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your bot token

    # Create the application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("search", search))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
