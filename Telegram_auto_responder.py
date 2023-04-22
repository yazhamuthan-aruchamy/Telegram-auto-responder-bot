from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = 'Your_API_KEY'
BOT_USERNAME: Final = '@Your_bot_name'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE): # Lets us use the /start command
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE): # Lets us use the /help command
    await update.message.reply_text('Try typing anything and I will do my best to respond!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE): # Lets us use the /custom command
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')

def process_message(message, keywords, response):
    score = 0
    message = message.lower()
    for word in keywords:
        if word in message:
            score += 1
    return score if score > 0 else 0, response

def get_response(message):
    score_list = [
        process_message(message, ['hello', 'hi', 'hey'], 'Hey there!'),
        process_message(message, ['how are you', 'how\'s it going', 'how\'s life'], 'I\'m doing well, thanks for asking!'),
        process_message(message, ['what is your name', 'who are you', 'your name'], 'My name is Bot, nice to meet you!'),
        process_message(message, ['what time is it', 'what\'s the time'], 'It\'s time to get a watch!'),
        process_message(message, ['what is your favorite color', 'favorite color'], 'My favorite color is blue.'),
        process_message(message, ['what is your favorite food', 'favorite food'], 'I don\'t eat food, sorry!'),
        process_message(message, ['thanks', 'thank you', 'thx'], 'You\'re welcome!'),
        process_message(message, ['goodbye'], 'Goodbye!') 
    ]

    max_score = max(score_list)
    index = score_list.index(max_score)

    return score_list[index][1]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text.lower()
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = get_response(new_text)
        else:
            return
    else:
        response = get_response(text)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE): # Log errors
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':  # Run the program
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))  # Commands
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))  # Messages
    app.add_error_handler(error) # Log all errors
    app.run_polling(poll_interval=2) # Run the bot