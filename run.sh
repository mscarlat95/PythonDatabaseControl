#!/bin/bash

tableName=inputFile=separator=direction=""

function removeWhiteSpaces() {
	echo "$(echo -e "${1}" | tr -d '[:space:]')"
}

function initializeValues {
	echo "Initializing values ..."
	tableName=$(removeWhiteSpaces $1)
	inputFile=$(removeWhiteSpaces $2)
	separator=$(removeWhiteSpaces $3)
	direction=$(removeWhiteSpaces $4)
}

function execute() {
	echo "Executing script ..."
	python timestamp_table.py $tableName $inputFile $separator $direction
}

function saveResult() {
	echo "Saving results ..."
	echo -e "<pre> \n" > results.html
	(cat logFile.txt) >> results.html
	echo -e "\n </pre>" >> results.html
}

function clean() {
	echo "Cleaning dump files ..."
	rm *.pyc
}

# check number of arguments
if [ $# -eq 4 ]
then
	initializeValues $1 $2 $3 $4;
	execute;
	saveResult;
	clean;
else
	echo "Usage: ./run.sh <tableName> <inputFile> <separator> <direction>"
fi

