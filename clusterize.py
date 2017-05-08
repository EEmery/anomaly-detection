import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mvpa2.suite import *
#from scipy.cluster.vq import kmeans, vq


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

bins = 50

# Trains a Self Organizing Maps (SOM) to the data
print "Training self organizing map with " + str(bins) + "x" + str(bins) + " lattice"
som = SimpleSOMMapper((bins, bins), len_consuption, learning_rate=0.01)
som.train(consuption)

# Maps data with the trained SOM
print "Mapping data with created self organizing map"
mapped = som(consuption)

# Creates and saves a dataframe with the generated map results
print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .csv"
mapped_df = pd.DataFrame({'ID':ids, 'X':mapped[:,0], 'Y':mapped[:,1]})
mapped_df.to_csv("Data/mapped/som_mapped_" + str(bins) + "x" + str(bins) +  "_lattice.csv", index=False, header=True)

# Save heatmap of data
print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .png as a heatmap"
heatmap, xedges, yedges = np.histogram2d(mapped[:,0], mapped[:,1], bins)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
plt.imshow(heatmap.T, extent=extent, origin='lower')
plt.colorbar()
plt.savefig("Data/mapped/heatmap_" + str(bins) + "x" + str(bins) + "_lattice.png", bbox_inches='tight')


# Save ploted data
print "Saving result of " + str(bins) + "x" + str(bins) + " lattice in a .png as a plot\n"
plt.clf()
plt.plot(mapped[:,0], mapped[:,1], 'bo')
plt.savefig("Data/mapped/plot_" + str(bins) + "x" + str(bins) + "_lattice.png", bbox_inches='tight')