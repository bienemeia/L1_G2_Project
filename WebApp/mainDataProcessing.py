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
		print(key)
		
	
	# for time in data, get values.
	
	# test table is called testdata


if __name__ == "__main__":
	main()
