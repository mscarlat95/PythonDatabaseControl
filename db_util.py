import mysql.connector
from mysql.connector import Error
import log_util as log

# mysql information
_host = "localhost"
_database = "demoDB"
_user = "root"
_password = "root"
conn = "" #unset

# check if db is connected and try to reconnect 
def check_is_connected():
	global conn

	if conn.is_connected() == False:
		log.updateLogFile("Connection lost\n Trying to reconnect ...")

		atttempts = 3
		status = False
		for i in xrange(atttempts):
			connect()

			status = conn.is_connected()
			if status == True:
				break
			time.sleep (100)

		# still disconnected
		if status == False:
			log.updateLogFile("Cannot connect to the database. Exiting ...")
			sys.exit(0)

# connect to database
def connect():
	global conn;
	try:
		conn = mysql.connector.connect (host = _host,
										database = _database,
										user = _user,
										password = _password)
		if conn.is_connected():
			log.updateLogFile("Opening connection ... ")
		else:
			check_is_connected()
	except Error as e:
		log.updateLogFile(str(e))

# peform mysql query 
def performQuery(command):
	global conn
	cursor = ""

	log.updateLogFile("Perform:\t" + command)
	try:
		cursor = conn.cursor()
		cursor.execute (command)
	except Error as e:
		print e
	finally:
		return cursor

# add new column in the current table 
def addColumn(tableName, column, columnType):

	# check if column exists
	command = "SHOW COLUMNS FROM %s LIKE \"%s\";" % (tableName, column)
	cursor = performQuery(command)
	rows = cursor.fetchall()

	# column doesnt exist --> add into table
	if len(rows) == 0:
		command = "ALTER TABLE %s ADD %s %s;" % (tableName, column, columnType)
		performQuery(command)
		conn.commit()


def createTable(tableName, hashset):
	global conn
	check_is_connected()

	command = "SHOW TABLES LIKE '%s'" % tableName
	cursor = performQuery(command)
	result = cursor.fetchone()
	if result:
		# update table columns in case of existing
		command = "SELECT %s FROM %s;" % ("*", tableName)
		cursor = performQuery(command)
		rows = cursor.fetchall()
		if len (rows) != 0:
			for key, value in hashset.iteritems():
				addColumn(tableName, key, "varchar(30)");
			log.updateLogFile("Table %s is updated" % tableName)
	else:
		# create table is it doesn t exist in database
		command = "CREATE TABLE IF NOT EXISTS %s (" % tableName
		for key, value in hashset.iteritems():
			command += key + " varchar(30), "
		command = command[0: len(command) - 2] + ");"
		cursor = performQuery(command)
		log.updateLogFile("Table %s is created" % tableName)

	

def insertIntoTable(tableName, hashset):
	global conn
	keys = values = ""

	for key, value in hashset.iteritems():
		keys += key + ", "
		values += "\"" + value + "\", "

	keys = keys[0: len(keys) - 2]
	values = values[0: len(values) - 2]

	command = "INSERT INTO %s(%s) values(%s);" % (tableName, keys, values)
	performQuery(command)
	conn.commit()

	log.updateLogFile("Insert in table %s done!" % tableName)


def displayTableContent(tableName, field):
	check_is_connected()

	command = "SELECT %s FROM %s;" % (field, tableName)
	cursor = performQuery(command)
	rows = cursor.fetchall()

	count = 0
	delimitator = ""
	result = ""

	# print column names
	for field in cursor.description:
		fld = str(field[0]) + "       \t       "
		count += len(fld) + 2
		result += fld
	else:
		result += "\n"

	for i in xrange(count):
		delimitator += "-"
	result += delimitator + "\n"

	# print rows 
	for row in rows:
		for i in xrange(len(row)):
			result += (str(row[i]) + "      \t      ")
		else:
			result += "\n"

	log.updateLogFile("Printing %s 's records:\n %s " % (tableName, result))

def clearTable(tableName):
	command = "TRUNCATE %s;" % tableName
	performQuery(command)
	conn.commit()
	log.updateLogFile("Cleared table %s " % tableName)

def disconnect():
	try:
		cursor = conn.cursor()
		cursor.close()
		conn.close()
	except Error as e:
		print e

	log.updateLogFile("Closing connection ... ")