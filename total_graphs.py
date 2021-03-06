import numpy as np
import pandas as pd
import plotly.express as px
import plotly
import time


from graph import get_date_and_time


def main():
    total = pd.read_csv('db/total.csv', delimiter=';',
                        names=['Дата', 'Случаи', 'Умершие', 'Выздоровевшие'])
    total_cases = total[['Дата', 'Случаи']]
    cases_fig = px.line(total_cases, x='Дата', y='Случаи', height=800, width=600,
                        title=f'График по количеству зараженных COVID-19. {get_date_and_time()}')

    total_deaths = total[['Дата', 'Умершие']]
    deaths_fig = px.line(total_deaths, x='Дата', y='Умершие', height=800, width=600,
                         title=f'График по умершим от COVID-19. {get_date_and_time()}')

    total_recovered = total[['Дата', 'Выздоровевшие']]
    recovered_fig = px.line(total_recovered, x='Дата', y='Выздоровевшие', height=800, width=600,
                            title=f'График по выздоровевшим от COVID-19. {get_date_and_time()}')

    # countries = pd.read_csv('db/countries.csv', delimiter=';',
    #                         names=['Дата', 'Страна', 'Случаи', 'Умершие', 'Выздоровевшие'])
    # russia = countries[countries.Страна == 'Russia']
    # rus_case = russia[['Дата', 'Случаи']]
    # rus_fig = px.line(rus_case, x='Дата', y='Случаи', height=800, width=600,
    #                   title=f'График заражения в России. {get_date_and_time()}')

    cases_fig.write_image("total_cases.png")
    deaths_fig.write_image('total_deaths.png')
    recovered_fig.write_image('total_recovered.png')
    # rus_fig.write_image('russian_cases.png')


if __name__ == '__main__':
    plotly.io.orca.ensure_server()
    time.sleep(10)
    main()
