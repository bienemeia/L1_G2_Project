import pyrebase
import random
import time
import json
from datetime import date, datetime

meia_config = {
	"apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
	"authDomain":"testhive-2bca5.firebaseapp.com",
	"databaseURL":"https://testhive-2bca5-default-rtdb.firebaseio.com/",
	"storageBucket":"testhive-2bca5.appspot.com"
}

# graham_config = {
# 	"apiKey": "AIzaSyDA_s8XGscNq3BIoU8PSS2pU6htnQ73RJE",
# 	"authDomain": "sandbox-99e4a.firebaseapp.com",
# 	"databaseURL": "https://sandbox-99e4a-default-rtdb.firebaseio.com",
# 	"storageBucket": "sandbox-99e4a.appspot.com"
# }

# graham_firebase = pyrebase.initialize_app(graham_config)
# graham_db = graham_firebase.database()

hive_firebase = pyrebase.initialize_app(meia_config)
hive_db = hive_firebase.database()

today = str(date.today())
now = str(datetime.now().time())

# Sample data
data_json = {
	"001" : { # device id, can have multiple hives.
		"name" : "Big Bertha", # optional, if giving each hive a nickname
		"values" : [ # making this a subset, as there will be lots of datetimes. Access will be easier.
			{ now : # will have 1 of these for every minute of the day -> 1440
				{
					"date" : today,
					"temperature" : {
						"inside" : 1.5,
						"outside" : -2,
						"base" : 0
					},
					"humidity" : {
						"inside" : 75,
						"outside" : 40,
						"base" : 63
					},
					"pressure" : 101.2, #kPa
					"co2" : 320 #PPM
				}
			},
		],
		# checking whethere there is ice or snow
		"iceStatus" : False,
		# checking status of different mechanisms
		"heaterStatus" : False,
		"flapperStatus" : False,
		"fanStatus" : False,
		"testLED1" : False,
		"testLED2" : False
	}
}

# Initial set up of DB
hive_db.child("hives").child(1).child("name").set("Big Bertha")
hive_db.child("hives").child(1).child("values").child(now).child("date").set(today)

hive_db.child("hives").child(1).child("values").child(now).child("temperature").child("outside").set(25)
hive_db.child("hives").child(1).child("values").child(now).child("temperature").child("inside").set(20)
hive_db.child("hives").child(1).child("values").child(now).child("temperature").child("base").set(24.3)

hive_db.child("hives").child(1).child("values").child(now).child("humidity").child("outside").set(75)
hive_db.child("hives").child(1).child("values").child(now).child("humidity").child("inside").set(80)
hive_db.child("hives").child(1).child("values").child(now).child("humidity").child("base").set(76)

hive_db.child("hives").child(1).child("values").child(now).child("co2").set(332)
hive_db.child("hives").child(1).child("values").child(now).child("pressure").set(101.5)

hive_db.child("hives").child(1).child("iceStatus").set(False)
hive_db.child("hives").child(1).child("heaterStatus").set(False)
hive_db.child("hives").child(1).child("flapperStatus").set(False)
hive_db.child("hives").child(1).child("fanStatus").set(False)

def writeData():
	
	hive_db.child("hives").push(data)

	t = sense.get_temperature()
		meia_db.child(dataset_t).child(key).set(t)

def readData(name, db):

	data_t = db.child(dataset_t).get()
	data_p = db.child(dataset_p).get()
	data_h = db.child(dataset_h).get()
	
	data_t_list = data_t.each()
	threePoints_t = [data_t_list[-1], data_t_list[-2], data_t_list[-3]]
	
	data_p_list = data_p.each()
	threePoints_p = [data_p_list[-1], data_p_list[-2], data_p_list[-3]]
	
	data_h_list = data_h.each()
	threePoints_h = [data_h_list[-1], data_h_list[-2], data_h_list[-3]]
	
	temp_message = name + "'s " + "last 3 temps are: {}, {}, {}".format(
		threePoints_t[0].val(), threePoints_t[1].val(), threePoints_t[2].val(),)
	pressure_message = name + "'s " + "last 3 pressures are: {}, {}, {}".format(
		threePoints_p[0].val(), threePoints_p[1].val(), threePoints_p[2].val(),)
	humidity_message = name + "'s " + "last 3 humidities are: {}, {}, {}".format(
		threePoints_h[0].val(), threePoints_h[1].val(), threePoints_h[2].val(),)
	
	print(temp_message)
	print(pressure_message)
	print(humidity_message)
	
# writeData()
# readData("Meia", meia_db)
# readData("Graham", graham_db)
