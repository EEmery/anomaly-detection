
import pandas as pd

df = pd.read_csv("Data/gas_stations_database--fixed_date.csv")

# Clusters by individuals and sorts by timestamp
print df.sort_values(['ID', 'YEAR', 'MONTH', 'DAY'], ascending=False)