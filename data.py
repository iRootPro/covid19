import requests
from bs4 import BeautifulSoup
import os
import csv
import datetime


def get_date():
    today = datetime.datetime.today()
    date_today = today.strftime("%d.%m.%Y")
    return date_today

def write_to_csv(filename, data):
    if not os.path.exists('db'):
        os.makedirs('db')
    with open(f'db/{filename}', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)


def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_total_covid(soup):
    div_total = soup.find_all('div', class_='maincounter-number')
    total_cases = div_total[0].find('span').get_text().strip()
    total_deaths = div_total[1].find('span').get_text().strip()
    total_recovery = div_total[2].find('span').get_text().strip()
    today = get_date()
    total = [[today, total_cases, total_deaths, total_recovery]]
    return total


def get_from_countries_covid(soup):
    table = soup.find('table', id='main_table_countries_today').find('tbody')
    trs = table.find_all('tr')
    today = get_date()
    text = ''
    data = []
    for tr in trs:
        tds = tr.find_all('td')
        if tds[0].find('a'):
            country = tds[0].find('a').get_text().strip()
        else:
            country = tds[0].get_text().strip()
        cases = tds[1].get_text().strip()
        deaths = tds[3].get_text().strip()
        recovered = tds[5].get_text().strip()
        data.append([today, country, cases, deaths, recovered])

    return data

def main():
    url = 'https://www.worldometers.info/coronavirus/'
    total = get_total_covid(get_html(url))
    write_to_csv('total.csv', total)
    data_all_countries = get_from_countries_covid(get_html(url))
    write_to_csv('countries.csv', data_all_countries)


if __name__ == '__main__':
    main()