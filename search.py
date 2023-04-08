# To parse script arguments
import argparse
# To handle dataframes
import pandas as pd
# To draw pie chart
import matplotlib.pyplot as plt
# To display progress bar during long operations
from tqdm.auto import tqdm
tqdm.pandas()

# Arguments checking functions
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
def is_valid_day(arg: str):
    day = str(arg)
    if not day in days:
        raise argparse.ArgumentTypeError("Day must be in letter : {}. '{}' is not.".format(days, day))
    return day

# List of all country possibilities in our dataframe
# Get with tickets_df['d_country'].unique() method after perform dataframe reading
countries = ['France', 'Belgique', 'Deutschland', 'Nederland', 'Italia', 'Schweiz', 'España',
             'United Kingdom', 'Danmark', 'Norge', 'Česko', 'Portugal', 'Sverige',
             'Slovenija', 'UK', 'България', 'Polska', 'Luxembourg', 'România', 'Hrvatska',
             'Magyarország', 'Ireland', 'Österreich', 'Црна Гора / Crna Gora', 'Slovensko']
# Sort to find possible occurrences of names
countries.sort()
# Indeed, we see 'UK' and 'United Kingdom' side by side
# Then, remove 'UK' in the list
countries.remove('UK')
# And replace every occurences of 'UK' by 'United Kingdom' in our dataframe
# => line 58

def is_valid_country(arg: str):
    country = str(arg)
    if not country in countries:
        raise argparse.ArgumentTypeError("Countries possible to analyse are : {}. '{}' is not.".format(countries, country))
    return country

# Get country and day name as script parameters
parser = argparse.ArgumentParser(description = 'Pie chart of travel searches for a given day and country')
parser.add_argument('--country', type = is_valid_country, required = True, help = 'Only {} possible'.format(countries))
parser.add_argument('--day', type = is_valid_day, required = False, help = 'Only {} possible'.format(days))
args = parser.parse_args()

# Read CSV files into dataframes
tickets_df = pd.read_csv('ticket_data.csv', usecols = ['search_ts', 'd_city'])
cities_df = pd.read_csv('cities.csv', usecols = ['id', 'local_name'])

# Adding cities' name in tickets dataframe
# For this, we first create a dictionary combining ID and corresponding city name from cities dataframe
dict_cities = cities_df.set_index('id')['local_name'].to_dict()
# Next step, mapping each ID from d_city column of tickets_df to his corresponding name
# Add for each travel the cities' name instead of cities' id
tickets_df['d_city'] = tickets_df['d_city'].map(dict_cities)

# Split city name and country name into two columns
tickets_df['d_country'] = tickets_df.progress_apply(lambda x: x['d_city'].split(',')[2].strip(), axis = 1)
tickets_df['d_country'] = tickets_df['d_country'].replace('UK', 'United Kingdom')
tickets_df['d_city'] = tickets_df.progress_apply(lambda x: x['d_city'].split(',')[0].strip(), axis = 1)

# Convert search_ts to datetime format to get day name more easily
tickets_df['search_ts'] = pd.to_datetime(tickets_df['search_ts'])

# Get only travels corresponding to the day and country specified in parameter
# Use day parameter only if it is specified by the user
filtered_df = tickets_df.loc[
    (tickets_df['d_country'] == args.country)
    & (tickets_df['search_ts'].dt.day_name() == args.day 
       if args.day is not None 
       else True
    )
]

# Count searches by destination 
searches_df = filtered_df['d_city'].value_counts()
# Give columns appropriate names
searches_df = searches_df.reset_index().rename(columns = {'index': 'destination', 'd_city': 'searches_nbr'})
# Save result into csv file
searches_df.to_csv(f"searches_{args.country}" + (f"_{args.day}" if args.day is not None else "") + ".csv", index = False)

## Remove noise data (destination where search percentage < 2)
# Compute percentage
searches_df['percentage'] = (searches_df['searches_nbr'] / searches_df['searches_nbr'].sum() * 100).round()
## Create a new dataframe specific to pie chart visualization
# Create a mask filtering only the destination with a percentage lower than 2
mask = searches_df['percentage'] < 2
# Get only the destination with percentage upper than 2 ('~' means not)
pie_df = searches_df[~mask]
# Add a new row gathering all the destinations with a searches number lower than 2% and cumulate them in one category called 'Others'
pie_df.loc[len(pie_df)] = ['Others (check csv file)', searches_df[mask]['searches_nbr'].sum(), searches_df[mask]['percentage'].sum()]

# Pie creation
pie, setup = plt.subplots()
setup.pie(pie_df['searches_nbr'], labels = pie_df['destination'], autopct = '%1.1f%%')
setup.set_title(f"Number of searches by destination in {args.country}" + (f" on {args.day}" if args.day is not None else ""))
pie.savefig(f"searches_{args.country}" + (f"_{args.day}" if args.day is not None else "") + ".png")