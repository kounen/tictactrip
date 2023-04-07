import requests
import os
from dotenv import load_dotenv
import pandas as pd
from travels import get_duration
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Load .env variables
load_dotenv()

# Get distance using 'Google Maps - Distance Matrix API'
def get_distance_with_googlemaps(origin: tuple, destination: tuple, mode: str):
    # Format mode
    if mode == 'bus' or mode == 'car' or mode == 'carpooling':
        mode = 'driving' # For car
    else:
        mode = 'transit' # For train

    # Get Google Map API key from .env
    GOOGLE_MAP_API_KEY = os.getenv('GOOGLE_MAP_API_KEY')
    # URL composition
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&"\
        f"mode={mode}&"\
        f"origins={origin['latitude']},{origin['longitude']}&"\
        f"destinations={destination['latitude']},{destination['longitude']}&"\
        f"key={GOOGLE_MAP_API_KEY}"
    # Make the request and get response
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as error:
        return -1
    # Parse response JSON to get the distance in meters
    try:
        distance = response.json()['rows'][0]['elements'][0]['distance']['value']
    except IndexError as error:
        return -1
    # Return distance in kilometers
    return distance / 1000

# Read CSV files into dataframes
tickets_df = pd.read_csv('ticket_data.csv')
cities_df = pd.read_csv('cities.csv')
providers_df = pd.read_csv('providers.csv')

# Remove unused columns
tickets_df = tickets_df.drop(columns = ['id', 'o_station', 'd_station', 'search_ts', 'other_companies', 'middle_stations'])

# Compute travel duration in hours
tickets_df['duration'] = tickets_df.progress_apply(
    lambda x: get_duration(x['departure_ts'], x['arrival_ts']).total_seconds() / 3600,
    axis = 1)

# Adding provider type in tickets dataframe
# For this, we first create a dictionary combining ID and corresponding provider type from provider CSV
dict_providers = providers_df.set_index('id')['transport_type'].to_dict()
# Next step, mapping each ID from company column to his corresponding type
# Add for each line the provider type (ex: bus, train, car, carpooling)
tickets_df['provider'] = tickets_df['company'].map(dict_providers)

# Adding cities' latitude and longitude in tickets dataframe
# For this, we first create a dictionary combining ID and corresponding city latitude/longitude from cities CSV
dict_cities = cities_df.set_index('id')[['latitude', 'longitude']].to_dict('index')
# Next step, mapping each ID from o_city and d_city columns to his corresponding latitude/longitude
# Add for each line the cities' latitude/longitude
# Adding them into two new columns : o_coordinates and d_coordinates
tickets_df['o_coordinates'] = tickets_df['o_city'].map(dict_cities)
tickets_df['d_coordinates'] = tickets_df['d_city'].map(dict_cities)

## Compute travel distance
## Using 'Google Maps - Distance Matrix API'
# More accurate because specific to the transport mode
# Too slow for this amount of data
# tickets_df['distance'] = tickets_df.progress_apply(
#     lambda x: get_distance_with_googlemaps(x['o_coordinates'], x['d_coordinates'], x['provider']),
#     axis = 1)
## Using geopy library
# Faster because the distance is calculated as the crow flies
tickets_df['distance'] = tickets_df.progress_apply(
    lambda x: geodesic(
        (x['o_coordinates']['latitude'], x['o_coordinates']['longitude']),
        (x['d_coordinates']['latitude'], x['d_coordinates']['longitude'])
        ).km,
    axis = 1).round()

# Convert cents price in euros price
# Load results in new column : price_in_euros
tickets_df['price_in_euros'] = tickets_df.progress_apply(lambda x: x['price_in_cents'] / 100, axis = 1)

# Remove unused columns and rename tickets_df in distances_df
distances_df = tickets_df.drop(columns = [
    'company',
    'departure_ts',
    'arrival_ts',
    'o_city',
    'd_city',
    'o_coordinates',
    'd_coordinates',
    'price_in_cents'])

# Save result into new csv file
distances_df.to_csv('distances.csv', index=False)

# Define the distance intervals for future analysis
# Create a list : [0, 100, 200, 300, ..., 1800, 1900, 2000]
distance_intervals = list(range(0, 2001, 100))

# Create a new column in distances dataframe to indicate the distance interval for each travel
distances_df['distance_interval'] = pd.cut(distances_df['distance'], distance_intervals)
distances_df['distance_interval'] = distances_df.progress_apply(lambda x: x['distance_interval'].right, axis = 1)

######################################################################################
############################### TRAVEL PRICE ANALYSIS ################################
######################################################################################

# Calculate the median price for each travel provider in each distance interval
# Store results in a new dataframe which will be used for future visualization
median_prices = distances_df.groupby(['distance_interval', 'provider'])['price_in_euros'].median()

# Unstack the provider column
# Allow us to create a separate column for each provider's median price in each distance interval
# This new dataframe representation will be more suitable for bar chart visualization
median_prices = median_prices.unstack()

# Create a bar chart to compare the median prices for each provider in each distance interval
# rot = 0 sets the rotation angle of the x-axis tick labels to 0 degrees, meaning that the labels will be horizontal
prices_chart = median_prices.plot.bar(rot = 0)

# Set the title and axis labels
prices_chart.set_title("Median Travel Prices by Distance Interval and Provider")
prices_chart.set_xlabel("Distance Interval (km)")
prices_chart.set_ylabel("Median Price (euros)")

######################################################################################
############################## TRAVEL DURATION ANALYSIS ##############################
######################################################################################

# Calculate the median duration for each travel provider in each distance interval
# Store results in a new dataframe which will be used for future visualization
median_duration = distances_df.groupby(['distance_interval', 'provider'])['duration'].median()

# Unstack the provider column
# Allow us to create a separate column for each provider's median duration in each distance interval
# This new dataframe representation will be more suitable for bar chart visualization
median_duration = median_duration.unstack()

# Create a bar chart to compare the median durations for each provider in each distance interval
# rot = 0 sets the rotation angle of the x-axis tick labels to 0 degrees, meaning that the labels will be horizontal
durations_chart = median_duration.plot.bar(rot = 0)

# Set the title and axis labels
durations_chart.set_title("Median Travel Durations by Distance Interval and Provider")
durations_chart.set_xlabel("Distance Interval (km)")
durations_chart.set_ylabel("Median Duration (hours)")

######################################################################################
################################# BAR CHARTS CREATION ################################
######################################################################################

# Rotate X axis ticks by 45° (without this, ticks value overlay occurs)
plt.xticks(rotation = 45)

# Resize the bar chart to not crop any legend/value
plt.tight_layout()

# Create the prices bar chart
prices_figure = prices_chart.get_figure()
prices_figure.savefig('median_travel_prices.png')

# Create the durations bar chart
durations_figure = durations_chart.get_figure()
durations_figure.savefig('median_travel_durations.png')