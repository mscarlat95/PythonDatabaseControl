import io
from datetime import datetime

def getTimeStamp():
	timestamp = datetime.now() 
	return str (timestamp.strftime('%Y/%m/%d %H:%M:%S') + ":\t")

def clearLogFile():
	with open("logFile.txt", "w"):
		pass

def updateLogFile(message):
	with open("logFile.txt", "a") as fout:
		fout.write (getTimeStamp() + message + "\n\n")
