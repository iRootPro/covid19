import plotly.express as px
import pandas as pd
import datetime

def get_date_and_time():
	today = datetime.datetime.today()
	date_and_time_today = today.strftime("%d.%m.%Y %H:%M")
	return date_and_time_today

def create_graph(table):
	df = pd.DataFrame(table, columns=['Страны', 'Cases', 'Deaths'])

	fig = px.bar(df, x = "Cases", y = "Страны", 
		title=f"Зараженные COVID-19. TOP20 + RU {get_date_and_time()}", 
		orientation='h',
		hover_data=['Deaths'], text='Cases',
		height=800, width=600
		)
	fig.update_traces(textposition='auto')
	fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
	fig.write_image("cases_top20.png")

def create_graph_deaths(table):
	df = pd.DataFrame(table, columns=['Страны', 'Cases', 'Deaths'])
	 
	fig = px.bar(df, x = "Deaths", y = "Страны",
		title=f"Умершие от COVID-19. {get_date_and_time()}",
		orientation='h', text='Deaths',
		height=800, width=600
		)
	fig.update_traces(textposition='auto')
	fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
	fig.write_image("deaths.png")