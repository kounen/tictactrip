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
After that, you can open and read travels.csv file.