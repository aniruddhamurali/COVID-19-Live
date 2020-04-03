import numpy as np
import pandas as pd
import plotly.express as px
import plotly.offline as py
import country_converter as coco
import warnings
warnings.filterwarnings('ignore')

countries = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

countries = countries[countries['Confirmed'].notna()]
iso3_codes = coco.convert(names=countries['Country/Region'].tolist(), to='ISO3')

countries['ISO_Codes'] = iso3_codes
countries = countries[countries['ISO_Codes'] != 'not found']


fig = px.scatter_geo(countries, locations="ISO_Codes", hover_name="Country/Region", 
                                size="Confirmed", size_max=50,
                                animation_frame="Date", projection="natural earth")
#fig.show()
py.plot(fig, validate=False, filename='global-bubble-map')
