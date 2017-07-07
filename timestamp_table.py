import sys
import log_util as log
import db_util as db
import parse_util as parser

if __name__ == "__main__":

	# check input arguments 
	if len(sys.argv) != 5:
		print "Usage: python timestamp_table.py <tableName> <inputFile> <separator> <direction>" 
		sys.exit(0)

	# initialize info
	tableName = sys.argv[1]
	inputFile = sys.argv[2]
	separator = sys.argv[3]
	direction = sys.argv[4]

	log.clearLogFile()

	# connect to the database
	db.connect()
	
	# create dictionary based on inputFile's content 
	hashset = {}
	try:
		hashset = parser.parseFile(inputFile, direction, separator)
	except ValueError as err:
		log.updateLogFile(str(err))
		db.disconnect()
		sys.exit(0)

	# create table if it doesn't exists
	db.createTable(tableName, hashset)

	# insert info into table
	db.insertIntoTable(tableName, hashset)

	# display records 
	db.displayTableContent(tableName, "*")

	# clear table
	# db.clearTable(tableName)

	# close connection to database
	db.disconnect()