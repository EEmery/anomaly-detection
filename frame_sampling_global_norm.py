import os
import pandas as pd

input_file_path_base = "Data/preprocessed/frame_sampling/"
output_file_path_base = "Data/preprocessed/frame_sampling_global_norm/"

# Iterates over all vehicle types
vehicle_types = os.listdir(input_file_path_base)
for vehicle_type in vehicle_types:

	# Iterates over all fuel types
	fuel_types = os.listdir(input_file_path_base+vehicle_type)
	for fuel_type in fuel_types:

		amounts = []
		intervals = []

		# Iterates over all ID's
		v_ids = os.listdir(input_file_path_base + vehicle_type + '/' + fuel_type)
		for v_num, v_id in enumerate(v_ids):
			print "Analysing for " + vehicle_type + " with " + fuel_type + " consuption (ID " + str(v_num) + " of " + str(len(v_ids)) + ")\r",

			# Opens ID frame sampling analysis (NOT NORMALIZED)
			input_file_name = input_file_path_base + vehicle_type + '/' + fuel_type + '/' + v_id
			df = pd.read_csv(input_file_name)

			# Saves highest value in a list
			amounts.append(df.loc[:,'A0':'A2'].max().max())
			intervals.append(df.loc[:,'I0':'I2'].max().max())
		print ''

		# Gets the highest of them all
		highest_amount = max(amounts)
		highest_interval = max(intervals)

		# Iterates over all ID's normalizing values
		for v_id in v_ids:
			print "Normalizing for " + vehicle_type + " with " + fuel_type + " consuption (ID " + str(v_num) + " of " + str(len(v_ids)) + ")\r",

			# Opens ID frame sampling analysis (NOT NORMALIZED)
			input_file_name = input_file_path_base + vehicle_type + '/' + fuel_type + '/' + v_id
			df = pd.read_csv(input_file_name).fillna(0)

			# Normalizes dataframe
			df.loc[:,'A0':'A2'] = df.loc[:,'A0':'A2'] / highest_amount
			df.loc[:,'I0':'I2'] = df.loc[:,'I0':'I2'] / highest_interval

			# Saves new dataframe
			output_file_path = output_file_path_base + vehicle_type + '/' + fuel_type + '/'
			if not os.path.exists(output_file_path):
				os.makedirs(output_file_path)
			df.to_csv(output_file_path + v_id, index=False, header=True)
		print ' '
	print '---------------------------\n'
