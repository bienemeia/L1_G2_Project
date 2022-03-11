from datetime import date, datetime

# Set the hive name
def pushHiveName(db, hiveId, name):
	db.child("hives").child(hiveId).child("name").set(name)
	
# Get current time in form HH:MM (24 hour)
def getTime():
	now = str(datetime.now().time())
	now = now.split(":", 2)
	hr = int(now[0])
	mn = int(now[1])
	if hr < 10:
		now[0] = "0" + str(hr)
	if mn < 10:
		now[1] = "0" + str(mn)
	return(now[0] + ":" + now[1])

# Get current time minus 1 minute
def getTimeMinus1():
	now = str(datetime.now().time())
	now = now.split(":", 2)
	hr = int(now[0])
	mn = int(now[1])
	if mn == 0:
		mn = 59
		hr = hr-1
	else:
		mn = mn-1
	if hr < 10:
		now[0] = "0" + str(hr)
	if mn < 10:
		now[1] = "0" + str(mn)
	return(now[0] + ":" + now[1])
	
# Set date as today in Firebase
def pushDate(db, hiveId):
	today = str(date.today())
	now = getTime()
	db.child("hives").child(hiveId).child("values").child(now).child("date").set(today)
	
# Set temps in Firebase for current time
def pushTemperature(db, hiveId, outside, inside, base):
	now = getTime()
	db.child("hives").child(hiveId).child("values").child(now).child("temperature").child("outside").set(outside)
	db.child("hives").child(hiveId).child("values").child(now).child("temperature").child("inside").set(inside)
	db.child("hives").child(hiveId).child("values").child(now).child("temperature").child("base").set(base)

# Set humidity in firebase for current time
def pushHumidity(db, hiveId, outside, inside, base):
	now = getTime()
	db.child("hives").child(hiveId).child("values").child(now).child("humidity").child("outside").set(outside)
	db.child("hives").child(hiveId).child("values").child(now).child("humidity").child("inside").set(inside)
	db.child("hives").child(hiveId).child("values").child(now).child("humidity").child("base").set(base)
	
# Set pressue in firebase for current time
def pushPressure(db, hiveId, pressure):
	now = getTime()
	db.child("hives").child(hiveId).child("values").child(now).child("pressure").set(pressure)
	
# Set CO2 in firebase for current time
def pushCo2(db, hiveId, co2):
	now = getTime()
	db.child("hives").child(hiveId).child("values").child(now).child("co2").set(co2)
	
# Set test value in firebase for current time
def pushTest(db, hiveId, test):
	now = getTime()
	db.child("hives").child(hiveId).child("values").child(now).child("test").set(test)
	
# Set ice status
def pushIceStatus(db, hiveId, status):
	db.child("hives").child(hiveId).child("iceStatus").set(status)

# Set heater status
def pushHeaterStatus(db, hiveId, status):
	db.child("hives").child(hiveId).child("heaterStatus").set(status)
	
# Set flapper status	
def pushFlapperStatus(db, hiveId, status):
	db.child("hives").child(hiveId).child("flapperStatus").set(status)
	
# Set fan status
def pushFanStatus(db, hiveId, status):
	db.child("hives").child(hiveId).child("fanStatus").set(status)
	
# Set test LED status on Arduino 1
def pushTestLed1Status(db, hiveId, status):
	return db.child("hives").child(hiveId).child("testLed1").set(status)

# Set test LED status on Arduino 2
def pushTestLed2Status(db, hiveId, status):
	return db.child("hives").child(hiveId).child("testLed2").set(status)
	
# Get the heater status
def getHeaterStatus(db, hiveId):
	return db.child("hives").child(hiveId).child("heaterStatus").get().val()

# Get flapper statues
def getFlapperStatus(db, hiveId):
	return db.child("hives").child(hiveId).child("flapperStatus").get().val()

# Get fan status
def getFanStatus(db, hiveId):
	return db.child("hives").child(hiveId).child("fanStatus").get().val()

# Get test LED status on Arduino 1
def getTestLed1Status(db, hiveId):
	return db.child("hives").child(hiveId).child("testLed1").get().val()

# Get test LED status on Arduino 2
def getTestLed2Status(db, hiveId):
	return db.child("hives").child(hiveId).child("testLed2").get().val()

# Gets a day's worth of environmental data
def getValues(db, hiveId):
	return db.child("hives").child(hiveId).child("values").get().val()
