#########################################################################################
#
# Preprocesses data.
#
# USAGE:   $python preprocessing.py
# OPTIONS: [input file name]
#          [output files path]
# 		   $python preprocessing.py  [input file name] [output files path]
#
#########################################################################################


# Imports necessary libraries
print "Importing packages\n"
import sys
import pandas as pd
from os import makedirs
from os.path import exists
from warnings import filterwarnings
from numpy import mean, array

# Filters warnings
filterwarnings("ignore")

print "Starting statistical analysis\n"


########################## COMMAND PROMPT AND FILE PATHS SETUP ##########################

# Reads the prompt passed arguments
sys_input = sys.argv
input_file_name1 = "Data/sanitized/gas_stations-fixed.csv" if len(sys_input) < 2 else sys_input[1]
input_file_name2 = "Data/sanitized/veiculos-fixed.csv"
output_file_path = "Data/preprocessed/statistical_analysis/" if len(sys_input) < 3 else sys_input[2]

# Sanitizes output path
output_file_path += "/" if (output_file_path[-1] == "/") else ""

# Creates output folder path if it does not exists
if not exists(output_file_path):
	makedirs(output_file_path)

# Loads the data from the .csv file
columns_names = ["CITY", "GAS_STATION", "ID", "FUEL_TYPE", "AMOUNT", "DAY", "MONTH", "YEAR"]
df = pd.read_csv(input_file_name1, names=columns_names)
columns_names = ["CODE", "ID", "0", "TYPE", "BRAND", "COLOR", "CITY", "DAY", "MONTH", "YEAR"]
df_vehicles = pd.read_csv(input_file_name2, names=columns_names)


####################### MAKES NECESSARY CHANGES IN THE DATA FRAME #######################

def codify_ID(ID):
	ID = str(ID).upper()
	codified_ID = [str(ord(char)) for char in ID ]
	codified_ID = ['00']+codified_ID if len(codified_ID) <=6 else codified_ID
	return ''.join(codified_ID)

# Changes car ID's to a numeric coded system
#df['ID'] = df['ID'].apply(codify_ID)
#df_vehicles['ID'] = df_vehicles['ID'].apply(codify_ID)

# Normalizes the fuel consuption
max_amount = df['AMOUNT'].max()
df['AMOUNT'] = df['AMOUNT']/max_amount

# Creates a week column
df['WEEK'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']]).apply(lambda x: x.week)

# Creates a quarter column
df['QUARTER'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']]).apply(lambda x: x.quarter)

# Creates a semester column
df['SEMESTER'] = df['MONTH'].apply(lambda x: 1 if (x < 7) else 2)

# Creates a day of year column
df['DAY'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']]).apply(lambda x: x.dayofyear)

# Numeralizes the vehiculo type
vehicles_types = list(df_vehicles['TYPE'].unique())
df_vehicles['TYPE'] = df_vehicles['TYPE'].apply(lambda x: vehicles_types.index(x)+1)

# Creates a frequency column
df['FREQUENCY'] = 1

# Creates a column for each fuel
df['GE'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINAESPECIAL']
df['GNV'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASNATURALVEHICULAR']
df['GP'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINAPREMIUM']
df['DO'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'DIESELOIL']


####################### PROCESS DATAFRAME IN RELATION TO PERIODS ########################

periods = ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'SEMESTER']
messages_to_print = ['daily', 'weekly', 'monthly', 'quarterly', 'semesterly']
columns_to_clean = ['AMOUNT', 'DAY', 'WEEK', 'MONTH', 'QUARTER', 'SEMESTER']

for period, message in zip(periods, messages_to_print):

	print "Starting " + message + " analysis"

	# Groups ID's fuel consuption by month
	grouping_cols = ['ID', 'YEAR'] + [period]
	grouped = df.groupby(grouping_cols, as_index=False)
	df_grouped = grouped.sum()

	# Add the car type of each ID
	df_grouped = pd.merge(df_grouped, df_vehicles[['ID', 'TYPE']], on='ID', how='left')

	# Sorts dataframe
	df_grouped = df_grouped.sort_values(grouping_cols, ascending=False)

	# Calculates the difference in the means of two halfs of the grouping
	df_grouped = pd.merge(df_grouped, grouped['GE'].apply(lambda x: mean(array(x)[len(array(x))/2:]) - mean(array(x)[:len(array(x))/2])).reset_index().rename(columns={0:'GE_RATE'}), on=grouping_cols)
	df_grouped = pd.merge(df_grouped, grouped['GNV'].apply(lambda x: mean(array(x)[len(array(x))/2:]) - mean(array(x)[:len(array(x))/2])).reset_index().rename(columns={0:'GNV_RATE'}), on=grouping_cols)
	df_grouped = pd.merge(df_grouped, grouped['GP'].apply(lambda x: mean(array(x)[len(array(x))/2:]) - mean(array(x)[:len(array(x))/2])).reset_index().rename(columns={0:'GP_RATE'}), on=grouping_cols)
	df_grouped = pd.merge(df_grouped, grouped['DO'].apply(lambda x: mean(array(x)[len(array(x))/2:]) - mean(array(x)[:len(array(x))/2])).reset_index().rename(columns={0:'DO_RATE'}), on=grouping_cols)

	# Calculates monthly means
	df_grouped = pd.merge(df_grouped, grouped[['GE', 'GNV', 'GP', 'DO']].mean().rename(columns={'GE':'GE_MEAN', 'GNV':'GNV_MEAN', 'GP':'GP_MEAN', 'DO':'DO_MEAN'}), on=grouping_cols)

	# Calculates monthly standard deviation
	grouped = df.groupby(grouping_cols)[['GE', 'GNV', 'GP', 'DO']].std().reset_index()
	df_grouped = pd.merge(df_grouped, grouped.rename(columns={'GE':'GE_STD', 'GNV':'GNV_STD', 'GP':'GP_STD', 'DO':'DO_STD'}), on=grouping_cols)

	# Cleans final dataframe
	columns_to_clean.remove(period)
	for col in columns_to_clean:
		del df_grouped[col]
	columns_to_clean.append(period)

	# Saves final file
	print "Saving " + message + " analysis"
	df_grouped.to_csv(output_file_path + message + "_analysis.csv", index=False, header=True)

	# Cleans auxiliar dataframes
	del grouped
	del df_grouped

	print message.title() + " analysis sucessfully finished\n"