import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mvpa2.suite import *


bins = 20

input_file_path_base = "Data/preprocessed/frame_sampling_local_norm/"
output_file_path_base = "Data/frame_sampling/frame_sampling_som_local_norm/"

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
			print "Creating Self-Organized Map for " + vehicle_type + " with " + fuel_type + " consuption (ID " + str(v_num) + " of " + str(len(v_ids)) + ")\r",

			# Opens ID frame sampling analysis (NOT NORMALIZED)
			input_file_name = input_file_path_base + vehicle_type + '/' + fuel_type + '/' + v_id
			data = pd.read_csv(input_file_name).fillna(0).as_matrix()

			# Creates a Self-Organizing Map (SOM)
			som = SimpleSOMMapper((bins, bins), 300, learning_rate=0.05)
			som.train(data)
			som_map = som(data)

			# Creates a folder with it does not exists
			output_file_path = output_file_path_base + vehicle_type + '/' + fuel_type + '/'
			if not os.path.exists(output_file_path):
				os.makedirs(output_file_path)

			# Plot SOM as a dataframe
			mapped_df = pd.DataFrame({'X':som_map[:,0], 'Y':som_map[:,1]})
			mapped_df.to_csv(output_file_path + v_id, index=False, header=True)

			# Plot SOM as a Heatmap (.png)
			heatmap, xedges, yedges = np.histogram2d(som_map[:,0], som_map[:,1], bins)
			extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
			plt.clf()
			plt.imshow(heatmap.T, extent=extent, origin='lower')
			plt.colorbar()
			plt.savefig(output_file_path + v_id[:-4] + '.png', bbox_inches='tight')

		print ''