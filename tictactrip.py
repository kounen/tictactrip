# To handle dataframes
import pandas as pd
# For time computation
from datetime import datetime
# To display progress bar during long operations
from tqdm.auto import tqdm
tqdm.pandas()

# Read CSV files into dataframes
tickets_df = pd.read_csv('ticket_data.csv')
cities_df = pd.read_csv('cities.csv')
stations_df = pd.read_csv('stations.csv')
providers_df = pd.read_csv('providers.csv')

# Compute travel duration
def get_duration(departure_ts: str, arrival_ts: str):
    departure_time = datetime.strptime(departure_ts, "%Y-%m-%d %H:%M:%S+%f")
    arrival_time = datetime.strptime(arrival_ts, "%Y-%m-%d %H:%M:%S+%f") 
    return arrival_time - departure_time
# Add it inside tickets dataframe in a new column called 'duration'
# We use axis = 1 to loop on each dataframe line and not column (axis = 0)
tickets_df['duration'] = tickets_df.progress_apply(
    lambda x: get_duration(x['departure_ts'], x['arrival_ts']),
    axis = 1)

# Convert cents price in euros price
# Load results in new column : price_in_euros
tickets_df['price_in_euros'] = tickets_df.progress_apply(lambda x: x['price_in_cents'] / 100, axis = 1)

# Create a new dataframe containing some interesting value for each travel
# Like maximum, minimum and average price/duration for each travel connected the same cities
# We use round() to round computation results, here with two decimals
travels_df = tickets_df.groupby(['o_city', 'd_city']).agg(
    {
        'duration': ['mean', 'min', 'max'],
        'price_in_euros': ['mean', 'min', 'max'],
        'id': 'size'
    }).round(2)
# Rename each columns for better understanding
travels_df.columns = [
    'mean_duration', 'min_duration', 'max_duration',
    'mean_price', 'min_price', 'max_price',
    'count']
# Add index column to travels dataframe
# Offer us an easier handling for future operations
# Also better looking
travels_df = travels_df.reset_index()

# Adding cities' name in travels dataframe
# For this, we first create a dictionary combining ID and corresponding city name from cities dataframe
dict_cities = cities_df.set_index('id')['local_name'].to_dict()
# Next step, mapping each ID from o_city and d_city columns of travels_df to his corresponding name
# Add for each travel the cities' name
# Adding them in two new columns : origin_city and destination_city
travels_df['origin_city'] = travels_df['o_city'].map(dict_cities)
travels_df['destination_city'] = travels_df['d_city'].map(dict_cities)

# Reorder travels dataframe columns
travels_df = travels_df[['o_city',
                         'd_city',
                         'origin_city',
                         'destination_city',
                         'count',
                         'mean_duration',
                         'min_duration',
                         'max_duration', 
                         'mean_price',
                         'min_price',
                         'max_price']]

# Save result into new csv file
travels_df.to_csv('travels.csv', index=False)