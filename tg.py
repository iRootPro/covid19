from telegram.ext import Updater, CommandHandler


from parse import get_html, get_total_covid, get_from_countries_covid, get_country
from subscribe import add_member, check_member
from parse_rus import top10_russia
from graph import get_date_and_time


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет. Я бот COVID-19. Я расскажу о статистике по заболеваемости короновирусом. Наберите / - для получения списка команд")


def info(update, context):
    url = 'https://www.worldometers.info/coronavirus/'
    total_cases, total_deaths, total_recovery = get_total_covid(get_html(url))
    text_answer = text = f'<u>Ситуация в мире:</u>\n🦠 Всего заболевших: {total_cases}\n⚰ Умерших: {total_deaths}\n👥 Выздоровевших: {total_recovery}'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_answer, parse_mode='html')


def top(update, context):
    url = 'https://www.worldometers.info/coronavirus/'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=get_from_countries_covid(get_html(url), 10))


def top10(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('top10.png', 'rb'))


def top20_deaths(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=open('deaths.png', 'rb'))


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
    text_detail_info = f'{top10_russia()}\n Данные на:{get_date_and_time()}'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_answer, parse_mode='html')
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_detail_info, parse_mode='markdown')
    # context.bot.send_photo(chat_id=update.effective_chat.id,
    #                        photo=open('russian_cases.png', 'rb'))


def ukraine(update, context):
    case, death, recovered = get_country('Ukraine')
    text_answer = f'<u>Ситуация на Украине:</u>\n🦠 Всего заболевших: {case}\n⚰ Умерших: {death}\n👥 Выздоровевших: {recovered}'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_answer, parse_mode='html')


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
    top_handler = CommandHandler('top', top)
    top10_handler = CommandHandler('top10', top10)
    top20_deaths_handler = CommandHandler('top20_deaths', top20_deaths)
    total_handler = CommandHandler('total', total)
    russia_handler = CommandHandler('russia', russia)
    ukraine_handler = CommandHandler('ukraine', ukraine)
    subscribe_handler = CommandHandler('subscribe', subscribe)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(top20_deaths_handler)
    dispatcher.add_handler(top10_handler)
    dispatcher.add_handler(top_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(total_handler)
    dispatcher.add_handler(russia_handler)
    dispatcher.add_handler(ukraine_handler)
    dispatcher.add_handler(subscribe_handler)
    updater.start_polling()
