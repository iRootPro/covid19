from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


from parse import get_html, get_total_covid, get_from_countries_covid, get_country
from subscribe import add_member, check_member
from parse_rus import top20_russia
from graph import get_date_and_time
from answer import search_similar_question


def start(update, context):
    update.message.reply_text("""
		🖖 Привет. Я бот COVID-19. Расскажу о статистике по заболеваемости короновирусом,\
		отвечу на твои вопросы.\n\
		❔ Можешь меня спросить о коронавирусе. Например:\n\
		- *Что такое кароновирус?*\n\
		- *Антибиотики эффективны от коронавируса?*\n\
		- *Симптомы covid-19*\n\
		- *Меры защиты*\n\
		и многое другое. Просто набери свой вопрос и отправиь его мне. Все ответы взяты с сайта ВОЗа.\n\
		\n
		*📱 Наберите / чтобы попасть в меню. Доступные команды:*\n\
		/info - Выведу информации о заразившихся, умерших и выздоровевших в режиме Online.\n\
		/total - Пришлю тебе три графика с динамикой развития COVID-19.\n\
		/russia - Дам информацию об обстановке в России. Общая + TOP20 регионов по заболеваемости.\n\
		/top10 - Пришлю график с TOP10 странами по заболеваемости.\n\n\
		🙏 Есть вопросы или предложения? Можете написать сюда -> @iRootPro
    	""", parse_mode='markdown')


def info(update, context):
    url = 'https://www.worldometers.info/coronavirus/'
    total_cases, total_deaths, total_recovery = get_total_covid(get_html(url))
    text_answer = text = f'<u>Ситуация в мире:</u>\n🦠 Всего заболевших: {total_cases}\n⚰ Умерших: {total_deaths}\n👥 Выздоровевших: {total_recovery}'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_answer, parse_mode='html')


def top10(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('top10.png', 'rb'))


def total(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('total_cases.png', 'rb'))
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('total_deaths.png', 'rb'))
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('total_recovered.png', 'rb'))


def russia(update, context):
    case, death, recovered = get_country('Russia')
    text_answer = f'<u>Ситуация в России:</u>\n🦠 Всего заболевших: {case}\n⚰ Умерших: {death}\n👥 Выздоровевших: {recovered}'
    text_detail_info = f'{top20_russia()}\n Задержка данных 2 часа'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_answer, parse_mode='html')
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_detail_info, parse_mode='markdown')


def message(update, context):
    answer = search_similar_question(update.message.text)
    update.message.reply_text(answer)


def subscribe(update, context):
    if check_member(update.effective_chat.id):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Вы уже подписались ранее')
    else:
        add_member(update.effective_chat.id)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Вы успешно подписаны на рассылку.')


def launch_bot(token_telegram):
    updater = Updater(token=token_telegram, use_context=True)
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    top10_handler = CommandHandler('top10', top10)
    total_handler = CommandHandler('total', total)
    russia_handler = CommandHandler('russia', russia)
    subscribe_handler = CommandHandler('subscribe', subscribe)
    message_handler = MessageHandler(Filters.text, message)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(top10_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(total_handler)
    dispatcher.add_handler(russia_handler)
    dispatcher.add_handler(subscribe_handler)
    dispatcher.add_handler(message_handler)
    updater.start_polling()
