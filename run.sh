#!/bin/bash

# run python script
python timestamp_table.py testTable input.txt : byCols

# save content in html format
# echo -e "<pre> \n" > /var/www/html/results.html
# (cat logFile.txt) >> /var/www/html/results.html
# echo -e "\n </pre>" >> /var/www/html/results.html

# destroy log file
cat logFile.txt
rm *.pyc logFile.txt


