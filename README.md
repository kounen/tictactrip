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