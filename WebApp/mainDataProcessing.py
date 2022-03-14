from helper_functions import firebase, process
import pyrebase
import json
import sqlite3
import datetime

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
	
	for key, values in data.items():
		temperature = process.getTemperatures(values)
		humidity = process.getHumidity(values)
		pressure = process.getPressure(values)
		co2 = process.getCo2(values)
		test = process.getTest(values)
		
		cursor.execute('''insert into testDB values (?,?,?,?,?,?,?,?,?,?)''',
		(key, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2, test))
	db.commit()
	db.close()

if __name__ == "__main__":
	main()
