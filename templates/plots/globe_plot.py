import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.io as pio

import seaborn as sns

import warnings
warnings.filterwarnings('ignore')


def run():
    # Read csv from raw Github CSV file
    countries = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

    # Create a new dataframe with our cleaned country list
    dates = countries['Date'].unique().tolist()
    countries_cleaned = countries.groupby('Country/Region')
    countries_grouped = list(countries_cleaned)

    columns = ['Country/Region', 'Lat', 'Long'] + dates
    df = pd.DataFrame(columns=columns)


    index = 0
    # Iterate through each country
    for country in countries_grouped:
        df.append(pd.Series(name=index))
        df.at[index, 'Country/Region'] = country[1]['Country/Region'].unique()[0]
        df.at[index, 'Lat'] = country[1]['Lat'].unique()[0]
        df.at[index, 'Long'] = country[1]['Long'].unique()[0]

        country_data = country[1]

        eachDate = list(country_data.groupby("Date"))
        
        # Iterate through each date to get cases
        for date in eachDate:
            date_data = date[1]
            cases = date_data['Confirmed'].sum() + 1
            df.at[index, date_data['Date'].iloc[0]] = cases

        index += 1

    # Data for data slider excludes first 3 columns
    datesWithData = list(df.columns)[3:]

    # Colorscale
    metricscale1=[[0, 'rgb(102,194,165)'], [0.05, 'rgb(102,194,165)'], [0.15, 'rgb(171,221,164)'], [0.2, 'rgb(230,245,152)'], [0.25, 'rgb(255,255,191)'], [0.35, 'rgb(254,224,139)'], [0.45, 'rgb(253,174,97)'], [0.55, 'rgb(213,62,79)'], [1.0, 'rgb(158,1,66)']]

    # Set data slider attributes and values for each date
    dataSlider = []
    for date in datesWithData:
        data_one_day = dict(
            name = date,
            type = 'choropleth',
            autocolorscale = False,
            colorscale = metricscale1,
            showscale = False,
            locations = df['Country/Region'].values,
            z = np.log10((df[date].values).astype(np.float64)),
            text = [f'Country: {df["Country/Region"].iloc[i]}<br>Cases : {df[date].iloc[i] - 1}' for i in range(0,len(df))],
            hoverinfo = 'text',
            locationmode = 'country names',
            marker = dict(
                line = dict(color = 'rgb(250,250,225)', 
                width = 0.5)
            ),
            colorbar = dict(
                tickprefix = '',
                title = 'Number of cases'
            )
        )
        dataSlider.append(data_one_day)

    # Create sliders
    steps = []
    for i in range(len(dataSlider)):
        step = dict(method = 'restyle',
                    args = ['visible', [False] * len(dataSlider)],
                    label = dataSlider[i]['name'])
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active = len(dataSlider) - 1,
                    pad = {"t": 10},
                    steps = steps,
                    currentvalue = {"prefix": "Date: "},
                    tickcolor = "white",
                    font = {'color':'white'},
                    bgcolor = 'white',
                    tickwidth = 1)] 

    # Set configurations for orthographic heatmap
    layout = dict(
        title = 'World Heatmap of Global Confirmed Cases of Coronavirus',
        title_x = 0.5,
        geo = dict(
            showframe = True,
            showocean = True,
            oceancolor = 'rgb(28,107,160)',
            projection = dict(
                type = 'orthographic',
                    rotation = dict(
                        lon = 60,
                        lat = 10
                    ),
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
        #sliders = sliders,
        #height = 600,
    )
    #fig = dict(data=dataSlider, layout=layout_def)
    fig = go.Figure(data = dataSlider[len(dataSlider) - 1], layout = layout)
    fig.update_layout(template="plotly_dark")

    #py.plot(fig, validate=False, filename='./templates/plots/global-coronavirus-cases', auto_open=False)
    py.plot(fig, validate=False, filename='global-coronavirus-cases', auto_open=False)

run()