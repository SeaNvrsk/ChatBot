from httpx import request
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, filters, ContextTypes, CommandHandler, \
    MessageHandler, ConversationHandler
from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu,
                  default_callback_handler, load_prompt, send_text_buttons)
from credentials import ChatGPT_TOKEN, BOT_TOKEN

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

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
        'quiz': 'Поучаствовать в квизе ❓',
        'spanish': 'Выучить новые испанские слова 🙌🏼',
        'weather': 'узнать погоду на завтра 🌤'

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


async def random_more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await random(update, context)


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'gpt'
    chat_gpt.set_prompt(load_prompt('gpt'))
    text = load_message('gpt')
    await send_image(update, context, 'CHATGPT')
    await send_text(update, context, text)


async def gpt_dialogue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.message.text
    message = await send_text(update, context, "Думаю над ответом...")
    answer = await chat_gpt.add_message(request)
    await message.edit_text('...')
    await send_text_buttons(update, context, answer, buttons={'stop':'Завершить'})


async def spanish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'spanish'
    chat_gpt.set_prompt(load_prompt('spanish'))
    text = load_message('spanish')
    await send_image(update, context, 'spanish')
    await send_text(update, context, text)



async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'weather'
    chat_gpt.set_prompt(load_prompt('weather'))
    text = load_message('weather')
    await send_image(update, context, 'weather')
    await send_text(update, context, text)


async def weather_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.message.text
    message = await send_text(update, context, "Закрываю глаза и представляю погоду на завтра...")
    answer = await chat_gpt.add_message(request)
    await message.edit_text('...')
    await send_text_buttons(update, context, answer, buttons={'stop': 'Завершить'})


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['mode'] = 'talk'
    text = load_message('talk')
    await send_image(update, context, 'talk')
    await send_text_buttons(update, context, text, buttons={
        'talk_cobain' : 'Курт Кобейн',
        'talk_hawking' : 'Стивен Хокинг',
        'talk_nietzsche' : 'Фридрих Ницще',
        'talk_queen' : 'Королева Елизавета',
        'talk_tolkien' : 'Джон Толкиен'
    })


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_gpt.set_prompt(load_prompt('quiz'))
    await send_image(update, context, 'quiz')
    await send_text_buttons(update, context, "Выбери тему",{
        'quiz_prog': 'Программирование',
        'quiz_math': 'Математика',
        'quiz_biology': 'Биология'
    })
    return THEME


async def quiz_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    question = await chat_gpt.add_message(update.callback_query.data)
    await send_text(update, context, question)
    return ANSWER


async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    answer = await chat_gpt.add_message(text)
    if answer == 'Правильно':
        context.user_data['score'] = context.user_data.get('score', 0) + 1
    await send_text(update, context, answer + '\n\nВаш счет: ' + str(context.user_data.get('score', 0)))
    return ConversationHandler.END


async def talk_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    data = update.callback_query.data
    chat_gpt.set_prompt(load_prompt(data))
    greet = await chat_gpt.add_message('Поздоровайся со мной')
    await send_image(update, context, data)
    await send_text(update, context, greet)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await start(update, context)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('mode') in ('gpt', 'talk', 'spanish'):
        await gpt_dialogue(update, context)
    elif context.user_data.get('mode') == 'weather':
        await weather_info(update, context)


app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

# Зарегистрировать обработчик команды можно так:
# app.add_handler(CommandHandler('command', handler_func))
app.add_handler(CommandHandler('talk', talk))
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('random', random))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('weather', weather))
app.add_handler(CommandHandler('spanish', spanish))
# Зарегистрировать обработчик коллбэка можно так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^app_.*'))
app.add_handler(CallbackQueryHandler(stop, pattern='stop'))
app.add_handler(CallbackQueryHandler(random_more, pattern='^random_.*'))
app.add_handler(CallbackQueryHandler(talk_buttons, pattern='^talk_.*'))


THEME, ANSWER = range(2)
app.add_handler(ConversationHandler(entry_points=[CommandHandler('quiz', quiz)], states={
    THEME: [CallbackQueryHandler(quiz_theme, pattern='^quiz_.*')],
    ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_answer)]
},fallbacks=[CommandHandler('stop', stop)]))

app.run_polling()


