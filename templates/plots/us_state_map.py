import plotly.graph_objects as go
import plotly.offline as py

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from datetime import date 
from datetime import timedelta

import warnings
warnings.filterwarnings('ignore')


# Dict for US abbreviations
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


def run():
    # Read csv from raw Github CSV file
    us = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")

    states_grouped = us.groupby('Province_State').sum().reset_index()
    states = states_grouped['Province_State']

    # Get yesterday's date to display most recent county case data
    today = date.today()
    yesterday = today - timedelta(days = 1)
    yesterday = str(yesterday.month) + "/" + str(yesterday.day) + "/" + str(yesterday.year)[len(str(yesterday.year))-2:]

    # Set configurations of chloropleth map
    fig = go.Figure(data=go.Choropleth(
        locations = states.map(us_state_abbrev),
        z = states_grouped[yesterday], # Date is used as the column of dataframe
        locationmode = 'USA-states',
        colorscale = 'Reds',
        colorbar_title = "Cases per State",
        zmin = 0,
        zmax = 50000
    ))

    fig.update_layout(
        title = 'Current Coronavirus Cases per State in the U.S.',
        title_x = 0.5,
        geo_scope ='usa',
        margin = {"r": 20, "t": 80, "l": 20, "b": 20},
        height = 600,
        template = "plotly_dark"
    )

    py.plot(fig, config={"displayModeBar": False}, validate=False, filename='./templates/plots/us-cases-map', auto_open=False)

run()