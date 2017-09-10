import numpy as np
import kmedoids
from sklearn.metrics.pairwise import pairwise_distances
from scipy.spatial.distance import euclidean

# 3 points in dataset
data = np.array([[1,1], 
				[2,2], 
				[10,10]])

# distance matrix
D = pairwise_distances(data, metric='euclidean')

print D

# split into 2 clusters
M, C = kmedoids.kMedoids(D, 2)

print M
print C

print euclidean(data[C[0][1]], data[M[0]])