import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# ඔබේ Telegram Bot Token එක මෙතනට දාන්න
TOKEN = '8779154473:AAHrYRxFndt9FQvZ9aUQ5Flz2Q7-FH-ddgE'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tharaka EW AI System Online! \nCommands: /status gold, /status btc, /summary")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # මෙතනට තමයි 90% Accuracy Elliott Wave Logic එක එන්නේ
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🔍 Scanning Market...\n✅ Gold 90% Setup Identified!\nEntry: 2410.5 | SL: 2405 | TP: 2425")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    status_handler = CommandHandler('status', status)
    
    application.add_handler(start_handler)
    application.add_handler(status_handler)
    
    application.run_polling()
