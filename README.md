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

Generates four output files, `weekly_analysis.csv`, `monthly_analysis.csv`, `quarterly_analysis.csv` and `semesterly_analysis.csv`. Each of them is grouped to respect to their periods. All refuel amounts in the output files are normalized in respect to the highest refueling in the whole input file (which must not be normalized). The input `.csv` file must have at least the following columns:

ID - YEAR - MONTH - DAY - FUEL_TYPE - AMOUNT

The output `.csv` will have the following columns:

**ID**: License plate  
**YEAR**: Year of refuel  
**SEMESTER**: Quarter of refuel  
**QUARTER**: Quarter of refuel  
**MONTH**: Month of refuel  
**WEEK**: Quarter of refuel  
**FREQUENCY**: Frequency of refuel (monthly or quarterly)  
**TYPE**: Type of vehicle  
**GE**: Special Fuel refueled amount (GASOLINAESPECIAL)  
**GNV**: Natural Gas refueled amount (GASNATURALVEHICULAR)  
**GP**: Premium Fuel refueled amount (GASOLINAPREMIUM)  
**DO**: Disel Oil refueled amount (DISELOIL)  
**GE_RATE**: mean refuel amount difference between first and second halfes of period  
**GNV_RATE**: mean refuel amount difference between first and second halfes of period  
**GP_RATE**: mean refuel amount difference between first and second halfes of period  
**DO_RATE**: mean refuel amount difference between first and second halfes of period  
**GE_MEAN**: mean refuel amount of fuel  
**GNV_MEAN**: mean refuel amount of fuel  
**GP_MEAN**: mean refuel amount of fuel  
**DO_MEAN**: mean refuel amount of fuel  
**GE_STD**: Standard deviation of refuel amount of fuel  
**GNV_STD**: Standard deviation of refuel amount of fuel  
**GP_STD**: Standard deviation of refuel amount of fuel  
**DO_STD**: Standard deviation of refuel amount of fuel  

_Note: SEMESTER, QUARTER, MONTH and WEEK only appear in it's groupings._

_Note: TYPE can be:_  
_AUTOMOVIL: 1_  
_CAMIONETA: 2_  
_JEEP: 3_  
_UNKOWN: 4_  
_VAGONETA: 5_  
_CAMION: 6_  
_OMNIBUS: 7_  
_MOTO: 8_  
_MINIBUS: 9_  
_MICROBUS: 10_  
_VOLQUETA: 11_  

```
USAGE:   $python preprocessing.py

OPTIONS: [input file name]
         [output file path]
         $python preprocessing.py [input file name] [output file path]
```