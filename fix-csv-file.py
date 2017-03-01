import sys

def fix_csv_file(input_file_name, output_file_name):
	"""
	Replaces semicolon by comas and outputs the result in a proper .csv file.

	@input_file_name: .csv file name where ";" is suposed to be the column separator.
	@output_file_name: .csv file name to be created.

	@return: none
	"""
	input_file = open(input_file_name, "r")
	output_file = open(output_file_name, "w")
	
	for line in input_file:
		output_file.write(line.replace(";", ","))

	input_file.close()
	output_file.close()


sys_input = sys.argv

# Prints help message
if sys_input[-1] == 'help':
	print "Replaces semicolon by comas and outputs the result in a proper .csv file."
	print "USAGE: fix-csv-file.py [input file name].csv [output file name].csv"

# Proper usage of script
elif len(sys_input) == 3:
	_, input_file, output_file = sys.argv
	fix_csv_file(input_file, output_file)

# Wrong usage of script
else:
	print "PROPER USAGE: fix-csv-file.py [input file name].csv [output file name].csv"