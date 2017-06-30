import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

city_list = ['Indi', 'Pitt', 'Miam', 'Wash', 'Chic']

df_list = []

for city in city_list:
	df = pd.read_csv('./temp_data/{}.csv'.format(city))
	df.name = city
	df_list.append(df)

for df in df_list:
	date_index = []
	for date in df.loc[:,'DATE']:
		date_index.append((pd.to_datetime(datetime.strptime(str(date), "%Y%m%d")).dayofyear - 264) % 366)
	df.index = date_index
	if df.name == 'Chic':
		plt.plot(df.index, df['TMAX'], 'o', c='#800000', markersize=2)
		plt.plot(df.index, df['TMIN'], 'o', c='#800000', markersize=2)
	else:
		plt.plot(df.index, df['TMAX'], 'o', c='#ffcc5c', markersize=2)
		plt.plot(df.index, df['TMIN'], 'o', c='#dc6900', markersize=2)

born_info = df_list[0][df_list[0]['DATE'] == 19750122]

little_league_info = df_list[1][df_list[1]['DATE'] == 19880714]

plt.plot(born_info.index[0], born_info.iloc[0, 3], color='k', marker='o', markerfacecolor='#FFFF00')

plt.plot(little_league_info.index[0], little_league_info.iloc[0, 3], color='k', marker='o', markerfacecolor='#FFFF00')

plt.annotate('born', xy=(born_info.index[0], born_info.iloc[0, 3]), xytext=(born_info.index[0] - 100, born_info.iloc[0, 3] - 30), arrowprops=dict(facecolor='black', shrink=0.05))

plt.annotate('little league all-star team wins regional championship', xy=(little_league_info.index[0], little_league_info.iloc[0, 3]), xytext=(little_league_info.index[0] - 175, little_league_info.iloc[0, 3] + 50), arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlabel('Superposition of Years')

plt.ylabel('Fahrenheit')

plt.show()