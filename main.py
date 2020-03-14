import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable

import tg


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_total_covid(soup):
    div_total = soup.find('div', class_='maincounter-number')
    total = div_total.find('span').get_text()
    return total


def get_from_countries_covid(soup, top):
    table = soup.find('table', id='main_table_countries').find('tbody')
    trs = table.find_all('tr')

    table_data = [['Страна', 'Заболевших',
                   'Новых заболевших', 'Умерших', 'Новых умерших']]
    for tr in trs:
        top -= 1
        tds = tr.find_all('td')
        if tds[0].find('a'):
            country = tds[0].find('a').get_text()
        else:
            country = tds[0].get_text()
        cases = tds[1].get_text()
        new_cases = tds[2].get_text()
        deaths = tds[3].get_text()
        new_deaths = tds[4].get_text()

        if top >= 0:
            table_data.append([country, cases, new_cases, deaths, new_deaths])
        if 'Russia' in table_data:
            break
        if 'Russia' in country:
            table_data.append([country, cases, new_cases, deaths, new_deaths])

    table = AsciiTable(table_data)
    return table


def main():
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    url = 'https://www.worldometers.info/coronavirus/'
    total = get_total_covid(get_html(url))
    print(f'Всего заболевших: {total}')
    table = get_from_countries_covid(get_html(url), 10)
    tg.launch_bot(TELEGRAM_TOKEN)

if __name__ == '__main__':
    load_dotenv()
    main()
