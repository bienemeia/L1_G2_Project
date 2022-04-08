from datetime import date, datetime


# Set the hive name
def pushHiveName(db, hiveId, name):
    db.child("hives").child(hiveId).child("name").set(name)


# Get current time in form HH:MM (24 hour)
def getTime():
    now = str(datetime.now().time())
    now = now.split(":")
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
        hr = hr - 1
    else:
        mn = mn - 1

    if hr < 10:
        now[0] = "0" + str(hr)
    else:
        now[0] = str(hr)

    if mn < 10:
        now[1] = "0" + str(mn)
    else:
        now[1] = str(mn)
        
    return(now[0] + ":" + now[1])


# Set date as today in Firebase
def pushDate(db, hiveId, time):
    today = str(date.today())
    db.child("hives").child(hiveId).child("values").child(time).child("date").set(today)


# Set temps in Firebase for current time
def pushTemperature(db, hiveId, time, base, inside, outside):
    db.child("hives").child(hiveId).child("values").child(time).child("temperature").child("outside").set(outside)
    db.child("hives").child(hiveId).child("values").child(time).child("temperature").child("inside").set(inside)
    db.child("hives").child(hiveId).child("values").child(time).child("temperature").child("base").set(base)


# Set humidity in firebase for current time
def pushHumidity(db, hiveId, time, base, inside, outside):
    db.child("hives").child(hiveId).child("values").child(time).child("humidity").child("outside").set(outside)
    db.child("hives").child(hiveId).child("values").child(time).child("humidity").child("inside").set(inside)
    db.child("hives").child(hiveId).child("values").child(time).child("humidity").child("base").set(base)


# Set pressue in firebase for current time
def pushPressure(db, hiveId, time, pressure):
    db.child("hives").child(hiveId).child("values").child(time).child("pressure").set(pressure)


# Set CO2 in firebase for current time
def pushCo2(db, hiveId, time, co2):
    db.child("hives").child(hiveId).child("values").child(time).child("co2").set(co2)


# Set test value in firebase for current time
def pushTest(db, hiveId, time, test):
    db.child("hives").child(hiveId).child("values").child(time).child("test").set(test)


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


# Set manual status
def pushManualStatus(db, hiveId, status):
    db.child("hives").child(hiveId).child("manualStatus").set(status)


# Set test LED status on Arduino 1
def pushTestLed1Status(db, hiveId, status):
    return db.child("hives").child(hiveId).child("testLed1").set(status)


# Set test LED status on Arduino 2
def pushTestLed2Status(db, hiveId, status):
    return db.child("hives").child(hiveId).child("testLed2").set(status)
    

# Get the hive name
def getHiveName(db, hiveId):
    return db.child("hives").child(hiveId).child("name").get().val()


# Get date for specified time slot
def getDate(db, hiveId, time):
    return db.child("hives").child(hiveId).child("values").child(time).child("date").get().val()


# Get temperatures for specified time slot
def getTemperature(db, hiveId, time):
    return db.child("hives").child(hiveId).child("values").child(time).child("temperature").get().val()


# Get humidities for specified time slot
def getHumidity(db, hiveId, time):
    return db.child("hives").child(hiveId).child("values").child(time).child("humidity").get().val()


# Get pressure for specifiec time slot
def getPressure(db, hiveId, time):
    return db.child("hives").child(hiveId).child("values").child(time).child("pressure").get().val()


# Get pressure for specifiec time slot
def getCo2(db, hiveId, time):
    return db.child("hives").child(hiveId).child("values").child(time).child("co2").get().val()


# Get the ice status
def getIceStatus(db, hiveId):
    return db.child("hives").child(hiveId).child("iceStatus").get().val()


# Get the heater status
def getHeaterStatus(db, hiveId):
    return db.child("hives").child(hiveId).child("heaterStatus").get().val()


# Get flapper statues
def getFlapperStatus(db, hiveId):
    return db.child("hives").child(hiveId).child("flapperStatus").get().val()


# Get fan status
def getFanStatus(db, hiveId):
    return db.child("hives").child(hiveId).child("fanStatus").get().val()


# Get manual status
def getManualStatus(db, hiveId):
    return db.child("hives").child(hiveId).child("manualStatus").get().val()


# Get test LED status on Arduino 1
def getTestLed1Status(db, hiveId):
    return db.child("hives").child(hiveId).child("testLed1").get().val()


# Get test LED status on Arduino 2
def getTestLed2Status(db, hiveId):
    return db.child("hives").child(hiveId).child("testLed2").get().val()
    
# Get the heater status
def getSystemStatus(db, hiveId, system):
    return db.child("hives").child(hiveId).child(system).get().val()


# Gets a day's worth of environmental data
def getValues(db, hiveId):
    return db.child("hives").child(hiveId).child("values").get().val()
