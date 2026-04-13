import os
import logging
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import init_db, subscribe_user, unsubscribe_user, get_all_subscribers, is_news_new
from news import fetch_tech_news

# Logging Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def broadcast_news(context: ContextTypes.DEFAULT_TYPE):
    """Scheduled task to send news to all subscribers."""
    articles = await fetch_tech_news()
    subscribers = get_all_subscribers()
    
    if not articles or not subscribers:
        return

    for art in articles:
        if is_news_new(art['hash']):
            message = (
                f"🚀 **Tech Update**\n\n"
                f"📰 **{art['title']}**\n\n"
                f"🔹 {art['summary']}\n\n"
                f"🔗 [Read more]({art['url']})"
            )
            for user_id in subscribers:
                try:
                    await context.bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
                except Exception:
                    continue # Skip users who blocked the bot

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Welcome to **TechBulletinBot**! 🖥️\n\n"
        "I provide the latest technology news updates twice daily (Morning & Evening).\n\n"
        "Commands:\n"
        "/subscribe - Receive daily updates\n"
        "/unsubscribe - Stop receiving updates\n"
        "/news - Get latest news instantly"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = await fetch_tech_news()
    if not articles:
        await update.message.reply_text("Unable to fetch news right now. Please try again later.")
        return
    
    art = articles[0]
    message = f"🚀 **Latest Tech News**\n\n**{art['title']}**\n\n{art['summary']}\n\n🔗 [Read more]({art['url']})"
    await update.message.reply_text(message, parse_mode='Markdown')

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if subscribe_user(update.effective_user.id):
        await update.message.reply_text("✅ Success! You've subscribed to twice-daily tech updates.")
    else:
        await update.message.reply_text("You are already subscribed to the bulletin!")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if unsubscribe_user(update.effective_user.id):
        await update.message.reply_text("❌ You have unsubscribed from daily updates.")
    else:
        await update.message.reply_text("You aren't currently subscribed.")

def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Job Queue for Automation (Morning 08:00, Evening 20:00)
    job_queue = app.job_queue
    job_queue.run_daily(broadcast_news, time=datetime.time(hour=8, minute=0))
    job_queue.run_daily(broadcast_news, time=datetime.time(hour=20, minute=0))

    logging.info("TechBulletinBot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
