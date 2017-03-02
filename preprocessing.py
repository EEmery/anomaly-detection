
import pandas as pd

# Reads the data from the .csv file
columns_names = ["CITY", "GAS_STATION", "ID", "FUEL_TYPE", "COST", "DAY", "MONTH", "YEAR"]
df = pd.read_csv("Data/gas_stations_database--fixed_date.csv", names=columns_names)


# Clusters by individuals and sorts by timestamp
#print df.sort_values(['ID', 'YEAR', 'MONTH', 'DAY'], ascending=False)


# Chooses one specific ID
targetID = df['ID'] == '3649HAR'
print df[targetID].sort_values(['YEAR', 'MONTH', 'DAY'], ascending=False)