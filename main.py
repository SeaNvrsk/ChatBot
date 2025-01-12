import logging

from telegram import ForceReply, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from util import send_text, send_image

from keys import token

app = Application.builder().token(token).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}!")
    markup = ReplyKeyboardMarkup( [
        ['1', '2'],
    ])
    await context.bot.send_message(update.effective_chat.id, 'Hello, welcome to the bot!', reply_markup=markup)
    print(user)

async def good_bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Bye {user}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(f"you said {update.message.text}" )

async def otro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, "GPT")
    await send_text(update, context, "Es otro test")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, otro))
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('bye', good_bye))
app.run_polling()