#%%
import pandas as pd
import numpy as np
import altair as alt
#%%
#Read in the Data into "flights"
URL = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json"
flights = pd.read_json(URL)
flights
#%%
## GRAND QUESTION 1
#Creates a chart that sums up Total flights, delays, and average delay time in hours.
worst_delay = (flights.groupby('airport_code')
    .agg(
        total_delays = ('num_of_delays_total', np.sum),
        total_flights = ('num_of_flights_total', np.sum),
        average_delay_time = ('minutes_delayed_total', np.mean))
    #This creates new columns for the following agg functions    
    .assign(
        average_delay_hours = lambda x: (x.average_delay_time / 60).round(2),
        proportion_delay = lambda x: (x.total_delays / x.total_flights * 100).round(2))
    .filter(['airport_code', 'total_flights', 'total_delays', 'proportion_delay', 'average_delay_hours'])
    .sort_values(by = ['average_delay_hours'], ascending = False)
    .reset_index())
#%%
#A bar chart that shows the airports with the desired columns. 
worst_chart = (alt.Chart(worst_delay)
    .encode(
        alt.X('airport_code', sort=alt.EncodingSortField(field='airport_code', op='count')),
        y = 'average_delay_hours')
    .mark_bar())
#%%
# Creates markdown table
print(worst_delay
    .head(20)
    .to_markdown(index=False))
#%%
#Some months had the value "n/a". These were replaced with "Unkown" and replaces
#all weird numbers with nan in late aircraft for Grand Question 3 - 4
flights_clean = (flights.replace(to_replace = 'n/a', value = 'Unknown')
    .assign(
        num_of_delays_late_aircraft = lambda x: np.where(x.num_of_delays_late_aircraft < 0, np.nan, x.num_of_delays_late_aircraft)
    ))
#%%
## GRAND QUESTION 2
# Finds total delays by month. Excludes unknown months
worst_month = (flights_clean.filter(['month', 'num_of_delays_total'])
    .groupby('month')
    .agg(
        total_delays = ('num_of_delays_total', np.sum)
    )
    .query('month != "Unknown"')
    .reset_index())
worst_month
#%%
# Chart showing what months have the most total delays
month_chart = (alt.Chart(worst_month)
    .encode(
        alt.Y('total_delays', title='Number of Delays'),
        alt.X('month:O', sort=['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            title='Month'))
    .mark_bar())

#%%
# Boxplot to show the averages
month_box = (alt.Chart(flights_clean)
    .encode(
        alt.Y('num_of_delays_total', title='Number of Delays'),
        alt.X('month:O', sort=['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            title='Month'))
    .mark_boxplot()
    )
#%%
# Table showing the total amount of delays per month.
print(worst_month
    .head(20)
    .sort_values(by="total_delays", ascending = False)
    .to_markdown(index=False))
#%%
## GRAND QUESTION 3
# Takes all weather, nas, and late aircraft delays. Takes 30% of late_aircraft into new column. Takes 40% of nas if in months april - august
# and 65% during any other month.
weather_delays = (flights_clean.filter(["month","num_of_delays_weather", "num_of_delays_late_aircraft", "num_of_delays_nas"]))
conditions = [(weather_delays['month'] == "April") | (weather_delays['month'] == "May") | (weather_delays['month'] == "June") | (weather_delays['month'] == "July") | (weather_delays['month'] == "August")]
choices = [weather_delays['num_of_delays_nas'] * .4]
weather_delays['nas_mild_weather'] = np.select(conditions, choices, default = weather_delays['num_of_delays_nas'] * .65)
fixed_weather = (weather_delays.filter(['num_of_delays_weather', 'num_of_delays_late_aircraft', 'nas_mild_weather'])
    .assign(
      late_aircraft_mild_weather = lambda x: (x.num_of_delays_late_aircraft * .3)  
    )
    .filter(['num_of_delays_weather', 'late_aircraft_mild_weather', 'nas_mild_weather']))
fixed_weather
#%%
# puts the sums into a table
Total_weather_delays = (fixed_weather.sum(axis=0))
Total_weather_delays.loc['Total'] = Total_weather_delays.sum(axis=0)
Total_weather_delays
#%%
# Create Table for Markdown
print(Total_weather_delays
    .head(20)
    .to_markdown(index=True, tablefmt="pretty"))
#%%
## GRAND QUESTION 4
# Does the same as above but adds a column for the totals and adds totals per aiport code.
weather_delays_chart = (flights_clean.filter(["airport_code", "month","num_of_delays_weather", "num_of_delays_late_aircraft", "num_of_delays_nas"]))
conditions = [(weather_delays['month'] == "April") | (weather_delays['month'] == "May") | (weather_delays['month'] == "June") | (weather_delays['month'] == "July") | (weather_delays['month'] == "August")]
choices = [weather_delays['num_of_delays_nas'] * .4]
weather_delays_chart['nas_mild_weather'] = np.select(conditions, choices, default = weather_delays['num_of_delays_nas'] * .65)
fixed_weather_chart = (weather_delays_chart.filter(['airport_code', 'num_of_delays_weather', 'num_of_delays_late_aircraft', 'nas_mild_weather'])
    .assign(
      late_aircraft_mild_weather = lambda x: (x.num_of_delays_late_aircraft * .3),
      Totals = lambda x: (x.num_of_delays_weather + x.late_aircraft_mild_weather + x.nas_mild_weather) 
    )
    .filter(['airport_code', 'Totals'])
    .groupby('airport_code')
    .agg(
        airport_weather_delay = ('Totals', np.sum)
    )
    .reset_index())
fixed_weather_chart
#%%
# Bar chart to display the above
weather_chart = (alt.Chart(fixed_weather_chart)
    .encode(
        alt.X('airport_code', title = "Airport Code"),
        alt.Y('airport_weather_delay', title = "Total Number of Delays")
    )
    .mark_bar())
#%%
# Print table for markdown
print(fixed_weather_chart
    .head(20)
    .to_markdown(index = False))
#%%
quiz = flights["year"].isna().sum()
quiz
#%%
