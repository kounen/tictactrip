# 🚄🚙🚶🏼‍♀️ TicTacTrip (_Technical test data scientist_)

## Download resources
First you need to download resource files in root directory:
- ***.env*** (containing API keys);
- ***ticket_data.csv*** : containing tickets history (one row => one result on tictactrip);
- ***cities.csv*** : cities served by tictactrip;
- ***stations.csv*** : stations served by tictactrip;
- ***providers.csv*** : providers performing travel (TGV...).

## Packages installation
First, you need python and then install the required python packages
```sh
pip3 install -r requirements.txt
```

## First script : get travels information
This first script create a CSV file containing data for each travel connecting the same cities.
For example, for all the travels connecting Paris (France) to Lyon (France), we will know the mean, minimum and maximum travel time and price. And also the number of travel suggested by tictactrip for this connection.
To run this script and create the output CSV file, type this command line in your terminal at the root directory:
```sh
python3 travels.py
```
After that, you can open and read *travels.csv* file.

## Second script : analyse prices and durations for each provider
This second script aims to provide a comparison between each provider type (bus, train, car).
After running this script, you will be able to visualize the evolution of prices (*median_travel_prices.png*) and durations (*median_travel_durations.png*) in function of travel distance for each provider.
To run this script and create the output CSV file and two bar charts, type this command line in your terminal at the root directory:
```sh
python3 distances.py
```
After that, you can open and read *distances.csv*, *median_travel_prices.png* and *median_travel_durations.png* files.
> Note: I didn't use stations.csv file in this script for two reasons.
> Despite interesting usage of stations coordinates to compute more accurate distances, I also notice some inconsistencies. Indeed, in some rows, I could note that some tickets don't have any stations specified and only cities informations were provided. Moreover, even in rows where o_station and d_station data were present, some middle_stations fields had exactly the same id that the o_station or d_station.
> The second reason is linked to the first one. Indeed even if I could compute cleverly the distances (get stations coordinates unless they were not provide, then take cities coordinates...), I didn't have enough time during this technical week (midterm exams, want to make other analysis...).

## Third script : analysis of searches number on tictactrip website by destination for a specific day and country
This script creates two files:
- one pie chart offering us a circular visualization of the number of searches on tictactrip for each destination for a given country and day;
- one csv file containing the number of searches by destination for a given country and day. Contrary to the pie chart, we will be able to consult all the destinations in this file. Indeed, I have to reduce some information in the pie chart for a better understanding (overlay between slices information). So all the destinations in a country representing less than 2% of the searches where ommited and gathered in a same slice called 'Others'.

To run this script and create the output CSV file and pie chart, type this command line in your terminal at the root directory:
```sh
python3 search.py --country España --day Friday
```
So here, we will get an analyse of the number of searches by destination in Spain for friday.
--day is optional. To get the script manual, type this command line in your terminal at the root directory:
```sh
python3 search.py --help
```
> Note: I didn't use month but day in this analysis. Simple reason : I had only the data of 2017-10... So I had to adapt my script to a day flag and not a month one.
> This script is for me interesting as a business intelligence feature. Indeed, you can use this kind of analysis to update your website according to the day. Example: if you notice after running this script that 1/3 of the destinatons searched tuesday in Spain is for Madrid, you can put a specific 'space' on tictactrip webpage to recommend this travel directly to the user. Moreover, we could even use user's IP to adapt recommendation system to his country...