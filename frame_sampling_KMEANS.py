import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq


k_means = range(1, 10)
elbow_rate = 0.1

input_file_path_base = "Data/preprocessed/frame_sampling_global_norm/"
output_file_path_base = "Data/frame_sampling/frame_sampling_kmeans_global_norm/"

if not os.path.exists(output_file_path_base):
	os.makedirs(output_file_path_base)
f = open(output_file_path_base + 'k_means-output-log.txt', 'w')

# Iterates over all vehicle types
vehicle_types = os.listdir(input_file_path_base)
for vehicle_type in vehicle_types:

	# Iterates over all fuel types
	fuel_types = os.listdir(input_file_path_base+vehicle_type)
	for fuel_type in fuel_types:

		amounts = []
		intervals = []

		# Iterates over all ID's (files that end on '.csv')
		v_ids = [i for i in os.listdir(input_file_path_base + vehicle_type + '/' + fuel_type) if i[-4:] == '.csv']
		for v_num, v_id in enumerate(v_ids):
			print "Creating Self-Organized Map for " + vehicle_type + " with " + fuel_type + " consuption (ID " + str(v_num) + " of " + str(len(v_ids)) + ")\r",

			# Opens ID frame sampling analysis (NOT NORMALIZED)
			input_file_name = input_file_path_base + vehicle_type + '/' + fuel_type + '/' + v_id
			df = pd.read_csv(input_file_name)
			data = df.fillna(0).as_matrix().astype(float)

			# Starts K-Means analysis
			best_distortion = None
			best_code_book = None
			best_distance = None
			best_k = None
			for k_mean in k_means:
				centroids, distortion = kmeans(data, k_mean)									# Uses kmeans to clusterize data from actual map
				code_book, distance = vq(data, centroids)										# Gets codebook of ID's

				# Saves results if distortion is more than "elbow_rate" percent smaller than the best distortion so far
				if best_distortion == None or abs(distortion - best_distortion)/best_distortion > elbow_rate:
					best_distortion = distortion
					best_code_book = code_book
					best_distance = distance
					best_k = k_mean
				# If distortion is not "elbow_percent" percent smaller than the best distortion so far, quites the analysis
				else:
					break

			df['CODE_BOOK'] = best_code_book													# Saves codebook on result on dataframe
			df['DISTANCE'] = best_distance														# Saves distances from centroids on dataframe
			f.write(vehicle_type + ' ' + fuel_type + ' ' + v_id[:-4] + ' k=' + str(best_k) + '\n')

			# Creates a folder with it does not exists
			output_file_path = output_file_path_base + vehicle_type + '/' + fuel_type + '/'
			if not os.path.exists(output_file_path):
				os.makedirs(output_file_path)

			# Saves dataframe
			df.to_csv(output_file_path + v_id, index=False, header=True)

		print ''
f.close()