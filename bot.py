from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler
from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu,
                  default_callback_handler, load_prompt, send_text_buttons)
from credentials import ChatGPT_TOKEN, BOT_TOKEN


chat_gpt = ChatGptService(ChatGPT_TOKEN)
app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('main')
    await send_image(update, context, 'GPT')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Главное меню',
        'random': 'Узнать случайный интересный факт 🧠',
        'gpt': 'Задать вопрос чату GPT 🤖',
        'talk': 'Поговорить с известной личностью 👤',
        'quiz': 'Поучаствовать в квизе ❓'
        # Добавить команду в меню можно так:
        # 'command': 'button text'

    })

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, 'random')
    message = await send_text(update, context, "Генерирую интересный факт...")
    prompt = load_prompt('random')
    answer = await chat_gpt.send_question(prompt, '')
    await message.edit_text("...")
    await send_text_buttons(update, context, answer, {
        'random_more': 'Еще факт',
        'stop': 'Закончить'
    })

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await start(update, context)

async def random_more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await random(update, context)


# Зарегистрировать обработчик команды можно так:
# app.add_handler(CommandHandler('command', handler_func))
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
# Зарегистрировать обработчик коллбэка можно так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(stop, pattern='stop'))
app.add_handler(CallbackQueryHandler(random_more, pattern='^random_.*'))
app.run_polling()
