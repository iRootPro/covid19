from telegram.ext import Updater, CommandHandler


from parse import get_html, get_total_covid, get_from_countries_covid
from subscribe import add_member


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет. Я бот COVID-19. Я расскажу о статистике по заболеваемости короновирусом. Наберите / - для получения списка команд")


def info(update, context):
	url = 'https://www.worldometers.info/coronavirus/'
	total_cases, total_deaths, total_recovery = get_total_covid(get_html(url))
	text_answer = text=f'Всего заболевших: {total_cases}\nУмерших: {total_deaths}\nВыздоровевших: {total_recovery}'
	context.bot.send_message(chat_id=update.effective_chat.id, text=text_answer)


def top(update, context):
	url = 'https://www.worldometers.info/coronavirus/'
	context.bot.send_message(chat_id=update.effective_chat.id, text=get_from_countries_covid(get_html(url), 10))


def top20_img(update, context):
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('cases_top20.png', 'rb'))


def deaths(update,context):
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('deaths.png', 'rb'))


def total(update, context):
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('total_cases.png', 'rb'))
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('total_deaths.png', 'rb'))
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('total_recovered.png', 'rb'))

def russia(update, context):
	context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('russian_cases.png', 'rb'))

def subscribe(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text='Вы подписаны на рассылку.')
	add_member(update.effective_chat.id)
	context.bot.send_message(chat_id=update.effective_chat.id, text='Вы подписаны на рассылку.')


def launch_bot(token_telegram):
    updater = Updater(token=token_telegram, use_context=True)
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    top_handler = CommandHandler('top', top)
    top20_img_handler = CommandHandler('top20_img', top20_img)
    deaths_handler = CommandHandler('deaths', deaths)
    total_handler = CommandHandler('total', total)
    russia_handler = CommandHandler('russia', russia)
    subscribe_handler = CommandHandler('subscribe', subscribe)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(deaths_handler)
    dispatcher.add_handler(top20_img_handler)
    dispatcher.add_handler(top_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(total_handler)
    dispatcher.add_handler(russia_handler)
    dispatcher.add_handler(subscribe_handler)
    updater.start_polling()
