import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as py

import numpy as np
import pandas as pd


def run():
    # Read csv from raw Github CSV file
    df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-latest-data-source-details.csv")
    df['Country'] = [e.split('-')[0] for e in df['Entity']]

    # Creating two subplots
    fig = make_subplots(rows = 1, cols = 2, 
                        specs = [[{}, {}]], 
                        shared_xaxes = True,
                        shared_yaxes = True, 
                        vertical_spacing = 0.001)

    # Add first subplot with bar graph
    fig.append_trace(go.Bar(
        # x and y axes are switched to make graph horizontal
        x = df['Cumulative total per thousand'],
        y = df['Country'],
        marker = dict(
            color = 'rgba(37, 167, 247, 0.7)',
            line = dict(
                color = 'rgba(37, 167, 247, 1.0)',
                width = 1),
        ),
        name = 'Cumulative total of COVID-19 tests <br>done per 1000 people',
        orientation = 'h',
    ), 1, 1)

    # Add second subplot with line graph
    fig.append_trace(go.Scatter(
        x = df['Daily change in cumulative total per thousand'], 
        y = df['Country'],
        mode = 'lines+markers',
        line_color = 'rgb(245, 141, 66)',
        name = 'Daily change in cumulative total of <br>COVID-19 tests done per 1000 people',
        connectgaps = True, # Show line straight through countries that don't have this data available
        marker = dict(size = 7)
    ), 1, 2)


    # Configure layout of subplots
    fig.update_layout(
        title = 'Cumulative Totals and Daily Changes in COVID-19 Testing',
        title_x = 0.5,
        # y-axis of first subplot
        yaxis = dict(
            showgrid = True,
            showline = False,
            showticklabels = True,
            domain = [0.1, 0.95],
            uirevision = dict(
                editable = False
            ),
            fixedrange = True,
        ),
        # y-axis of second subplot
        yaxis2 = dict(
            showgrid = True,
            showline = True,
            showticklabels = False,
            domain = [0.1, 0.95],
            #fixedrange = True,
        ),
        # x-axis of first subplot
        xaxis = dict(
            zeroline = False,
            showline = False,
            showticklabels = True,
            showgrid = True,
            domain = [0.05, 0.43],
            side = 'top',
            dtick = 40,
            fixedrange = True,
            uirevision = dict(
                editable = False
            )
        ),
        # x-axis of second subplot
        xaxis2 = dict(
            zeroline = False,
            showline = False,
            showticklabels = True,
            showgrid = True,
            domain = [0.46, 0.95],
            side = 'top',
            dtick = 1,
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

    # Note on bottom of plot
    annotations.append(dict(xref = 'paper', yref = 'paper',
                            x = 0.5, y = 0.06,
                            text = 'Note: Some countries do not have data on daily changes in the ' +
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

    py.plot(fig, config={"displayModeBar": False}, validate=False, filename='./templates/plots/testing-plots', auto_open=False)
    #py.plot(fig, validate=False, filename='testing-plots', include_plotlyjs=False, output_type='div')

run()