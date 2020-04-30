import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as py

import numpy as np
import pandas as pd

from datetime import date 
from datetime import timedelta

today = date.today()
yesterday = today - timedelta(days = 1)


def run():
    df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-latest-data-source-details.csv")
    df['Country'] = [e.split('-')[0] for e in df['Entity']]

    # Creating two subplots
    fig = make_subplots(rows = 1, cols = 2, 
                        specs = [[{}, {}]], 
                        shared_xaxes = True,
                        shared_yaxes = True, 
                        vertical_spacing = 0.001)

    fig.append_trace(go.Bar(
        x = df['Cumulative total per thousand'],
        y = df['Country'],
        marker = dict(
            color = 'rgba(37, 167, 247, 0.7)',
            line = dict(
                color = 'rgba(37, 167, 247, 1.0)',
                width = 1),
        ),
        name = 'Cumulative total of COVID-19 tests done per 1 thousand people',
        orientation = 'h',
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x = df['Daily change in cumulative total per thousand'], 
        y = df['Country'],
        mode = 'lines+markers',
        line_color = 'rgb(245, 141, 66)',
        name = 'Daily change in cumulative total of COVID-19 tests done per 1 thousand people',
        connectgaps = True,
        marker = dict(size = 7)
    ), 1, 2)

    fig.update_layout(
        title = 'Cumulative Totals and Daily Changes in COVID-19 Testing',
        title_x = 0.5,
        yaxis = dict(
            showgrid = True,
            showline = False,
            showticklabels = True,
            domain = [0.1, 0.95],
        ),
        yaxis2 = dict(
            showgrid = True,
            showline = True,
            showticklabels = False,
            domain = [0.1, 0.95],
        ),
        xaxis = dict(
            zeroline = False,
            showline = False,
            showticklabels = True,
            showgrid = True,
            domain = [0.05, 0.43],
            side = 'top',
            dtick = 10,
            fixedrange = True
        ),
        xaxis2 = dict(
            zeroline = False,
            showline = False,
            showticklabels = True,
            showgrid = True,
            domain = [0.46, 0.95],
            side = 'top',
            dtick = 0.2,
            fixedrange = True
        ),
        legend = dict(x = 0.32, y = 1.01, font_size = 12),
        margin = dict(l = 100, r = 20, t = 70, b = 0),
        template = "plotly_dark"
    )


    annotations = []
    # Round all numbers to 3 decimal places
    total_per = np.round(df['Cumulative total per thousand'], decimals = 3)
    delta_per = np.round(df['Daily change in cumulative total per thousand'], decimals = 3)

    '''
    for ydn, yd, xd in zip(delta_per, total_per, df['Entity']):
        # labeling daily change in cumulative total per thousand
        annotations.append(dict(xref = 'x1', yref = 'y1',
                                y = xd, x = yd,
                                text = str(yd),
                                font = dict(family = 'Arial', 
                                            size = 12,
                                            color = 'rgb(50, 171, 96)'
                                            ),
                                showarrow = False))
        # labeling cumulative total per thousand
        annotations.append(dict(xref = 'x2', yref = 'y2',
                                y = xd, x = ydn,
                                text = str(ydn),
                                font = dict(family = 'Arial', 
                                            size = 12,
                                            color = 'rgb(128, 0, 128)'),
                                showarrow = False))
    '''

    # Note
    annotations.append(dict(xref = 'paper', yref = 'paper',
                            x = 0.5, y = 0.06,
                            text='Note: Some countries do not have data on daily changes in the ' +
                                'total number of tests done per 1 thousand people and/or the cumulative ' +
                                'total number of tests done per 1 thousand people. <br>' +
                                'Some countries also had multiple sources stating different numbers of ' + 
                                'tests, so all sources are included in these plots. Look at data table for more details.',
                            font = dict(family = 'Arial', 
                                        size = 12, 
                                        color = 'rgb(225,225,225)'),
                            showarrow = False))

    fig.update_layout(annotations = annotations,
                    height = 1700)

    #fig.show()
    py.plot(fig, validate=False, filename='./templates/plots/testing-plots', auto_open=False)
    #py.plot(fig, validate=False, filename='testing-plots', include_plotlyjs=False, output_type='div')

#run()