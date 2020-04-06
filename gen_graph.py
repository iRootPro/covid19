import plotly.express as px
import plotly.graph_objs as go
import plotly.offline as pyo
import pandas as pd
import datetime
import plotly
import time

import parse


def get_date_and_time():
    today = datetime.datetime.today()
    date_and_time_today = today.strftime("%d.%m.%Y %H:%M")
    return date_and_time_today


def create_graph_top10():
    countries = pd.read_csv('db/current_countries.csv', delimiter=';',
                            thousands=',', names=['Data', 'Location', 'Case', 'Death', 'Recovered'])
    top10 = countries[1:11]
    fig1 = go.Figure(
        data=[
            go.Bar(
                x=top10['Case'],
                y=top10['Location'],
                name='Case',
                marker=dict(color='#e74c3c'),
                orientation='h',
                textposition='auto',
                text=top10['Case']

            ),
            go.Bar(
                x=top10['Death'],
                y=top10['Location'],
                name='Death',
                marker=dict(color='black'),
                orientation='h',
                textposition='auto',
                text=top10['Death']

            ),
            go.Bar(
                x=top10['Recovered'],
                y=top10['Location'],
                name='Recovered',
                marker=dict(color='green'),
                orientation='h',
                textposition='auto',
                text=top10['Recovered']
            )
        ],
        layout=go.Layout(
            title='TOP-10 стран COVID-19'
        )
    )
    fig1.update_layout(width=600, height=800, uniformtext_minsize=8,
                       uniformtext_mode='hide', barmode='group')
    fig1.write_image("top10.png")


def main():
    create_graph_top10()



if __name__ == '__main__':
	plotly.io.orca.ensure_server()
	time.sleep(10)
    main()
