import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable

import tg, parse, graph


def main():
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    url = 'https://www.worldometers.info/coronavirus/'
    # total = get_total_covid(get_html(url))
    # print(f'Всего заболевших: {total}')
    table = parse.get_from_countries_covid(parse.get_html(url), 20)
    graph.create_graph(table)
    graph.create_graph_deaths(table)
    #tg.launch_bot(TELEGRAM_TOKEN)

if __name__ == '__main__':
    load_dotenv()
    main()
