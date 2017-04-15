#########################################################################################
#
# Replaces semicolon by comas and outputs the result in a proper .csv file.
#
# USAGE:   $python fix-csv-file.py [input file] [output file]
# FLAGS:   --date (changes date format from DATE/DATE/DATE to DATE,DATE,DATE)
#
#########################################################################################


import sys


def fix_csv_file(input_file_name, output_file_name, fix_date, fix_NaN):
	"""
	Replaces semicolon by comas and outputs the result in a proper .csv file.

	@input_file_name: .csv file name where ";" is suposed to be the column separator.
	@output_file_name: .csv file name to be created.
	@fix_date: flag, if true, converts "DATE/DATE/DATE" to "DATE,DATE,DATE".
	@fix_NaN: Useg for files who has a "," in the end of the line. Flag, if true, removes the last comma.

	@return: none
	"""
	input_file = open(input_file_name, "r")
	output_file = open(output_file_name, "w")
	
	for line in input_file:
		# Replaces semicolon for comas
		fixed_line = line.replace(";", ",")

		# Changes date from "DATE/DATE/DATE" to "DATE,DATE,DATE"
		if fix_date:
			fixed_line = fixed_line.replace("/", ",")	

		# Fixes last comma problem
		if fix_NaN:
			fixed_line = fixed_line[:fixed_line.rfind(',')] + '\n'

		# Write line to final file
		output_file.write(fixed_line)

	input_file.close()
	output_file.close()


sys_input = sys.argv

# Prints help message
if sys_input[-1] == 'help':
	print "Replaces semicolon by comas and outputs the result in a proper .csv file."
	print "USAGE: fix-csv-file.py [input file name].csv [output file name].csv"
	print "OPTIONAL: --date"

# Proper usage of script without flags
elif len(sys_input) == 3:
	fix_csv_file(sys_input[1], sys_input[2], False, False)

# Proper usage of script with "--date" flag
elif len(sys_input) == 4 and sys_input[-1] == "--date":
	fix_csv_file(sys_input[1], sys_input[2], True, False)

# Proper usage of script with "--comma" flag
elif len(sys_input) == 4 and sys_input[-1] == "--comma":
	fix_csv_file(sys_input[1], sys_input[2], False, True)

# Proper usage of script with both flags
elif len(sys_input) == 5 and "--date" in (sys_input[3], sys_input[4]) and "--comma" in (sys_input[3], sys_input[4]):
	fix_csv_file(sys_input[1], sys_input[2], True, True)

# Wrong usage of script
else:
	print "PROPER USAGE: fix-csv-file.py [input file name].csv [output file name].csv"
	print "OPTIONAL: --date"