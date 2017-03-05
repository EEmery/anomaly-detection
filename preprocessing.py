import pandas as pd

# Loads the data from the .csv file
columns_names = ["CITY", "GAS_STATION", "ID", "FUEL_TYPE", "COST", "DAY", "MONTH", "YEAR"]
df = pd.read_csv("Data/gas_stations_database--fixed_date.csv", names=columns_names)


# Clusters hole dataframe by individuals and sorts by timestamp
#df.sort_values(['ID', 'YEAR', 'MONTH', 'DAY'], ascending=False)


# Chooses and prints one specific ID
#targetID = df['ID'] == '741NKH'
#print df[targetID].sort_values(['YEAR', 'MONTH', 'DAY'], ascending=False)


# Creates a quarter column
df['QUARTER'] = 0
df['QUARTER'][df['MONTH'] == 1] = df['QUARTER'][df['MONTH'] == 2] = df['QUARTER'][df['MONTH'] == 3] = 1
df['QUARTER'][df['MONTH'] == 4] = df['QUARTER'][df['MONTH'] == 5] = df['QUARTER'][df['MONTH'] == 6] = 2
df['QUARTER'][df['MONTH'] == 7] = df['QUARTER'][df['MONTH'] == 8] = df['QUARTER'][df['MONTH'] == 9] = 3
df['QUARTER'][df['MONTH'] == 10] = df['QUARTER'][df['MONTH'] == 11] = df['QUARTER'][df['MONTH'] == 12] = 4

# Creates a frequency column
df['FREQUENCY'] = 1


# Groups ID's fuel consuption by month
monthly_grouped = df.groupby(['ID', 'YEAR', 'MONTH', 'FUEL_TYPE'], as_index=False).sum()

# Calculates monthly mean
monthly_grouped['MEAN'] = df.groupby(['ID', 'YEAR', 'MONTH', 'FUEL_TYPE'], as_index=False).mean()['COST']

# Calculates monthly standard deviation
monthly_grouped['STD'] = df.groupby(['ID', 'YEAR', 'MONTH', 'FUEL_TYPE']).std().reset_index(0).reset_index(drop=True)['COST']

# Cleans final dataframe
del monthly_grouped['DAY']
del monthly_grouped['QUARTER']

# Sorts dataframe
monthly_grouped = monthly_grouped.sort_values(['ID', 'YEAR', 'MONTH'], ascending=False)


# Groups ID's fuel consuption by quarter
quarterly_grouped = df.groupby(['ID', 'YEAR', 'QUARTER', 'FUEL_TYPE'], as_index=False).sum()

# Calculates quarterly mean
quarterly_grouped['MEAN'] = df.groupby(['ID', 'YEAR', 'QUARTER', 'FUEL_TYPE'], as_index=False).mean()['COST']

# Calculates quarterly standard deviation
quarterly_grouped['STD'] = df.groupby(['ID', 'YEAR', 'QUARTER', 'FUEL_TYPE']).std().reset_index(0).reset_index(drop=True)['COST']

# Cleans final dataframe
del quarterly_grouped['DAY']
del quarterly_grouped['MONTH']

# Sorts dataframe
quarterly_grouped = quarterly_grouped.sort_values(['ID', 'YEAR', 'QUARTER'], ascending=False)


# Saves both generated dataframes into .csv files
monthly_grouped.to_csv("Data/grouped_data/monthly_grouped.csv", index=False, header=True)
quarterly_grouped.to_csv("Data/grouped_data/quartely_grouped.csv", index=False, header=True)