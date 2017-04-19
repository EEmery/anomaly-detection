# Imports necessary libraries
print "Importing packages\n"
import pandas as pd
import matplotlib.pyplot as plt
from warnings import filterwarnings
from numpy import nan


# Ignores warnings
filterwarnings("ignore")


input_file_path = "Data/preprocessed_v2/not-normalized/"
periods = ['WEEK', 'MONTH', 'QUARTER', 'SEMESTER']
periods_amounts = [53, 12, 4, 2]
file_names = ['weekly', 'monthly', 'quarterly', 'semesterly']


# Iterates over all periods
for period, period_amount, file_name in zip(periods, periods_amounts, file_names):

	print "Making " + file_name + " analysis"
	
	# Opens file (related to the period)
	periodic_analysis = pd.read_csv(input_file_path + file_name + '_analysis.csv')

	# Remover YEAR necessity by increasing period limits
	periodic_analysis[period] = periodic_analysis[period] + (periodic_analysis['YEAR'] - 2015) * period_amount

	# Slices data frame to get only necessary columns
	periodic_analysis = periodic_analysis[['ID', period, 'FREQUENCY', 'GE_MEAN', 'GNV_MEAN', 'GP_MEAN', 'DO_MEAN']]

	# Reshapes data frame to desired shape
	periodic_analysis = periodic_analysis.set_index(['ID', period])
	periodic_analysis = periodic_analysis.stack().unstack(1)

	
	# Gets the period of higher frequency
	max_frequencies = periodic_analysis.loc(axis=0)[:, 'FREQUENCY'].idxmax(axis=1).reset_index().rename(columns={0:'STAMP'})

	# Creates a data frame for final results
	result_df = pd.DataFrame(columns = ['ID', 'GE_MEAN', 'GNV_MEAN', 'GP_MEAN', 'DO_MEAN'])

	# Iterates over the ID's
	for i, ID, STAMP in zip(range(len(max_frequencies)), max_frequencies['ID'], max_frequencies['STAMP']):
		data = periodic_analysis.loc(axis=0)[ID].ix[1:, STAMP]					# Gets the means from the higher frequency period
		
		row = [ID]
		for mean in ['GE_MEAN', 'GNV_MEAN', 'GP_MEAN', 'DO_MEAN']:				# Iterates over all fule type means
			try:
				row.append(data[mean])											# Appends to final result
			except KeyError:
				row.append(nan)

		result_df.loc[i] = row													# Appends to result data frame


	# Show some data
	if period == 'MONTH':
		print len(result_df)
		periodic_analysis.loc['741NKH'].T.plot.bar()
		plt.show()