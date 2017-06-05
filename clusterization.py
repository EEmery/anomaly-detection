import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans, vq
from warnings import filterwarnings

# Filters warnings
filterwarnings("ignore")
file = open("Data/mapped_folded/behavorial_data/best-matching-cluster-log.txt", 'w')

k_means = 4
k_folds_list = [2, 3, 4]
bins_list = [20, 30, 40, 50]

for k_folds in k_folds_list:
	for bins in bins_list:

		print "\nClustering results of " + str(k_folds) + " folds with " + str(bins) + "x" + str(bins) + " lattice"
		file.write("Cluster results of " + str(k_folds) + " folds with " + str(bins) + "x" + str(bins) + " lattice\n")


		path = "Data/mapped_folded/behavorial_data/" + str(k_folds) + "_folds/lattice_" + str(bins) + "x" + str(bins) +"/"		# Refers to data path
		#os_path = os.getcwd().replace('\\', '/') + '/'																			# Gets the actual folder path
		#os.listdir(os_path + path)																								# Gets a list of all files in folder


		df = pd.DataFrame()																			# Will latter save the cluster of each ID in each map
		for map_num in range(k_folds):																# Iterates over maps
			data = pd.read_csv(path + "som_" + str(map_num) + "_mapped_" + str(bins) + "x" + str(bins) + "_lattice.csv")
			df['ID'] = data['ID'].unique()
			coordinates = data.ix[:, 1:].fillna(0).as_matrix().astype(float)						# Gets data as a numpy matrix
			
			centroids, distortion = kmeans(coordinates, k_means)									# Uses kmeans to clusterize data from actual map
			code_book, distance = vq(coordinates, centroids)										# Gets codebook of ID's

			df['MAP_' + str(map_num)] = code_book													# Saves codebook on result dataframe


		bm_cluster = np.zeros((k_means, k_folds-1))													# Will latter save the best matching clusters
		output = pd.DataFrame({'ID': df['ID'].unique(), 'CLUSTER': np.zeros(len(df['ID']))})
		for cluster_num in range(k_means):															# Iterates over global cluster
			for map_num in range(1, k_folds):														# Iterates over all maps except first

				tmp = np.zeros(k_means)																# Will save cluster matching scores
				for cluster_num_comp in range(k_means):												# Iterates over all clusters in comparison map
					condition = ((df['MAP_0'] == cluster_num) & (df['MAP_' + str(map_num)] == cluster_num_comp))
					tmp[cluster_num_comp] = len(df[condition])										# Gets score of comparison
				bm_cluster[cluster_num, map_num-1] = tmp.argmax()									# Saves cluster number that got highest score

			# Prints and saves sattistics of comparisons
			condition = df['MAP_0'] == cluster_num
			total = len(df[df['MAP_0'] == cluster_num])
			for map_num, cluster_idx in enumerate(bm_cluster[cluster_num]):
				condition = (condition & (df["MAP_" + str(map_num+1)] == cluster_idx))
				total += len(df[df["MAP_" + str(map_num+1)] == cluster_idx])
			print "Cluster " + str(cluster_num) + ": " + str(len(df[condition])) + " similar ID's from " + str(total/k_folds) + " ID's in cluster " + str(len(df[condition]) / float(total/k_folds))
			file.write("Cluster " + str(cluster_num) + ": " + str(len(df[condition])) + " similar ID's from " + str(total/k_folds) + " ID's in cluster " + str(len(df[condition]) / float(total/k_folds)) + "\n")
			output['CLUSTER'][condition] = cluster_num

		file.write("\n")
		output.to_csv(path+"clusterization-output.csv", index=False, header=True)				# Saves result dataframe