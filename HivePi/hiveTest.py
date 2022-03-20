from helper_functions import firebase
import pyrebase
import random
import time
import json
import random
from datetime import date, datetime

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
		
	# Testing, adds an entry for every minute in a 24-hour period
	for i in range(1440):
		time = getFormattedTime(i)
		temp = [round(random.uniform(-30, 30), 1), round(random.uniform(-30, 30), 1), round(random.uniform(-30, 30), 1)]
		humidity = [random.randrange(0,100), random.randrange(0,100), random.randrange(0,100)]
		pressure = round(random.uniform(100, 101.5), 2)
		co2 = random.randrange(2500,3000)
		
		# Push values to Firebase DB
		firebase.pushTemperatureTest(hive_db, 1, time, temp[0], temp[1], temp[2])
		firebase.pushHumidityTest(hive_db, 1, time, humidity[0], humidity[1], humidity[2])
		firebase.pushPressureTest(hive_db, 1, time, pressure)
		firebase.pushCo2Test(hive_db, 1, time, co2)
		firebase.pushDateTest(hive_db, 1, time)
	
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

