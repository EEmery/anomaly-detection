# Imports necessary libraries
print "Importing packages\n"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from warnings import filterwarnings


# Ignores warnings
filterwarnings("ignore")


input_file_path = "Data/preprocessed/statistical_analysis/not-normalized/"
output_file_path = "Data/preprocessed/frequency_analysis/"
periods = ['DAY', 'WEEK', 'MONTH', 'QUARTER', 'SEMESTER'][::-1]
periods_amounts = [365, 53, 12, 4, 2][::-1]
file_names = ['daily', 'weekly', 'monthly', 'quarterly', 'semesterly'][::-1]


# Iterates over all periods
for period, period_amount, file_name in zip(periods, periods_amounts, file_names):

	print "Making " + file_name + " analysis"
	
	# Opens file (related to the period)
	periodic_analysis = pd.read_csv(input_file_path + file_name + '_analysis.csv')

	# Remover YEAR necessity by increasing period limits
	periodic_analysis[period] = periodic_analysis[period] + (periodic_analysis['YEAR'] - 2015) * period_amount

	# Slices data frame to get only necessary columns
	periodic_analysis = periodic_analysis[['ID', period, 'GE_MEAN', 'GNV_MEAN', 'GP_MEAN', 'DO_MEAN']]

	# Creates an empty data frame with the same shape as the periodic analysis for the result
	result_df = periodic_analysis.copy()
	result_df['FREQUENCY'] = 0
	result_df.ix[:, 2:] = 0

	# Reshapes data frame to desired shape
	periodic_analysis = periodic_analysis.set_index(['ID', period]).stack(dropna=False).unstack(1)
	result_df = result_df.set_index(['ID', period]).stack(dropna=False).unstack(1)

	
	# Get all ID's to iterate over
	IDS = periodic_analysis.index.get_level_values(0).unique()

	
	# Iterates over the ID's counting the behaviour between days
	for ID in IDS:
		count = 1
		for STAMP in periodic_analysis.columns:
			
			try:
				if periodic_analysis.loc(axis=0)[ID][STAMP].dropna().empty:
					count += 1 if STAMP != 1 else 0
					if STAMP == periodic_analysis.columns[-1]:
						raise KeyError
				else:
					raise KeyError

			except KeyError:
				sum = np.nansum([np.array(result_df.loc(axis=0)[ID][count][:-1]), np.array(periodic_analysis.loc(axis=0)[ID][STAMP])], axis=0)
				freq = np.nansum([result_df.loc(axis=0)[ID][count][-1], 1], axis=0)
				result_df.set_value(ID, count, np.append(sum, freq))
				count = 1
		result_df.loc(axis=0)[ID][:'DO_MEAN'] = np.array(result_df.loc(axis=0)[ID][:'DO_MEAN'] / result_df.loc(axis=0)[ID, 'FREQUENCY'])

	# Saves result dataframe
	print "Saving " + file_name + " analysis\n"
	result_df.reset_index().rename(columns={'level_1':'FUEL_TYPE'}).to_csv(output_file_path + file_name + "_analysis.csv", index=False, header=True)
			

	# Show some data
	if period == 'SEMESTER':
		pass

		#print periodic_analysis.head(10)
		#print result_df.head(30)

		#periodic_analysis.loc['741NKH'].T.plot.bar()
		#periodic_analysis.loc['4030PAF'].T.plot.bar()
		#result_df.loc['741NKH'].T.plot.bar()
		#result_df.loc['4030PAF'].T.plot.bar()
		#result_df.loc['1517YDG', :3].T.plot.bar()
		#result_df.loc['1517YDG'].T.plot.bar()
		#result_df.loc['1512KLC'].T.plot.bar()

		#plt.show()