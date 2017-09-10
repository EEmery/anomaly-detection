# Imports necessary libraries
print "Importing packages\n"
import sys
import numpy as np
import pandas as pd
from os import makedirs
from os.path import exists
from warnings import filterwarnings


# Filters warnings
filterwarnings("ignore")


########################## COMMAND PROMPT AND FILE PATHS SETUP ##########################

print "Importing data\n"

# Reads the prompt passed arguments
sys_input = sys.argv
input_file_name1 = "Data/sanitized/gas_stations-fixed.csv"
input_file_name2 = "Data/sanitized/veiculos-fixed.csv"
output_file_path = "Data/preprocessed/time_series_analysis/"

# Creates output folder path if it does not exists
if not exists(output_file_path):
	makedirs(output_file_path)

# Loads the data from the .csv file
columns_names = ["CITY", "GAS_STATION", "ID", "FUEL_TYPE", "AMOUNT", "DAY", "MONTH", "YEAR"]
df = pd.read_csv(input_file_name1, names=columns_names)

columns_names = ["CODE", "ID", "0", "TYPE", "BRAND", "COLOR", "CITY", "DAY", "MONTH", "YEAR"]
df_vehicles = pd.read_csv(input_file_name2, names=columns_names)


#################################### REFORMATS DATA #####################################

print "Reformating data\n"

# Creates a timestamp column
df['TIMESTAMP'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']])

# Numeralizes the vehicles type
vehicles_types = list(df_vehicles['TYPE'].unique())
df_vehicles['TYPE'] = df_vehicles['TYPE'].apply(lambda x: vehicles_types.index(x)+1)

# Add the car type to each ID
df = pd.merge(df, df_vehicles[['ID', 'TYPE']], on='ID', how='right')

# Gets only needed columns from dataframe
df = df[['ID', 'TYPE', 'TIMESTAMP', 'AMOUNT']]

# Normalizes relative to vehicle type
df['AMOUNT'] = df.groupby('TYPE')['AMOUNT'].apply(lambda x: x/x.max())

# Saves dataframes (for memory saving)
for vehicle_type in vehicles_types:
	file_name = vehicle_type + "_time_series"
	df[df['TYPE'] == vehicles_types.index(vehicle_type)+1].to_csv(output_file_path + file_name + "_analysis.csv", index=False, header=True)

# Cleans memory
del df, df_vehicles


############################# APPLY ANALYSIS TO DATAFRAMES ##############################

SAMPLE_FRAME = 5

print "Starting time series analysis\n"

# Reloads dataframes one by one (for memory saving)
for vehicle_type in [vehicles_types[0]]:
	
	# Reopens file (for memory saving)
	file_name = output_file_path + vehicle_type + "_time_series_analysis.csv"
	df = pd.read_csv(file_name)
	result_df = pd.DataFrame()

	# Reshapes dataframes
	del df['TYPE']
	df = df.set_index(['ID', 'TIMESTAMP'], append=True).stack(dropna=False).unstack(1).reset_index()
	del df['level_0'], df['level_2']
	
	# Gets STD for all ID's in a moving sample frame
	len_timestamps = len(df)
	for i in range(len_timestamps - SAMPLE_FRAME):
		result_df = pd.concat([result_df, df.ix[i:i+SAMPLE_FRAME].std().to_frame().transpose()])

	# Restores the index
	result_df.index = range(len_timestamps)

	# Saves result
	#result_df.to_csv(file_name, index=False, header=True)
	#print result_df.set_index('TIMESTAMP').transpose().head()
	print result_df.head()

	print "Saved time series analysis for " + vehicle_type + " vehicles"