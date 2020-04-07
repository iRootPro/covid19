import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd

from data import get_date, write_to_csv


def get_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_info_cities(soup):
    data = []
    divs_item = soup.find_all('div', class_='covid-panel-view__item')
    for div_item in divs_item:
        city = div_item.find(
            'div', class_='covid-panel-view__item-name').get_text().strip()
        case_div = div_item.find('div', class_='covid-panel-view__item-cases')
        try:
            case_div.div.decompose()
        except AttributeError:
            case_div.get_text()

        today = get_date()
        case = case_div.get_text()
        data.append([today, city, case])
    return data


def top10_russia():
    locations = pd.read_csv('db/russian.csv', delimiter=';',
                            thousands=' ', names=['Data', 'Location', 'Case'])
    loc_today = locations[locations.Data == get_date()][['Location', 'Case']]
    table = loc_today[1:21]
    markdown_table = tabulate(table, tablefmt='github', headers=[
                              'Локация', '🦠'], showindex=False, numalign='right')
    return f'TOP20\n```{markdown_table}```'


def main():
    url = 'https://yandex.ru/web-maps/covid19'
    cities = get_info_cities(get_html(url))
    write_to_csv('russian.csv', cities)


if __name__ == '__main__':
    main()
