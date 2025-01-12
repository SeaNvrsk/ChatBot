import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from util import send_text


from keys import token

app = Application.builder().token(token).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hello {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    print(user)

async def good_bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Bye {user}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(f"you said {update.message.text}" )

async def otro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_text(update, context, "Es otro test")

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('bye', good_bye))
app.run_polling()