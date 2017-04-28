# Imports necessary libraries
print "Importing packages\n"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from warnings import filterwarnings


# Ignores warnings
filterwarnings("ignore")


input_file_path = "Data/preprocessed/statistical_analysis/not-normalized/"
output_file_path = "Data/preprocessed/time_interval_analysis/"

print "Making time interval analysis"
	
# Opens file (related to the period)
periodic_analysis = pd.read_csv(input_file_path + 'daily' + '_analysis.csv')

# Creates a time interval column
periodic_analysis['INTERVAL'] = periodic_analysis['DAY'] + (periodic_analysis['YEAR'] - 2015) * 365

# Gets the difference between time intervals
left = periodic_analysis[['ID', 'YEAR', 'DAY', 'GE', 'GNV', 'GP', 'DO']]
right = periodic_analysis[['ID', 'INTERVAL']].groupby('ID').diff()
result_df = pd.merge(left, right, left_index=True, right_index=True)

# Makes date show in the right form
dates = pd.to_datetime(result_df['YEAR'], format="%Y") + pd.to_timedelta(result_df['DAY']-1, unit='d')
result_df['DAY'] = dates.apply(lambda x: x.day)
result_df = pd.merge(result_df, dates.apply(lambda x: x.month).to_frame().rename(columns={0:'MONTH'}), left_index=True, right_index=True)

# Round fuel amounts
rounded = result_df[['GE', 'GNV', 'GP', 'DO']].round().rename(columns={'GE':'GE_R', 'GNV':'GNV_R', 'GP':'GP_R', 'DO':'DO_R'})
result_df = pd.merge(result_df, rounded, left_index=True, right_index=True)

# Sorts and saves result data frame
print "Saving time interval analysis"
result_df = result_df[['ID', 'YEAR', 'MONTH', 'DAY', 'INTERVAL', 'GE', 'GNV', 'GP', 'DO', 'GE_R', 'GNV_R', 'GP_R', 'DO_R']]
result_df = result_df.sort_values(['ID', 'YEAR', 'MONTH', 'DAY'], ascending=False)
result_df.to_csv(output_file_path + "time_interval_analysis.csv", index=False, header=True)