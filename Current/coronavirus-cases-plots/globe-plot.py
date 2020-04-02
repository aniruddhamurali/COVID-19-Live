import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from datetime import date 
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 1)
#print(yesterday)  


countries = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

# List of countries
country_list = ['Afghanistan','Angola','Albania','Argentina','Armenia','Australia'
,'Austria','Azerbaijan','Burundi','Belgium','Benin','Burkina Faso','Bangladesh','Bulgaria'
,'Bahrain','Bosnia and Herzegovina','Belarus','Belize','Bolivia','Brazil','Barbados','Brunei Darussalam'
,'Bhutan','Botswana','Central African Republic','Canada','Switzerland','Chile','China','Cameroon'
,'Congo','Colombia','Comoros','Cabo Verde','Costa Rica','Cuba','Cyprus','Czech Republic','Germany'
,'Denmark','Dominican Republic','Algeria','Ecuador','Egypt','Spain','Estonia','Ethiopia','Finland','Fiji'
,'France','Gabon','United Kingdom','Georgia','Ghana','Guinea','Greece','Guatemala','Guyana','Hong Kong'
,'Honduras','Croatia','Haiti','Hungary','Indonesia','India','Ireland','Iran','Iraq','Iceland','Israel'
,'Italy','Jamaica','Jordan','Japan','Kazakhstan','Kenya','Cambodia','Korea, Rep.','Kuwait','Lebanon','Liberia'
,'Libya','Sri Lanka','Lesotho','Lithuania','Luxembourg','Latvia','Macao','Morocco','Moldova','Madagascar'
,'Maldives','Mexico','Macedonia','Mali','Malta','Myanmar','Montenegro','Mongolia','Mozambique','Mauritania'
,'Mauritius','Malawi','Malaysia','North America','Namibia','Niger','Nigeria','Nicaragua','Netherlands'
,'Norway','Nepal','New Zealand   ','Oman','Pakistan','Panama','Peru','Philippines','Papua New Guinea'
,'Poland','Puerto Rico','Portugal','Paraguay','Qatar','Romania','Russian Federation','Rwanda','Saudi Arabia'
,'Sudan','Senegal','Singapore','Solomon Islands','Sierra Leone','El Salvador','Somalia','Serbia','Slovenia'
,'Sweden','Swaziland','Syrian Arab Republic','Chad','Togo','Thailand','Tajikistan','Turkmenistan','Timor-Leste'
,'Trinidad and Tobago','Tunisia','Turkey','Tanzania','Uganda','Ukraine','Uruguay','United States','Uzbekistan'
,'Venezuela, RB','Vietnam','Yemen, Rep.','South Africa','Congo, Dem. Rep.','Zambia','Zimbabwe'
]

# Create a new dataframe with our cleaned country list
dates = countries['Date'].unique().tolist()
countries_cleaned = countries.groupby('Country/Region')
countries_grouped = list(countries_cleaned)

columns = ['Country/Region', 'Province/State', 'Lat', 'Long'] + dates
df = pd.DataFrame(columns=columns)

index = 0
for country in countries_grouped:    
    df.append(pd.Series(name=index))
    df.at[index, 'Country/Region'] = country[1]['Country/Region'].unique()[0]
    df.at[index, 'Province/State'] = country[1]['Province/State'].unique()[0]
    df.at[index, 'Lat'] = country[1]['Lat'].unique()[0]
    df.at[index, 'Long'] = country[1]['Long'].unique()[0]

    for date in dates:
        dateIndex = (country[1].index[country[1]['Date'] == date][0]) % len(dates)
        cases = country[1]['Confirmed'].iloc[dateIndex] + 1 # +1 is to avoid 0s
        df.at[index, date] = cases

    index += 1



datesWithData = list(df.columns)[4:]


# Generate world plots for Coronavirus
metricscale1=[[0, 'rgb(102,194,165)'], [0.05, 'rgb(102,194,165)'], [0.15, 'rgb(171,221,164)'], [0.2, 'rgb(230,245,152)'], [0.25, 'rgb(255,255,191)'], [0.35, 'rgb(254,224,139)'], [0.45, 'rgb(253,174,97)'], [0.55, 'rgb(213,62,79)'], [1.0, 'rgb(158,1,66)']]

dataSlider = []
for date in datesWithData:
    data_one_day = dict(
        name = date,
        type = 'choropleth',
        autocolorscale = False,
        colorscale = metricscale1,
        showscale = True,
        locations = df['Country/Region'].values,
        z = np.log10((df[date].values).astype(np.float64)),
        locationmode = 'country names',
        marker = dict(
            line = dict(color = 'rgb(250,250,225)', 
            width = 0.5)
        ),
        colorbar = dict(
            autotick = True, 
            tickprefix = '',
            title = 'Number of cases'
        )
    )
    dataSlider.append(data_one_day)

steps = []
for i in range(len(dataSlider)):
    step = dict(method='restyle',
                args=['visible', [False] * len(dataSlider)],
                label=dataSlider[i]['name'])
    step['args'][1][i] = True
    steps.append(step)

sliders = [dict(active=0,
                pad={"t": 10},
                steps=steps)] 

layout = dict(
    title = 'World Map of Global Confirmed Cases of Coronavirus',
    geo = dict(
        showframe = True,
        showocean = True,
        oceancolor = 'rgb(28,107,160)',
        projection = dict(
            type = 'orthographic',
                rotation = dict(
                    lon = 60,
                    lat = 10),
        ),
        lonaxis =  dict(
            showgrid = False,
            gridcolor = 'rgb(102, 102, 102)'
        ),
        lataxis = dict(
            showgrid = False,
            gridcolor = 'rgb(102, 102, 102)'
        )
    ),
    sliders = sliders
)
fig = dict(data=dataSlider, layout=layout)
py.plot(fig, validate=False, filename='global-coronavirus-cases')
