import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from mvpa2.suite import *


# Imports data
#data = pd.read_csv("Data/preprocessed/frequency_analysis/daily_analysis.csv")
data = pd.read_csv("Data/preprocessed/behavorial_analysis/behavorial-analysis.csv")

# Gets data
ids = data['ID'].unique()
consuption = data.ix[:, 2:].fillna(0).as_matrix()

# Removes the frequency rows
#len_consuption = len(consuption)
#mask = np.array([i in xrange(4, len_consuption, 5) for i in xrange(len_consuption)])
#consuption = consuption[~mask]

# Reshapes consuption data
#consuption = consuption.reshape((len(ids), 4*len(consuption[0])))
len_consuption = len(consuption)


bins_list = [20, 30, 40, 50]
k_folds_list = [2, 3, 4]

for k_folds in k_folds_list:
	for bins in bins_list:

		print "\n\nAnalysing Self-Oraganized Maps with " + str(k_folds) + " folds and " + str(bins) + " by " + str(bins) + " lattice"
		slice_size = int(len_consuption/k_folds)

		# Trains Self Organizing Maps
		som_list = []
		for i in range(k_folds):
			print "Training self organized map " + str(i)
			som_list.append(SimpleSOMMapper((bins, bins), len_consuption, learning_rate=0.05))
			som_list[-1].train(np.copy(consuption[slice_size*i : slice_size*(i+1)]))


		# Maps data with the trained SOM
		mapped = []
		for i, som in enumerate(som_list):
			print "Mapping data with self-organized map " + str(i)
			mapped.append(som(consuption))


		# Saves results
		for i, mapped in enumerate(mapped):
			print "\nSaving results of map " + str(i)

			# Creates a folder with it does not exists
			output_file_path = "Data/mapped_folded/behavorial_data/" + str(k_folds) + "_folds/lattice_" + str(bins) + "x" + str(bins) + "/"
			if not os.path.exists(output_file_path):
				os.makedirs(output_file_path)

			# Creates and saves a dataframe with the generated map results
			print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .csv"
			mapped_df = pd.DataFrame({'ID':ids, 'X':mapped[:,0], 'Y':mapped[:,1]})
			mapped_df.to_csv(output_file_path + "som_" + str(i) + "_mapped_" + str(bins) + "x" + str(bins) +  "_lattice.csv", index=False, header=True)

			# Save heatmap of data
			print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .png as a heatmap"
			heatmap, xedges, yedges = np.histogram2d(mapped[:,0], mapped[:,1], bins)
			extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
			plt.clf()
			plt.imshow(heatmap.T, extent=extent, origin='lower')
			plt.colorbar()
			plt.savefig(output_file_path + "heatmap_" + str(i) + "_" + str(bins) + "x" + str(bins) + "_lattice.png", bbox_inches='tight')


			# Save ploted data
			print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .png as a plot\n"
			plt.clf()
			plt.plot(mapped[:,0], mapped[:,1], 'bo')
			plt.savefig(output_file_path + "plot_" + str(i) + "_" + str(bins) + "x" + str(bins) + "_lattice.png", bbox_inches='tight')