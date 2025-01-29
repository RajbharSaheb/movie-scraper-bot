import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from scraper import search_movie
from config import TOKEN

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🎬 Welcome to Movie Bot! Send me a movie name to search.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_chat_action(action='typing')
    
    try:
        results = await search_movie(query)
        if not results:
            return await update.message.reply_text("🚫 No results found. Try another movie name.")
        
        response = "🍿 Search Results:\n\n"
        for res in results[:5]:  # Show top 5 results
            response += f"📽 {res['title']}\n🔗 {res['link']}\n\n"
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("⚠️ An error occurred. Please try again later.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
