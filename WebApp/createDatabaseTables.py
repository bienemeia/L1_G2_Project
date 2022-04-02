import sys
sys.path.append('..')
from helper_functions import process, firebase
from flask import Flask, Markup, render_template
import time
import sqlite3
import pyrebase



# Open connection to database
db = sqlite3.connect("hiveDB.db")
cursor = process.getDBCursor(db)

try:
	process.createDailyDB(cursor)
except:
	print("Already created")
	
try:
	process.createWeeklyDB(cursor)
except:
	print("Already created")
	
try:
	process.createMonthlyDB(cursor)
except:
	print("Already created")
	
try:
	process.createYearlyDB(cursor)
except:
	print("Already created")

# Set up Firebase authentication
meia_config = {
	"apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
	"authDomain": "testhive-2bca5.firebaseapp.com",
	"databaseURL": "https://testhive-2bca5-default-rtdb.firebaseio.com/",
	"storageBucket": "testhive-2bca5.appspot.com"
}
# Initialize Firebase DB
hive_firebase = pyrebase.initialize_app(meia_config)
hive_db = hive_firebase.database()
dayOfWeek = 1
dayOfMonth = 1

while True:
	db = sqlite3.connect("hiveDB.db")
	cursor = process.getDBCursor(db)
	now = firebase.getTime()
	updated = False

	date = firebase.getDate(hive_db, 1, now)
	tempDict = firebase.getTemperature(hive_db, 1, now)
	temperature = [tempDict['base'], tempDict['inside'], tempDict['outside']]
	humidityDict = firebase.getHumidity(hive_db, 1, now)
	humidity = [humidityDict['base'], humidityDict['inside'], humidityDict['outside']]
	pressure = firebase.getPressure(hive_db, 1, now)
	co2 = firebase.getCo2(hive_db, 1, now)

	cursor.execute('''INSERT OR REPLACE INTO dailyDB values (?,?,?,?,?,?,?,?,?,?)''',
				   (now, date, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2))

	if not updated and now == "23:59":  # Process data at the end of every day
		process.processWeeklyAverages(cursor, dayOfWeek)
		process.processMonthlyAverages(cursor, dayOfMonth)
		process.processYearlyAverages(cursor)
		updated = True
		if dayOfWeek == 7:
			dayOfWeek = 1
		else:
			dayOfWeek += 1
		if dayOfMonth == 31:
			dayOfMonth = 1
		else:
			dayOfMonth += 1
	if now != "23:59":
		updated = False

	db.commit()
	db.close()

	time.sleep(30)
