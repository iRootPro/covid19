import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd 

def get_html(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_total_covid(soup):
    div_total = soup.find_all('div', class_='maincounter-number')
    total_cases = div_total[0].find('span').get_text()
    total_deaths = div_total[1].find('span').get_text()
    total_recovery = div_total[2].find('span').get_text()
    return total_cases, total_deaths, total_recovery


def get_from_countries_covid(soup, top):
    table = soup.find('table', id='main_table_countries_today').find('tbody')
    trs = table.find_all('tr')

    table_data = [['Страна', 'Заболевших',
                   'Новых заболевших', 'Умерших', 'Новых умерших']]
    text = ''
    data = []
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
            text += f'{country}: {cases} заболевших \n\n'
            data.append([country, cases, deaths])
        if 'Russia' in table_data:
            break
        if 'Russia' in country:
            table_data.append([country, cases, new_cases, deaths, new_deaths])
            text += f'{country}: {cases} заболевших \n\n'
            data.append([country, cases, deaths])
    text += 'Если у вас есть предложение по функционалу, пишите @iRootPro.\nTelegram-канал о здоровье @health_life, instagram ЗОЖ в картинках https://instagram.com/iroot'
    return data

def get_country(location):
    countries = pd.read_csv('db/current_countries.csv', delimiter=';', names=['Data', 'Location', 'Case', 'Death', 'Recovered'])
    country = countries[countries.Location == location]
    country_case = country.Case.tolist()[0]
    country_death = country.Death.tolist()[0]
    country_recovered = country.Recovered.tolist()[0]

    return country_case, country_death, country_recovered

