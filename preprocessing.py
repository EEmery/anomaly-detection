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

print "Starting preprocessing\n"


########################## COMMAND PROMPT AND FILE PATHS SETUP ##########################

# Reads the prompt passed arguments
sys_input = sys.argv
input_file_name = "Data/gas_stations-fixed.csv" if len(sys_input) < 2 else sys_input[1]
output_file_path = "Data/preprocessed/" if len(sys_input) < 3 else sys_input[2]

# Sanitizes output path
output_file_path += "/" if (output_file_path[-1] == "/") else ""

# Creates output folder path if it does not exists
if not exists(output_file_path):
	makedirs(output_file_path)

# Loads the data from the .csv file
columns_names = ["CITY", "GAS_STATION", "ID", "FUEL_TYPE", "AMOUNT", "DAY", "MONTH", "YEAR"]
df = pd.read_csv(input_file_name, names=columns_names)


####################### MAKES NECESSARY CHANGES IN THE DATA FRAME #######################

# Normalizes the fuel consuption
max_amount = df['AMOUNT'].max()
df['AMOUNT'] = df['AMOUNT']/max_amount

# Creates a week column
df['WEEK'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']]).apply(lambda x: x.week)

# Creates a quarter column
df['QUARTER'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']]).apply(lambda x: x.quarter)

# Creates a semester column
df['SEMESTER'] = df['MONTH'].apply(lambda x: 1 if (x < 7) else 2)

# Creates a frequency column
df['FREQUENCY'] = 1

# Creates a column for each fuel
df['GE'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINAESPECIAL']
df['GNV'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASNATURALVEHICULAR']
df['GP'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINAPREMIUM']
df['DO'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'DIESELOIL']


####################### PROCESS DATAFRAME IN RELATION TO PERIODS ########################

periods = ['WEEK', 'MONTH', 'QUARTER', 'SEMESTER']
messages_to_print = ['weekly', 'monthly', 'quarterly', 'semesterly']
columns_to_clean = ['AMOUNT', 'DAY', 'WEEK', 'MONTH', 'QUARTER', 'SEMESTER']

for period, message in zip(periods, messages_to_print):

	print "Starting " + message + " analysis"

	# Groups ID's fuel consuption by month
	grouping_cols = ['ID', 'YEAR'] + [period]
	grouped = df.groupby(grouping_cols, as_index=False)
	df_grouped = grouped.sum()

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

	# Saves final file
	print "Saving " + message + " analysis"
	df_grouped.to_csv(output_file_path + message + "_analysis.csv", index=False, header=True)

	# Cleans final dataframe
	columns_to_clean.remove(period)
	for col in columns_to_clean:
		del df_grouped[col]
	columns_to_clean.append(period)

	# Cleans auxiliar dataframes
	del grouped
	del df_grouped

	print message.title() + " analysis sucessfully finished\n"