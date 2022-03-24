import sys
sys.path.append('..')
from helper_functions import firebase
from helper_functions import arduinoInterface as arduino
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
	
	while True:
			
		# Get values from Arduino
		# Random placeholder values
		# Remember, order is base, inside, outside
		temp = [round(random.uniform(-30, 30), 1), round(random.uniform(-30, 30), 1), round(random.uniform(-30, 30), 1)]
		humidity = [random.randrange(0,100), random.randrange(0,100), random.randrange(0,100)]
		pressure = round(random.uniform(100, 101.5), 2)
		co2 = random.randrange(2500,3000)
		
		# Get test value from arduino
		test = arduino.read()
		
		# Get current time
		time = firebase.getTimeMinus()
		
		# Push values to Firebase DB
		firebase.pushTemperature(hive_db, 1, time, temp[0], temp[1], temp[2])
		firebase.pushHumidity(hive_db, 1, time, humidity[0], humidity[1], humidity[2])
		firebase.pushPressure(hive_db, 1, time, pressure)
		firebase.pushCo2(hive_db, 1, time, co2)
		firebase.pushDate(hive_db, 1, time)
		
		# Get instructions from Firebase DB and send to Arduino
		if firebase.getHeaterStatus(hive_db, 1):
			print("heater activated")
			# activate heater
			
		if firebase.getFlapperStatus(hive_db, 1):
			print("flapper activated")
			# activate flapper
			
		if firebase.getFanStatus(hive_db, 1):
			print("fan activated")
			# activate fan
			
		if firebase.getTestLed1Status(hive_db, 1):
			print("LED1 activated")
			arduino.ledON()
		else:
			arduino.ledOFF()
			
		if firebase.getTestLed2Status(hive_db, 1):
			print("LED2 activated")
			# activate test LED2
			
		# Waits 45 seconds to guarantee having values every minute of the day
		# If data is already present, it is overwritten rather than duplicated
		time.sleep(45)
	
if __name__ == "__main__":
	main()

