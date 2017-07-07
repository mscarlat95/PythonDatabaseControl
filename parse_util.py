import io
import sys
import log_util as log

invalid_format_err = "Error: Invalid file format. Exiting ..."

# add info into hashset
def updateHashset(hashset, key, value):
	key = key.strip(' \n \t')
	value = value.strip (' \n \t')
	hashset[key] = value
	return hashset


def parseByColumns(inputFile, separator):
	hashset = {}
	with open(inputFile, 'r') as fin:
		for line in fin:
			# obtain [key, value] pair
			pair = line.split (separator)
			if len(pair) != 2:
				log.updateLogFile(invalid_format_err)
				raise ValueError(invalid_format_err)
			# remove white spaces, new lines etc
			hashset = updateHashset(hashset, pair[0], pair[1])
	return hashset


def parseByRows(inputFile, separator):
	hashset = {}

	rows = []
	columns = []
	with open(inputFile, 'r') as fin:
		if len(fin) == 2:
			rows = fin[0].split (separator)
			columns = fin[1].split (separator)
		else:
			raise ValueError(invalid_format_err)

# parse input file content
def parseFile(inputFile, direction, separator):

	result = {}
	try:
		if direction == "byCols":
			result = parseByColumns(inputFile, separator)
		elif direction == "byRows":
			result = parseByRows(inputFile, separator)
	except ValueError as err:
		print err

	if result == {}:
		raise ValueError(invalid_format_err)
	else:
		return result
