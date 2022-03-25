import pyrebase
import json
import sqlite3
import datetime
import time
import random

def processWeekly(cursor, dayOfWeek, dayOfMonth):
	# Want to process the averages of all values over 1 hour
	return
	
# 
def processWeeklyAverages(cursor, dayOfWeek):
	# Can get time and date from beginning of day, since doing processing at end of day
	try:
		date = cursor.execute(''' SELECT date FROM dailyDB ''').fetchone()[0]
	except:
		print("Problem searching table")

	# Loop through every hour and minute, averaging all values over 1 hour
	for hour in range(24):
		sumTempBase = 0
		sumTempInside = 0
		sumTempOutside = 0
		sumHumidBase = 0
		sumHumidInside = 0
		sumHumidOutside = 0
		sumCo2 = 0
		sumPressure = 0
		for minute in range(60):
			# Get tempBase at time
			try:
				values = cursor.execute(''' SELECT tempBase, tempInside, tempOutside, humidityBase, humidityInside,
					humidityOutside, co2, pressure FROM dailyDB WHERE time=? ''', 
					(getFormattedTime(minute+(hour*60)),)).fetchone()
			except:
				print("Problem searching table")
				
			# Sum all values within 1 hour
			sumTempBase += values[0]
			sumTempInside += values[1]
			sumTempOutside += values[2]
			sumHumidBase += values[3]
			sumHumidInside += values[4]
			sumHumidOutside += values[5]
			sumCo2 += values[6]
			sumPressure += values[7]
			
		# Calculate averages over 3 hours
		avgTempBase = round(sumTempBase/60, 2)
		avgTempInside = round(sumTempInside/60, 2)
		avgTempOutside = round(sumTempOutside/60, 2)
		avgHumidBase = round(sumHumidBase/60, 2)
		avgHumidInside = round(sumHumidInside/60, 2)
		avgHumidOutside = round(sumHumidOutside/60, 2)
		avgCo2 = round(sumCo2/60, 2)
		avgPressure = round(sumPressure/60, 2)
		
		# Get dayHour string in format 'dayOfWeek-hour'
		dayHour = str(dayOfWeek)+"-"+str(hour)
		
		# Post values to DB
		try:
			cursor.execute(''' INSERT OR REPLACE INTO weeklyDB values (?,?,?,?,?,?,?,?,?,?,?)''', 
							(dayHour, hour, date, 
							avgTempBase, avgTempInside, avgTempOutside,
							avgHumidBase, avgHumidInside, avgHumidOutside,
							avgPressure, avgCo2))
		except:
			print("Problem inserting values into table")

def processMonthlyAverages(cursor, dayOfMonth):
	# Can get time and date from beginning of day, since doing processing at end of day
	try:
		date = cursor.execute(''' SELECT date FROM dailyDB ''').fetchone()[0]
	except:
		print("Problem searching table")

	# Loop through every hour and minute, averaging all values over 1 hour
	
	for hour in range(0,24,3):
		sumTempBase = 0
		sumTempInside = 0
		sumTempOutside = 0
		sumHumidBase = 0
		sumHumidInside = 0
		sumHumidOutside = 0
		sumCo2 = 0
		sumPressure = 0
		for minute in range(180):
			# Get tempBase at time
			try:
				values = cursor.execute(''' SELECT tempBase, tempInside, tempOutside, humidityBase, humidityInside,
					humidityOutside, co2, pressure FROM dailyDB WHERE time=? ''', 
					(getFormattedTime(minute+(hour*60)),)).fetchone()
			except:
				print("Problem searching table")
				
			# Sum all values within 1 hour
			sumTempBase += values[0]
			sumTempInside += values[1]
			sumTempOutside += values[2]
			sumHumidBase += values[3]
			sumHumidInside += values[4]
			sumHumidOutside += values[5]
			sumCo2 += values[6]
			sumPressure += values[7]
			
		# Calculate averages over 1 hour
		avgTempBase = round(sumTempBase/180, 2)
		avgTempInside = round(sumTempInside/180, 2)
		avgTempOutside = round(sumTempOutside/180, 2)
		avgHumidBase = round(sumHumidBase/180, 2)
		avgHumidInside = round(sumHumidInside/180, 2)
		avgHumidOutside = round(sumHumidOutside/180, 2)
		avgCo2 = round(sumCo2/180, 2)
		avgPressure = round(sumPressure/180, 2)
		
		# Get dayHour string in format 'dayOfWeek-hour'
		dayHour = str(dayOfMonth)+"-"+str(hour)
		
		# Post values to DB
		try:
			cursor.execute(''' INSERT OR REPLACE INTO monthlyDB values (?,?,?,?,?,?,?,?,?,?,?)''', 
							(dayHour, hour, date, 
							avgTempBase, avgTempInside, avgTempOutside,
							avgHumidBase, avgHumidInside, avgHumidOutside,
							avgPressure, avgCo2))
		except:
			print("Problem inserting values into table")
						
