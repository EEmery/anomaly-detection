import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mvpa2.suite import *
#from scipy.cluster.vq import kmeans, vq


########################### DATA EXTRACTION AND PREPARATION #############################

data = pd.read_csv("Data/preprocessed/frequency_analysis/semesterly_analysis.csv")

ids = data['ID'].unique()
consuption = data.ix[:, 2:].fillna(0).as_matrix()

# Removes the frequency rows
len_consuption = len(consuption)
mask = np.array([i in xrange(4, len_consuption, 5) for i in xrange(len_consuption)])
consuption = consuption[~mask]

# Reshapes consuption data
consuption = consuption.reshape((len(ids), 4*len(consuption[0])))
len_consuption = len(consuption)


############################ SELF ORGANIZED MAPS TRAININGS ##############################

bins = 50
slice_size = int(len_consuption/4)

# Trains Self Organizing Maps (SOM) 1
print "Training self organizing map 1 with " + str(bins) + "x" + str(bins) + " lattice"
som1 = SimpleSOMMapper((bins, bins), len_consuption, learning_rate=0.01)
som1.train(np.copy(consuption[:slice_size]))

# Trains Self Organizing Maps (SOM) 2
print "Training self organizing map 2 with " + str(bins) + "x" + str(bins) + " lattice"
som2 = SimpleSOMMapper((bins, bins), len_consuption, learning_rate=0.01)
som2.train(np.copy(consuption[slice_size:slice_size*2]))

# Trains Self Organizing Maps (SOM) 3
print "Training self organizing map 3 with " + str(bins) + "x" + str(bins) + " lattice"
som3 = SimpleSOMMapper((bins, bins), len_consuption, learning_rate=0.01)
som3.train(np.copy(consuption[slice_size*2:slice_size*3]))

# Trains Self Organizing Maps (SOM) 4
print "Training self organizing map 4 with " + str(bins) + "x" + str(bins) + " lattice"
som4 = SimpleSOMMapper((bins, bins), len_consuption, learning_rate=0.01)
som4.train(np.copy(consuption[slice_size*3:slice_size*4]))


############################# SELF ORGANIZED MAPS MAPPING ###############################

# Maps data with the trained SOM
print "Mapping data with created self organizing map"

mapped = [som1(consuption), som2(consuption), som3(consuption), som4(consuption)]

for i, mapped in enumerate(mapped):
	print "Map: " + str(i)

	# Creates and saves a dataframe with the generated map results
	print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .csv"
	mapped_df = pd.DataFrame({'ID':ids, 'X':mapped[:,0], 'Y':mapped[:,1]})
	mapped_df.to_csv("Data/mapped_folded/som_" + str(i) + "_mapped_" + str(bins) + "x" + str(bins) +  "_lattice.csv", index=False, header=True)

	# Save heatmap of data
	print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .png as a heatmap"
	heatmap, xedges, yedges = np.histogram2d(mapped[:,0], mapped[:,1], bins)
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
	plt.clf()
	plt.imshow(heatmap.T, extent=extent, origin='lower')
	plt.colorbar()
	plt.savefig("Data/mapped_folded/heatmap_" + str(i) + "_" + str(bins) + "x" + str(bins) + "_lattice.png", bbox_inches='tight')


	# Save ploted data
	print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .png as a plot\n"
	plt.clf()
	plt.plot(mapped[:,0], mapped[:,1], 'bo')
	plt.savefig("Data/mapped_folded/plot_" + str(i) + "_" + str(bins) + "x" + str(bins) + "_lattice.png", bbox_inches='tight')