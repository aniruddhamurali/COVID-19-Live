import plotly.offline as py
import plotly.express as px

from urllib.request import urlopen
import json
import pandas as pd

from datetime import date 
from datetime import timedelta

import warnings
warnings.filterwarnings('ignore')


today = date.today()
yesterday = today - timedelta(days = 1)
yesterday = str(yesterday.month) + "/" + str(yesterday.day) + "/" + str(yesterday.year)[len(str(yesterday.year))-2:]

def run():
    # GeoJSON
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    us = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
    us = us.dropna()
    us['FIPS'] = us['FIPS'].apply(lambda x: str(int(x)).zfill(5)) # Make sure all counties FIPs are 5 digits

    fig = px.choropleth(us, 
        geojson = counties, 
        locations = 'FIPS', 
        color = yesterday,
        color_continuous_scale = "Viridis",
        range_color = (0, 300),
        scope = "usa",
        labels = {yesterday: 'Cases per County'},
        template = "plotly_dark"
    )

    fig.update_layout(
        title = 'Current Coronavirus Cases per County in the U.S.',
        title_x = 0.5,
        margin = {"r": 20, "t": 80, "l": 20, "b": 20},
        height = 600
    )
    #py.plot(fig, filename="./templates/plots/us-counties-map.html", auto_open=False)
    py.plot(fig, filename="us-counties-map.html", auto_open=False)

run()