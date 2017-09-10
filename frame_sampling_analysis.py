# Imports necessary libraries
print "Importing packages\n"
import sys
import numpy as np
import pandas as pd
from os import makedirs
from os.path import exists
from warnings import filterwarnings
from datetime import timedelta


# Filters warnings
filterwarnings("ignore")


########################## COMMAND PROMPT AND FILE PATHS SETUP ##########################

print "Importing data\n"

# Reads the prompt passed arguments
sys_input = sys.argv
input_file_name = "Data/sanitized/prepro_datetime.csv"

# Loads the data from the .csv file
columns_names = ["ind","d_veh_brn","ID","TYPE","FUEL_TYPE","GAS_STATION","LOCAL","TIMESTAMP","AMOUNT"]
df = pd.read_csv(input_file_name, names=columns_names)


#################################### REFORMATS DATA #####################################

print "Reformating data\n"

ids = list(df['ID'].unique())
num_ids = len(ids)

fuel_types = list(df['FUEL_TYPE'].unique())
num_fuel_types = len(fuel_types)

vehicles_types = list(df['TYPE'].unique())
num_vehicles_types = len(vehicles_types)


# Creates a timestamp column
df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%Y-%m-%d %H:%M:%S')

# Numeralizes the vehicles type
#df['TYPE'] = df['TYPE'].apply(lambda x: vehicles_types.index(x)+1)

# Creates a column for each fuel
df['GE'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINA ESPECIAL']
df['GNV'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GAS NATURAL VEHICULAR']
df['GP'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'GASOLINA PREMIUM']
df['DO'] = df['AMOUNT'].loc[df['FUEL_TYPE'] == 'DIESEL OIL']

# Renames fuel types
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASOLINA ESPECIAL'] = 'GE'
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GAS NATURAL VEHICULAR'] = 'GNV'
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'GASOLINA PREMIUM'] = 'GP'
df['FUEL_TYPE'].loc[df['FUEL_TYPE'] == 'DIESEL OIL'] = 'DO'

# Gets time intervals from timestamps
df = df.sort(['ID', 'FUEL_TYPE', 'TIMESTAMP'])
tmp = df.groupby(['ID', 'FUEL_TYPE']).apply(lambda x: x['TIMESTAMP'] - x['TIMESTAMP'].shift()).reset_index().rename(columns={'TIMESTAMP':'TIMESTAMP_DIFF'})
df = pd.merge(df, tmp[['level_2', 'TIMESTAMP_DIFF']], left_index=True, right_on='level_2')

# Gets only needed columns from dataframe
df = df[['ID', 'TYPE', 'FUEL_TYPE', 'TIMESTAMP', 'TIMESTAMP_DIFF', 'GE', 'GNV', 'GP', 'DO']]
df.index = range(len(df))




sample_frame = 3

for f_type in ['GE', 'GNV', 'GP', 'DO']:

	for v_num, v_id in enumerate(ids):
		print 'Analysing for ' + f_type + ' consuption (ID ' + str(v_num) + ' of ' + str(num_ids) + ')\r',

		v_type = df[df['ID'] == v_id]['TYPE'].iloc[0]
		mask = (df['ID'] == v_id) & (df['FUEL_TYPE'] == f_type)
		len_timestamps = len(df[mask])

		try:
			# Start analysis for ID
			result_df = pd.DataFrame(columns = ['A0', 'A1', 'A2', 'I0', 'I1', 'I2'])
			for idx in range(len_timestamps-sample_frame):
				amounts = df[mask].iloc[idx : idx+sample_frame][f_type].tolist()
				result_df.loc[idx, 'A0':'A2'] = amounts

				intervals_np = df[mask].iloc[idx : idx+sample_frame]['TIMESTAMP_DIFF'].fillna(0).tolist()
				intervals = []
				for gap in intervals_np:
					d = gap.days
					#h = gap.seconds // 3600
					#s = gap.seconds - (h*3600)
					#m = s // 60
					#s = s - (m*60)
					#intervals.append(str(d) + ' ' + str(h) + ":" + str(m) + ":" + str(s))
					intervals.append(d)
				result_df.loc[idx, 'I0':'I2'] = intervals

			# Saves result dataframe
			if len(result_df) > 0:
				# Creates a folder if needed
				output_file_path = "Data/preprocessed/frame_sampling/" + v_type + '/' + f_type + '/'
				if not exists(output_file_path):
					makedirs(output_file_path)

				# Normalizes dataframe
				#result_df.loc[:,'I0':'I2'] = result_df.loc[:,'I0':'I2']/result_df.loc[:,'I0':'I2'].max().max()
				#result_df.loc[:,'A0':'A2'] = result_df.loc[:,'A0':'A2']/result_df.loc[:,'A0':'A2'].max().max()

				# Saves dataframe
				result_df.to_csv(output_file_path+v_id+'.csv', index=False, header=True)

		except KeyError:
			pass
	print ''