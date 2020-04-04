import plotly.express as px
import pandas as pd
import datetime

import parse


def get_date_and_time():
    today = datetime.datetime.today()
    date_and_time_today = today.strftime("%d.%m.%Y %H:%M")
    return date_and_time_today


def create_graph_cases():
    countries = pd.read_csv('db/current_countries.csv', delimiter=';',
                            thousands=',', names=['Data', 'Location', 'Case', 'Death', 'Recovered'])
    top20_case = countries[1:21]

    fig = px.bar(top20_case, x=top20_case.Case, y=top20_case.Location, title=f"Зараженные COVID-19. TOP20", orientation='h',
                 height=800, width=600, text=top20_case.Case)
    fig.update_traces(textposition='auto')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.write_image("cases_top20.png")


def create_graph_deaths():
    countries = pd.read_csv('db/current_countries.csv', delimiter=';',
                            thousands=',', names=['Data', 'Location', 'Case', 'Death', 'Recovered'])
    countries.fillna(0, inplace=True)
    top20_death = countries.sort_values('Death', ascending=False)[1:21]

    death_fig = px.bar(top20_death, x=top20_death.Death, y=top20_death.Location, title=f"Умершие от COVID-19.\nTOP20 стран", orientation='h',
                       height=800, width=600, text=top20_death.Death)
    death_fig.update_traces(textposition='auto')
    death_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    death_fig.write_image("deaths.png")


def main():
    create_graph_cases()
    create_graph_deaths()


if __name__ == '__main__':
    main()
