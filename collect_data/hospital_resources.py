import pymongo
import pandas as pd

import plotly.graph_objects as go
import plotly.offline as py

client = pymongo.MongoClient("mongodb+srv://mainUser:An1ruddha@hospitalization-ptx4a.gcp.mongodb.net/test")
mydb = client['resource_data']
mycol = mydb['resources_4_27']

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

'''doc = mycol.find()
for data in doc:
    print(data['ICUbed_mean'])
'''

resources = []
columns = ['location_name', 'date', 'allbed_mean', 'ICUbed_mean', 'bedover_mean', 'icuover_mean']
df = pd.DataFrame(columns=columns)

index = 0
for data in mycol.find({"date":"2020-04-27"}):
    if data['location_name'] in us_state_abbrev.keys():
        df.append(pd.Series(name=index))
        #resources.append(data)
        df.at[index, 'location_name'] = data['location_name']
        df.at[index, 'date'] = data['date']
        df.at[index, 'allbed_mean'] = round(float(data['allbed_mean']))
        df.at[index, 'ICUbed_mean'] = data['ICUbed_mean']
        df.at[index, 'bedover_mean'] = data['bedover_mean']
        df.at[index, 'icuover_mean'] = data['icuover_mean']
        '''df2 = pd.DataFrame([[data['location_name'], data['date'], 
                            float(data['allbed_mean']), data['ICUbed_mean'],
                            data['bedover_mean'], data['icuover_mean']]], columns=columns)
        df.append(df2)'''
        index += 1


scale = 5
df['text'] = 'Average beds needed per day: ' + df['allbed_mean'].astype(str)

fig = go.Figure(data=go.Scattergeo(
        locations = df['location_name'].map(us_state_abbrev),
        #z = df['allbed_mean'],
        locationmode = 'USA-states',
        #colorscale = 'Blues',
        #colorbar_title = "Hospital Resources per State",
        #zmin = 0,
        #zmax = 50000
        marker = dict(
            size = df['allbed_mean'].astype(float)/scale,
            color = 'rgb(0,0,255)',
            #line_color='rgb(255,40,40)',
            line_width = 0.5,
            sizemode = 'area'
        ),
        text = df['text']
    ))

fig.update_layout(
    title = 'Hospital Resources per State in the U.S.',
    title_x = 0.5,
    geo_scope ='usa',
    margin = {"r": 20, "t": 80, "l": 20, "b": 20},
    height = 600,
    template = "plotly_dark"
)

#py.plot(fig, validate=False, filename='./templates/plots/us-hospital_resources', auto_open=False)
py.plot(fig, validate=False)

#print(df)

#print(resources)
