# Imports necessary libraries
print "Importing packages\n"
import pandas as pd
from warnings import filterwarnings
from numpy import mean, array

# Filters warnings
filterwarnings("ignore")

print "Starting behavorial analysis\n"

output_file_path = "Data/preprocessed/"
output = pd.DataFrame()


################################## CONSUPTION AMOUNT ####################################

statistical_analysis = pd.read_csv('Data/preprocessed/statistical_analysis/not-normalized/monthly_analysis.csv')
statistical_analysis = statistical_analysis.sort_values('ID', ascending=False)
output['ID'] = statistical_analysis['ID'].unique()											# Puts ID's to output

tmp = statistical_analysis[['ID', 'GE', 'GNV', 'GP', 'DO']].groupby('ID').mean().reset_index()
output = pd.merge(output, tmp, on='ID')														# Puts monthly refuel mean to output

tmp = statistical_analysis[['ID', 'GE_STD', 'GNV_STD', 'GP_STD', 'DO_STD']].groupby('ID').std().reset_index()
output = pd.merge(output, tmp, on='ID')														# Puts monthly refuel STD to output


###################################### FREQUENCY ########################################

time_interval_analysis = pd.read_csv('Data/preprocessed/time_interval_analysis/time_interval_analysis.csv').fillna(0)

tmp = time_interval_analysis.groupby('ID', group_keys=False).apply(lambda x: x.ix[x.INTERVAL.idxmin()])[['ID', 'GE_R', 'GNV_R', 'GP_R', 'DO_R']]
output = pd.merge(output, tmp, on='ID')														# Puts highest time interval to output

tmp = time_interval_analysis[['ID', 'INTERVAL']].groupby('ID').std().reset_index().rename(columns={'INTERVAL':'INTERVAL_STD'})
output = pd.merge(output, tmp, on='ID')														# Puts time interval STD to output


###################################### FUEL TYPE ########################################

columns_names = ["CITY", "GAS_STATION", "ID", "FUEL_TYPE", "AMOUNT", "DAY", "MONTH", "YEAR"]
raw_data = pd.read_csv('Data/sanitized/gas_stations-fixed.csv', names=columns_names)
raw_data = raw_data.sort_values('ID', ascending=False)

fuel_types = raw_data['FUEL_TYPE'].unique()

for fuel_type in fuel_types:
	raw_data[fuel_type] = 0

for fuel_type in fuel_types:
	raw_data[fuel_type][raw_data['FUEL_TYPE'] == fuel_type] = 1

tmp = raw_data.groupby('ID', as_index=False).sum()[fuel_types].as_matrix()
output['MAX_FUEL_TYPE'] = tmp.argmax(axis=1)												# Puts most registered fuel to output
output['FUEL_TYPE_STD'] = tmp.std(axis=1)													# Puts fuel type STD to output


################################# CONSUPTION LOCATION ###################################

consuption_locations = raw_data['GAS_STATION'].unique()

for consuption_location in consuption_locations:
	raw_data[consuption_location] = 0

for consuption_location in consuption_locations:
	raw_data[consuption_location][raw_data['GAS_STATION'] == consuption_location] = 1

tmp = raw_data.groupby('ID', as_index=False).sum()[consuption_locations].as_matrix()
output['MAX_LOCATION'] = tmp.argmax(axis=1)													# Puts most registered fuel to output
output['LOCATION_STD'] = tmp.std(axis=1)													# Puts fuel type STD to output

output.to_csv("Data/preprocessed/behavorial_analysis/behavorial-analysis.csv", index=False, header=True)