def processYearlyAverages(cursor):
	# Can get time and date from beginning of day, since doing processing at end of day
	try:
		date = cursor.execute(''' SELECT date FROM dailyDB ''').fetchone()[0]
	except:
		print("Problem searching table")

	# Loop through every hour and minute, averaging all values over 1 hour
	sumTempBase = 0
	sumTempInside = 0
	sumTempOutside = 0
	sumHumidBase = 0
	sumHumidInside = 0
	sumHumidOutside = 0
	sumCo2 = 0
	sumPressure = 0
	for hour in range(0,24,3):
		for minute in range(180):
			# Get tempBase at time
			try:
				values = cursor.execute(''' SELECT tempBase, tempInside, tempOutside, humidityBase, humidityInside,
					humidityOutside, co2, pressure FROM dailyDB WHERE time=? ''', 
					(getFormattedTime(minute+(hour*60)),)).fetchone()
			except:
				print("Problem searching table")
				
			# Sum all values within 1 hour
			sumTempBase += values[0]
			sumTempInside += values[1]
			sumTempOutside += values[2]
			sumHumidBase += values[3]
			sumHumidInside += values[4]
			sumHumidOutside += values[5]
			sumCo2 += values[6]
			sumPressure += values[7]
			
	# Calculate averages over 1 day
	avgTempBase = round(sumTempBase/1440, 2)
	avgTempInside = round(sumTempInside/1440, 2)
	avgTempOutside = round(sumTempOutside/1440, 2)
	avgHumidBase = round(sumHumidBase/1440, 2)
	avgHumidInside = round(sumHumidInside/1440, 2)
	avgHumidOutside = round(sumHumidOutside/1440, 2)
	avgCo2 = round(sumCo2/1440, 2)
	avgPressure = round(sumPressure/1440, 2)
		
	# Post values to DB
	try:
		cursor.execute(''' INSERT OR REPLACE INTO yearlyDB values (?,?,?,?,?,?,?,?,?)''', 
						(date, 
						avgTempBase, avgTempInside, avgTempOutside,
						avgHumidBase, avgHumidInside, avgHumidOutside,
						avgPressure, avgCo2))
	except:
		print("Problem inserting values into table")


def getDailyArray(cursor):
	values = {'time':[], 'date':[], 'tempBase':[], 'tempInside':[], 'tempOutside':[],
		'humidityBase':[], 'humidityInside':[], 'humidityOutside':[],
		'pressure':[], 'co2':[]}
	try:
		tempBase = cursor.execute('''SELECT time, date, tempBase, tempInside, tempOutside, 
			humidityBase, humidityInside, humidityOutside,
			pressure, co2 FROM dailyDB ORDER BY date, time''').fetchall()
	except:
		print("Problem searching table")
		
	for row in tempBase:
		values["time"].append(row[0])
		values["date"].append(row[1])
		values["tempBase"].append(row[2])
		values["tempInside"].append(row[3])
		values["tempOutside"].append(row[4])
		values["humidityBase"].append(row[5])
		values["humidityInside"].append(row[6])
		values["humidityOutside"].append(row[7])
		values["pressure"].append(row[8])
		values["co2"].append(row[9])
		
	return values


# Get DB cursor for hiveDB.db
def getDBCursor(db):
	db.row_factory = sqlite3.Row
	return db.cursor()
	

### The following methods are for setting up the system with DBs

# Method for creating daily DB
# Only to be used if DB doesn't exist on system
def createDailyDB(cursor):
	try:
		cursor.execute('''CREATE TABLE dailyDB 
			(time TEXT, date TEXT, 
			tempBase REAL, tempInside REAL, tempOutside REAL, 
			humidityBase REAL, humidityInside REAL, humidityOutside REAL,
			pressure REAL, co2 REAL,
			UNIQUE(time))''')
	except:
		print("Problem creating table")

# Method for creating weekly DB 
# Only to be used if DB doesn't exist on system
def createWeeklyDB(cursor):
	try:
		cursor.execute('''CREATE TABLE weeklyDB 
			(dayHour TEXT, hour INT, date TEXT, 
			tempBase REAL, tempInside REAL, tempOutside REAL, 
			humidityBase REAL, humidityInside REAL, humidityOutside REAL,
			pressure REAL, co2 REAL,
			UNIQUE(dayHour))''')
	except:
		print("Problem creating table")
		
# Method for creating monthly DB 
# Only to be used if DB doesn't exist on system
def createMonthlyDB(cursor):
	try:
		cursor.execute('''CREATE TABLE monthlyDB 
			(dayHour TEXT, hour INT, date TEXT, 
			tempBase REAL, tempInside REAL, tempOutside REAL, 
			humidityBase REAL, humidityInside REAL, humidityOutside REAL,
			pressure REAL, co2 REAL,
			UNIQUE(dayHour))''')
	except:
		print("Problem creating table")
		
# Method for creating yearly DB 
# Only to be used if DB doesn't exist on system
def createYearlyDB(cursor):
	try:
		cursor.execute('''CREATE TABLE yearlyDB 
			(date TEXT, 
			tempBase REAL, tempInside REAL, tempOutside REAL, 
			humidityBase REAL, humidityInside REAL, humidityOutside REAL,
			pressure REAL, co2 REAL,
			UNIQUE(date))''')	
	except:
		print("Problem creating table")

# Method to format time given an integer
def getFormattedTime(num):
	hr = num//60
	mn = num%60
	time = [hr, mn]
	if hr < 10:
		time[0] = "0" + str(hr)
	if mn < 10:
		time[1] = "0" + str(mn)
	return(str(time[0]) + ":" + str(time[1]))
	
# Method for creating test values in DB
def testValues(cursor):
	for i in range(1440):
		now = getFormattedTime(i)
		date = datetime.date.today()
		temperature = [round(random.uniform(-20,20),2), round(random.uniform(-20,20),2), round(random.uniform(-20,20),2)]
		humidity = [random.randint(0,100), random.randint(0,100), random.randint(0,100)]
		pressure = round(random.uniform(100,150),2)
		co2 = random.randint(330,600)
		try:
			cursor.execute('''INSERT OR REPLACE INTO dailyDB values (?,?,?,?,?,?,?,?,?,?)''',
				(now, date, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2))	
		except:
			print("Problem inserting values into database")
