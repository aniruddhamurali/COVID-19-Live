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

# Create a new dataframe with our cleaned country list
dates = countries['Date'].unique().tolist()
countries_cleaned = countries.groupby('Country/Region')
countries_grouped = list(countries_cleaned)


columns = ['Date', 'Country/Region', 'Lat', 'Long', 'ISO_Codes', 'Confirmed']
df = pd.DataFrame(columns=columns)


index = 0
for country in countries_grouped:
    country_data = country[1]
    eachDate = list(country_data.groupby("Date"))
    
    for date in eachDate:
        date_data = date[1]
        df.append(pd.Series(name=index))
        
        df.at[index, 'Date'] = date[0] #country_data['Date'].iloc[index % len(date_data)]
        df.at[index, 'Country/Region'] = country_data['Country/Region'].iloc[index % len(date_data)]
        df.at[index, 'Lat'] = country_data['Lat'].iloc[index % len(date_data)]
        df.at[index, 'Long'] = country_data['Long'].iloc[index % len(date_data)]
        df.at[index, 'ISO_Codes'] = country_data['ISO_Codes'].iloc[index % len(date_data)]
        
        cases = date_data['Confirmed'].sum()
        df.at[index, 'Confirmed'] = cases

        index += 1


fig = px.scatter_geo(df, locations="ISO_Codes", hover_name="Country/Region", 
                                size=df["Confirmed"].astype(int), size_max=50,
                                animation_frame="Date", projection="natural earth")
fig.show()
py.plot(fig, validate=False, filename='global-bubble-map')
