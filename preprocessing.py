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


if f_normalize:
	max_amount = df['AMOUNT'].max()
	df['AMOUNT'] = df['AMOUNT']/max_amount




# Creates a quarter column
df['QUARTER'] = 0
df['QUARTER'].loc[(df['MONTH'] >= 1) & (df['MONTH'] <= 3)] = 1
df['QUARTER'].loc[(df['MONTH'] >= 4) & (df['MONTH'] <= 6)] = 2
df['QUARTER'].loc[(df['MONTH'] >= 7) & (df['MONTH'] <= 9)] = 3
df['QUARTER'].loc[(df['MONTH'] >= 10) & (df['MONTH'] <= 12)] = 4


# Maps fuel types to numbers
#df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASOLINAESPECIAL'] = 1
#df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASNATURALVEHICULAR'] = 2
#df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASOLINAPREMIUM'] = 3
#df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'DIESELOIL'] = 4


# Creates a column for each fuel
df['GE'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINAESPECIAL']
df['GNV'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASNATURALVEHICULAR']
df['GP'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINAPREMIUM']
df['DO'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'DIESELOIL']

# Creates a frequency column
df['FREQUENCY'] = 1


################################### MONTHLY GROUPING ####################################

# Groups ID's fuel consuption by month
monthly_grouped = df.groupby(['ID', 'YEAR', 'MONTH'], as_index=False).sum()

# Calculates the mean of the first half of the month
#monthly_grouped['HALF_1'] = df['AMOUNT'].loc(df)

# Calculates monthly mean
monthly_grouped['MEAN'] = df.groupby(['ID', 'YEAR', 'MONTH'], as_index=False).mean()['AMOUNT']

# Calculates monthly standard deviation
monthly_grouped['STD'] = df.groupby(['ID', 'YEAR', 'MONTH']).std().reset_index(0).reset_index(drop=True)['AMOUNT']

# Cleans final dataframe
del monthly_grouped['DAY']
del monthly_grouped['QUARTER']

# Sorts dataframe
monthly_grouped = monthly_grouped.sort_values(['ID', 'YEAR', 'MONTH'], ascending=False)


################################## QUARTERLY GROUPING ###################################

# Groups ID's fuel consuption by quarter
quarterly_grouped = df.groupby(['ID', 'YEAR', 'QUARTER'], as_index=False).sum()

# Calculates quarterly mean
quarterly_grouped['MEAN'] = df.groupby(['ID', 'YEAR', 'QUARTER'], as_index=False).mean()['AMOUNT']

# Calculates quarterly standard deviation
quarterly_grouped['STD'] = df.groupby(['ID', 'YEAR', 'QUARTER']).std().reset_index(0).reset_index(drop=True)['AMOUNT']

# Cleans final dataframe
del quarterly_grouped['DAY']
del quarterly_grouped['MONTH']

# Sorts dataframe
quarterly_grouped = quarterly_grouped.sort_values(['ID', 'YEAR', 'QUARTER'], ascending=False)




# Creates output folder path if it does not exists
if not exists(output_file_path):
	makedirs(output_file_path)

file_end = "-normalized.csv" if f_normalize else ".csv"

# Saves both generated dataframes into .csv files
#monthly_grouped.to_csv(output_file_path+"monthly_grouped"+file_end, index=False, header=True)
#quarterly_grouped.to_csv(output_file_path+"quartely_grouped"+file_end, index=False, header=True)

#print monthly_grouped.head(30)
print df.head(10)

print "\nSuccessfully finished!"