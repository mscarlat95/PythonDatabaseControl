import io
import log_util as log

# add info into hashset
def updateHashset(hashset, key, value):
	key = key.strip(' \n \t')
	value = value.strip (' \n \t')
	hashset[key] = value
	return hashset

# parse input file content
def parseFile(inputFile, separator):
	hashset = {}

	with open(inputFile, 'r') as fin:
		for line in fin:

			# obtain [key, value] pair
			pair = line.split (separator)
			if len(pair) != 2:
				updateLogFile("Error: Invalid file format. Exiting ...")
				sys.exit(0)

			# remove white spaces, new lines etc
			hashset = updateHashset(hashset, pair[0], pair[1])
	return hashset