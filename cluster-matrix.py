# Imports necessary libraries
print "Importing packages\n"
import pandas as pd
import matplotlib.pyplot as plt
from warnings import filterwarnings


# Ignores warnings
filterwarnings("ignore")


input_file_path = "Data/preprocessed_v2/not-normalized/"
periods = ['WEEK', 'MONTH', 'QUARTER', 'SEMESTER']
periods_amounts = [53, 12, 4, 2]
file_names = ['weekly', 'monthly', 'quarterly', 'semesterly']


# Iterates over all periods
for period, period_amount, file_name in zip(periods, periods_amounts, file_names):
	
	# Opens file (related to the period)
	cluster_matrix = pd.read_csv(input_file_path + file_name + '_analysis.csv')

	# Remover YEAR necessity by increasing period limits
	cluster_matrix[period] = cluster_matrix[period] + (cluster_matrix['YEAR'] - 2015) * period_amount

	# Slices data frame to get only necessary columns
	cluster_matrix = cluster_matrix[['ID', period, 'FREQUENCY', 'GE_MEAN', 'GNV_MEAN', 'GP_MEAN', 'DO_MEAN']]

	# Reshapes data frame to desired shape
	cluster_matrix = cluster_matrix.set_index(['ID', period])
	cluster_matrix = cluster_matrix.stack().unstack(1)

	# Show some data
	if period == 'MONTH':
		cluster_matrix.loc['741NKH'].T.plot.bar()
		plt.show()