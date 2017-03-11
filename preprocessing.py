#########################################################################################
#
# Preprocesses data.
#
# USAGE:   $python preprocessing.py [input file name]
# OPTIONS: $python preprocessin.py [input file name] [output file path]
# FLAGS:   --norm (normalizes the fuel amount)
#
#########################################################################################


# Imports necessary libraries
import sys
import pandas as pd
from os import makedirs
from os.path import exists


# Reads the prompt passed arguments
sys_input = sys.argv
f_normalize = True if ("--norm" in sys_input) else False
input_file_name = sys_input[1]
output_file_path = "output/"
if (len(sys_input) == 3 and not "--norm" in sys_input) or len(sys_input) == 4:
	output_file_path = sys_input[2] if (sys_input[2][-1] == '/') else sys_input[2] + '/'


# Loads the data from the .csv file
columns_names = ["CITY", "GAS_STATION", "ID", "FUEL_TYPE", "AMOUNT", "DAY", "MONTH", "YEAR"]
df = pd.read_csv(input_file_name, names=columns_names)
#df = pd.read_csv("Data/gas_stations_database--fixed_date.csv", names=columns_names)


f_normalize = True
if f_normalize:
	max_amount = df['AMOUNT'].max()
	df['AMOUNT'] = df['AMOUNT']/max_amount


# Maps fuel types to numbers
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASOLINAESPECIAL'] = 1
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASNATURALVEHICULAR'] = 2
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASOLINAPREMIUM'] = 3
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'DIESELOIL'] = 4

# Creates a quarter column
df['QUARTER'] = 0
df['QUARTER'].loc[df['MONTH'] == 1] = df['QUARTER'].loc[df['MONTH'] == 2] = df['QUARTER'].loc[df['MONTH'] == 3] = 1
df['QUARTER'].loc[df['MONTH'] == 4] = df['QUARTER'].loc[df['MONTH'] == 5] = df['QUARTER'].loc[df['MONTH'] == 6] = 2
df['QUARTER'].loc[df['MONTH'] == 7] = df['QUARTER'].loc[df['MONTH'] == 8] = df['QUARTER'].loc[df['MONTH'] == 9] = 3
df['QUARTER'].loc[df['MONTH'] == 10] = df['QUARTER'].loc[df['MONTH'] == 11] = df['QUARTER'].loc[df['MONTH'] == 12] = 4

# Creates a frequency column
df['FREQUENCY'] = 1


# Groups ID's fuel consuption by month
monthly_grouped = df.groupby(['ID', 'YEAR', 'MONTH', 'FUEL_TYPE'], as_index=False).sum()

# Calculates monthly mean
monthly_grouped['MEAN'] = df.groupby(['ID', 'YEAR', 'MONTH', 'FUEL_TYPE'], as_index=False).mean()['AMOUNT']

# Calculates monthly standard deviation
monthly_grouped['STD'] = df.groupby(['ID', 'YEAR', 'MONTH', 'FUEL_TYPE']).std().reset_index(0).reset_index(drop=True)['AMOUNT']

# Cleans final dataframe
del monthly_grouped['DAY']
del monthly_grouped['QUARTER']

# Sorts dataframe
monthly_grouped = monthly_grouped.sort_values(['ID', 'YEAR', 'MONTH'], ascending=False)


# Groups ID's fuel consuption by quarter
quarterly_grouped = df.groupby(['ID', 'YEAR', 'QUARTER', 'FUEL_TYPE'], as_index=False).sum()

# Calculates quarterly mean
quarterly_grouped['MEAN'] = df.groupby(['ID', 'YEAR', 'QUARTER', 'FUEL_TYPE'], as_index=False).mean()['AMOUNT']

# Calculates quarterly standard deviation
quarterly_grouped['STD'] = df.groupby(['ID', 'YEAR', 'QUARTER', 'FUEL_TYPE']).std().reset_index(0).reset_index(drop=True)['AMOUNT']

# Cleans final dataframe
del quarterly_grouped['DAY']
del quarterly_grouped['MONTH']

# Sorts dataframe
quarterly_grouped = quarterly_grouped.sort_values(['ID', 'YEAR', 'QUARTER'], ascending=False)


# Creates output folder path if it does not exists
if not exists(output_file_path):
	makedirs(output_file_path)

# Saves both generated dataframes into .csv files
monthly_grouped.to_csv(output_file_path+"monthly_grouped.csv", index=False, header=True)
quarterly_grouped.to_csv(output_file_path+"quartely_grouped.csv", index=False, header=True)

print "\nSuccessfully finished!"