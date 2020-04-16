import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd

from data import get_date
from data_current import write_to_csv


def get_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_info_cities(soup):
    data = []
    trs_item = soup.find_all('tr', class_='covid-table-view__item')
    for tr_item in trs_item:
        tds = tr_item.find_all('td')
        city = tds[0].get_text().strip()
        case = tds[1].get_text().strip()
        print(city, case)
        today = get_date()
        data.append([today, city, case])
    return data


def top20_russia():
    locations = pd.read_csv('db/russian.csv', delimiter=';',
                            thousands=' ', names=['Data', 'Location', 'Case'])
    loc_today = locations[locations.Data == get_date()][['Location', 'Case']]
    table = loc_today[0:21]
    markdown_table = tabulate(table, tablefmt='github',
                              showindex=False, numalign='right')
    return f'TOP20\n```{markdown_table}```'


def main():
    url = 'https://yandex.ru/web-maps/covid19'
    cities = get_info_cities(get_html(url))
    write_to_csv('russian.csv', cities)


if __name__ == '__main__':
    main()
