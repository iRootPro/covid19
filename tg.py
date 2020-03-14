from telegram.ext import Updater, CommandHandler

from parse import get_html, get_total_covid, get_from_countries_covid

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет. Я бот COVID-19. Я расскажу о статистике по заболеваемости короновирусом. Наберите /info - для получения общего количества заболевших, /top - выведет TOP 10 стран по заболеваемости")

def info(update, context):
	url = 'https://www.worldometers.info/coronavirus/'
	context.bot.send_message(chat_id=update.effective_chat.id, text=f'Всего заболевших: {get_total_covid(get_html(url))}')

def top(update, context):
	url = 'https://www.worldometers.info/coronavirus/'
	print(context)
	context.bot.send_message(chat_id=update.effective_chat.id, text=get_from_countries_covid(get_html(url), 10))

def launch_bot(token_telegram):
    updater = Updater(token=token_telegram, use_context=True)
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    top_handler = CommandHandler('top', top)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(top_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
