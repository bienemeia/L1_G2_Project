from helper_functions import firebase, process
import pyrebase
import json
import sqlite3
from datetime import datetime
import time
import random

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
	
	data = firebase.getValues(hive_db, 1)
	db = sqlite3.connect("hiveDB.db")
	db.row_factory = sqlite3.Row
	cursor=db.cursor()
	date = datetime.today().strftime('%Y-%m-%d')
	test = 1
	
	# Loop for testing and initially populating SQLite table
	for i in range(1440):
		time = getFormattedTime(i)
		print(time)
		temp = [round(random.uniform(-30, 30), 1), round(random.uniform(-30, 30), 1), round(random.uniform(-30, 30), 1)]
		humidity = [random.randrange(0,100), random.randrange(0,100), random.randrange(0,100)]
		pressure = round(random.uniform(100, 101.5), 2)
		co2 = random.randrange(2500,3000)
		#cursor.execute('''insert into testDB values (?,?,?,?,?,?,?,?,?,?)''',
		#	(time, date, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2, test))

	# while True:
		# data = firebase.getValues(hive_db, 1)
		# db = sqlite3.connect("hiveDB.db")
		# db.row_factory = sqlite3.Row
		# cursor=db.cursor()
		
		# for key, values in data.items():
			# print(key)
			# temperature = process.getTemperatures(values)
			# humidity = process.getHumidity(values)
			# pressure = process.getPressure(values)
			# co2 = process.getCo2(values)
			# test = process.getTest(values)
			# #print(test)
			
			# cursor.execute('''insert into testDB values (?,?,?,?,?,?,?,?,?,?)''',
			# (key, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2, test))
		# db.commit()
		# db.close()
		
		# time.sleep(30)
		
		
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
