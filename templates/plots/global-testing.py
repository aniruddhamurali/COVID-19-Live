import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd

from datetime import date 
from datetime import timedelta



df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-latest-data-source-details.csv")

today = date.today()
yesterday = today - timedelta(days = 1)
#df = df.loc[df['Date'] == yesterday]

# Creating two subplots
fig = make_subplots(rows = 1, cols = 2, 
                    specs = [[{}, {}]], 
                    shared_xaxes = True,
                    shared_yaxes = False, 
                    vertical_spacing = 0.001)

fig.append_trace(go.Bar(
    x = df['Cumulative total per thousand'],
    y = df['Entity'],
    marker = dict(
        color = 'rgba(50, 171, 96, 0.6)',
        line = dict(
            color = 'rgba(50, 171, 96, 1.0)',
            width = 1),
    ),
    name = 'Cumulative total of COVID-19 tests done per 1 thousand people',
    orientation = 'h',
), 1, 1)

fig.append_trace(go.Scatter(
    x = df['Daily change in cumulative total per thousand'], 
    y = df['Entity'],
    mode = 'lines+markers',
    line_color = 'rgb(128, 0, 128)',
    name = 'Daily change in cumulative total of COVID-19 tests done per 1 thousand people',
    connectgaps = True,
), 1, 2)

fig.update_layout(
    title = 'Cumulative Totals and Daily Changes in COVID-19 Testing',
    yaxis = dict(
        showgrid = False,
        showline = False,
        showticklabels = True,
        domain = [0, 0.85],
    ),
    yaxis2 = dict(
        showgrid = False,
        showline = True,
        showticklabels = False,
        linecolor = 'rgba(102, 102, 102, 0.8)',
        linewidth = 2,
        domain = [0, 0.85],
    ),
    xaxis = dict(
        zeroline = False,
        showline = False,
        showticklabels = True,
        showgrid = True,
        domain = [0, 0.42],
    ),
    xaxis2 = dict(
        zeroline = False,
        showline = False,
        showticklabels = True,
        showgrid = True,
        domain = [0.47, 1],
        side = 'top',
        dtick = 0.2,
    ),
    legend = dict(x = 0.029, y = 1.038, font_size = 10),
    margin = dict(l = 100, r = 20, t = 70, b = 70),
    paper_bgcolor = 'rgb(248, 248, 255)',
    plot_bgcolor = 'rgb(248, 248, 255)',
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
                        x = -0.2, y = -0.109,
                        text='Note: Some countries do not have data on daily changes in the ' +
                             'total number of people tested per thousand people',
                        font = dict(family = 'Arial', 
                                    size = 10, 
                                    color = 'rgb(150,150,150)'),
                        showarrow = False))

fig.update_layout(annotations=annotations)

fig.show()