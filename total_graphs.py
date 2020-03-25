import numpy as np
import pandas as pd
import plotly.express as px


def main():
	total = pd.read_csv('db/total.csv', delimiter=';', 
		names=['Дата', 'Случаи', 'Умершие', 'Выздоровевшие'])	
	total_cases = total[['Дата', 'Случаи']]
	cases_fig = px.line(total_cases, x = 'Дата', y = 'Случаи', height = 800, width = 600, 
		title = 'График по количеству зараженных COVID-19')

	total_deaths = total[['Дата', 'Умершие']]
	deaths_fig = px.line(total_deaths, x = 'Дата', y = 'Умершие', height = 800, width = 600, 
		title = 'График по умершим от COVID-19')

	total_recovered = total[['Дата', 'Выздоровевшие']]
	recovered_fig = px.line(total_recovered, x = 'Дата', y = 'Выздоровевшие', height = 800, width = 600,
		title = 'График по выздоровевшим от COVID-19')

	cases_fig.write_image("total_cases.png")
	deaths_fig.write_image('total_deaths.png')
	total_recovered.write_image('total_recovered.png')


if __name__ == '__main__':
	main()