# Anomaly Detection

### Setting Up

* First, install Python 2.7 from <http://python.org>
* Then, with pip, install `pandas`
```
$pip install pandas
```

### About the files

_Note: For all the following python scripts, Windows users do not need to call `python` before the command._

#### fix-csv-file.py

_Note: this is an ad hoc program to solve specific problems encountered in .csv files needed for this research._

Changes semicolon separeted `.csv` to comma separated `.csv`. There is also an option to remove a last empty column (use `--comma`) and another to change date format from `DAY/MONTH/YEAR` to `DAY,MONTH,YEAR` (use `--date`), i.e., to treat days, months and years as separeted columns.

```
USAGE: $python fix-csv-file.py [input file] [output file]
FLAGS: --date (changes date format from DATE/DATE/DATE to DATE,DATE,DATE)
```

#### preprocessing.py

Generates two output files, `monthly_grouped.csv` and `quarterly_grouped.csv`. In the first one, data is grouped by month, in the second one, data is grouped by quarter. The input `.csv` file must have at least the following columns:

ID | YEAR | MONTH | DAY | FUEL_TYPE | AMOUNT

The output `.csv` will have the following columns:

* Monthly Grouped

ID | YEAR | MONTH | FUEL_TYPE | AMOUNT | FREQUENCY | MEAN | STD

* Quarterly Grouped

ID | YEAR | QUARTER | FUEL_TYPE | AMOUNT | FREQUENCY | MEAN | STD

Where:

**ID**: License plate  
**YEAR**: Year of refuel  
**MONTH**: Month of refuel  
**QUARTER**: Quarter of refuel  
**FUEL_TYPE**: Fuel type  
**AMOUNT**: Refuel amount  
**FREQUENCY**: Frequency of refuel (monthly or quarterly)  
**MEAN**: Mean of refuel amount (monthly or quarterly)  
**STD**: Standard deviation of refuel amount (monthly or quarterly)  

_Note: Fuel type can be:_  
**GASOLINAESPECIAL**: 1  
**GASNATURALVEHICULAR**: 2  
**GASOLINAPREMIUM**: 3  
**DIESELOIL**: 4  

The program also offers an option to normalize the refuel amount (AMOUNT) with respect to the maximum refuel amount in the input `.csv` file (use `--norm`). The mean and standard deviation are calculated using the normalized values.

```
USAGE:  $python preprocessing.py [input file name]
OPTION: $python preprocessin.py [input file name] [output file path]
FLAGS:  --norm (normalizes the fuel amount)
```

_Note: If no output file path is specified, the files goes to `/output` folder (creates one if necessary)._