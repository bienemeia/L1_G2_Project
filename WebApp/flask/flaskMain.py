# DESCRIPTION
# This code sets up and runs the website on a Flask server.
# When needed, it pulls values from Firebase to display current 
# conditions. It also pulls the data from the local SQLite DB
# to display in a graph.
#
# When buttons are clicked on the tools page, the updateHeater,
# updateFlapper, and updateManual methods push updates to Firebase
# to indicate those mechanisms turning on/off.
#
# AUTHOR
# Meia Copeland

import sys
sys.path.append('../..')
from helper_functions import process, firebase
from flask import Flask, Markup, render_template
import time
import sqlite3
import pyrebase

HIVE_ID = 1

app = Flask(__name__)
# Set up Firebase authentication
meia_config = {
    "apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
    "authDomain": "testhive-2bca5.firebaseapp.com",
    "databaseURL": "https://testhive-2bca5-default-rtdb.firebaseio.com/",
    "storageBucket": "testhive-2bca5.appspot.com"
}
# # Initialize Firebase DB
hive_firebase = pyrebase.initialize_app(meia_config)
hive_db = hive_firebase.database()

@app.route("/")
def index():
    # We can grab the values from firebase using python, and insert them into the html pretty easily
    # Still need to decide how to update regularly
    names = "Meia, Graham and Boshen"
    return render_template('index.html', names=names)


@app.route("/bees")
def bees():
    return render_template('bees.html')


@app.route("/login")
def login():
    # Login logic here
    return render_template('login.html')


@app.route("/video")
def video():
    # video logic here
    return render_template('video.html')


@app.route("/more")
def more():
    return render_template('more.html')


@app.route("/permission")
def permission():
    return render_template('permission.html')


@app.route("/data")
def data():
    # Open connection to database
    db = sqlite3.connect("../hiveDB.db")
    cursor = process.getDBCursor(db)

    # Get current time - 1
    now = firebase.getTimeMinus1()
    
    # Get values from now
    currentValues = cursor.execute(''' SELECT tempBase, tempInside, tempOutside, 
        humidityBase, humidityInside, humidityOutside,
        pressure, co2 from dailyDB WHERE time=? ''', (now,)).fetchone()
    
    # Get current values to display
    tempBase = currentValues[0]
    tempInside = currentValues[1]
    tempOutside = currentValues[2]
    humidityBase = currentValues[3]
    humidityInside = currentValues[4]
    humidityOutside = currentValues[5]
    pressure = currentValues[6]
    co2 = currentValues[7]

    # Get arrays of timeline values for graphing
    dailyValues = process.getDailyArray(cursor)
    weeklyValues = process.getWeeklyArray(cursor)
    monthlyValues = process.getMonthlyArray(cursor)
    yearlyValues = process.getYearlyArray(cursor)
    
    db.commit()
    db.close()

    return render_template('data.html', currentPressure=pressure, currentCo2=co2,
                                                    currentTempBase=tempBase, currentHumidityBase=humidityBase,
                                                    currentTempInside=tempInside, currentHumidityInside=humidityInside,
                                                    currentTempOutside=tempOutside, currentHumidityOutside=humidityOutside,
                                                    dailyLabels=dailyValues["time"], weeklyLabels=weeklyValues["dayHour"],
                                                    monthlyLabels=monthlyValues["dayHour"], yearlyLabels=yearlyValues["date"],
                                                    dailyTempBaseValues=dailyValues["tempBase"], weeklyTempBaseValues=weeklyValues["tempBase"],
                                                    monthlyTempBaseValues=monthlyValues["tempBase"], yearlyTempBaseValues=yearlyValues["tempBase"],
                                                    dailyHumidityBaseValues=dailyValues["humidityBase"], weeklyHumidityBaseValues=weeklyValues["humidityBase"],
                                                    monthlyHumidityBaseValues=monthlyValues["humidityBase"], yearlyHumidityBaseValues=yearlyValues["humidityBase"],
                                                    dailyTempInsideValues=dailyValues["tempInside"], weeklyTempInsideValues=weeklyValues["tempInside"],
                                                    monthlyTempInsideValues=monthlyValues["tempInside"], yearlyTempInsideValues=yearlyValues["tempInside"],
                                                    dailyHumidityInsideValues=dailyValues["humidityInside"], weeklyHumidityInsideValues=weeklyValues["humidityBase"],
                                                    monthlyHumidityInsideValues=monthlyValues["humidityInside"], yearlyHumidityInsideValues=yearlyValues["humidityInside"],
                                                    dailyTempOutsideValues=dailyValues["tempOutside"], weeklyTempOutsideValues=weeklyValues["tempOutside"],
                                                    monthlyTempOutsideValues=monthlyValues["tempOutside"], yearlyTempOutsideValues=yearlyValues["tempOutside"],
                                                    dailyHumidityOutsideValues=dailyValues["humidityOutside"], weeklyHumidityOutsideValues=weeklyValues["humidityOutside"],
                                                    monthlyHumidityOutsideValues=monthlyValues["humidityOutside"], yearlyHumidityOutsideValues=yearlyValues["humidityOutside"],
                                                    dailyPressure=dailyValues["pressure"], weeklyPressure=weeklyValues["pressure"],
                                                    monthlyPressure=monthlyValues["pressure"], yearlyPressure=yearlyValues["pressure"],
                                                    dailyCo2=dailyValues["co2"], weeklyCo2=weeklyValues["co2"],
                                                    monthlyCo2=monthlyValues["co2"], yearlyCo2=yearlyValues["co2"])


@app.route("/tools")
def tools():
    heaterStatus = 0
    flapperStatus = 0
    manualStatus = 0
    
    if firebase.getManualStatus(hive_db, HIVE_ID):
        manualStatus = 1
        
    if firebase.getHeaterStatus(hive_db, HIVE_ID):
        heaterStatus = 1
        
    if firebase.getFlapperStatus(hive_db, HIVE_ID):
        flapperStatus = 1

    return render_template('tools.html', manualStatus=manualStatus, heaterStatus=heaterStatus, flapperStatus=flapperStatus)


@app.route("/updateManual")
def updateManual():
    if firebase.getManualStatus(hive_db, HIVE_ID):
        firebase.pushManualStatus(hive_db, HIVE_ID, False)
    else:
        firebase.pushManualStatus(hive_db, HIVE_ID, True)
    return("nothing")


@app.route("/updateHeater")
def updateHeater():
    if firebase.getManualStatus(hive_db, HIVE_ID):
        if firebase.getHeaterStatus(hive_db, HIVE_ID):
            firebase.pushHeaterStatus(hive_db, HIVE_ID, False)
        else:
            firebase.pushHeaterStatus(hive_db, HIVE_ID, True)
    return("nothing")


@app.route("/updateFlapper")
def updateFlapper():
    if firebase.getManualStatus(hive_db, HIVE_ID):
        if firebase.getFlapperStatus(hive_db, HIVE_ID):
            firebase.pushFlapperStatus(hive_db, HIVE_ID, False)
        else:
            firebase.pushFlapperStatus(hive_db, HIVE_ID, True)
    return("nothing")


if __name__ == "__main__":
    # initializing_network()
    app.run(debug=True, host='0.0.0.0',port=8081)
