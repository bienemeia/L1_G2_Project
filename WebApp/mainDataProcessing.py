import sys
sys.path.append('..')
from helper_functions import firebase, process
import pyrebase
import json
import sqlite3
from datetime import datetime
import time

def main():
	
	# Set up Firebase authentication
	meia_config = {
	"apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
	"authDomain":"testhive-2bca5.firebaseapp.com",
	"databaseURL":"https://testhive-2bca5-default-rtdb.firebaseio.com/",
	"storageBucket":"testhive-2bca5.appspot.com"
	}
	# Initialize Firebase DB
	hive_firebase = pyrebase.initialize_app(meia_config)
	hive_db = hive_firebase.database()

	while True:
		now = firebase.getTime()
		db = sqlite3.connect("hiveDB.db")
		db.row_factory = sqlite3.Row
		cursor=db.cursor()
		createDB()
				
		date = firebase.getDate(hive_db, 1, now)
		tempDict = firebase.getTemperature(hive_db, 1, now)
		temperature = [tempDict['base'], tempDict['inside'], tempDict['outside']]
		humidityDict = firebase.getHumidity(hive_db, 1, now)
		humidity = [humidityDict['base'], humidityDict['inside'], humidityDict['outside']]
		pressure = firebase.getPressure(hive_db, 1, now)
		co2 = firebase.getCo2(hive_db, 1, now)
		
		cursor.execute('''INSERT OR REPLACE INTO dailyDB values (?,?,?,?,?,?,?,?,?,?)''',
			(now, date, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2))	

		db.commit()
		db.close()
		
		time.sleep(30)
		
# Method for setting up DB only
def createDB(cursor):
	cursor.execute('''CREATE TABLE dailyDB 
		(time TEXT, date TEXT, 
		tempBase REAL, tempInside REAL, tempOutside REAL, 
		humidityBase REAL, humidityInside REAL, humidityOutside REAL,
		pressure REAL, co2 REAL,
		UNIQUE(time))''')
		
def getFormattedTime(num):
	hr = num//60
	mn = num%60
	time = [hr, mn]
	if hr < 10:
		time[0] = "0" + str(hr)
	if mn < 10:
		time[1] = "0" + str(mn)
	return(str(time[0]) + ":" + str(time[1]))

if __name__ == "__main__":
	main()
