import sys
sys.path.append('../..')
from helper_functions import process, firebase
from flask import Flask, Markup, render_template
import time
import sqlite3

app = Flask(__name__)

# Open connection to database
db = sqlite3.connect("../hiveDB.db")
cursor = process.getDBCursor(db)

# Get current time - 1
now = firebase.getTimeMinus1()

# Get values from now
currentValues = cursor.execute(''' SELECT tempBase, tempInside, tempOutside, 
  humidityBase, humidityInside, humidityOutside,
  pressure, co2 from dailyDB WHERE time=? ''', (now,)).fetchone()

tempBase = currentValues[0]
tempInside = currentValues[1]
tempOutside = currentValues[2]
humidityBase = currentValues[3]
humidityInside = currentValues[4]
humidityOutside = currentValues[5]
pressure = currentValues[6]
co2 = currentValues[7]

dailyValues = process.getDailyArray(cursor)
weeklyValues = process.getWeeklyArray(cursor)
monthlyValues = process.getMonthlyArray(cursor)
yearlyValues = process.getYearlyArray(cursor)


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
  return render_template('data.html', currentTemp=tempBase, 
                          currentHumidity=humidityBase, dailyLabels=dailyValues["time"], weeklyLabels=weeklyValues["dayHour"],
                          monthlyLabels=monthlyValues["dayHour"], yearlyLabels=yearlyValues["date"],
                          dailyTempValues=dailyValues["tempBase"], weeklyTempValues=weeklyValues["tempBase"],
                          monthlyTempValues=monthlyValues["tempBase"], yearlyTempValues=yearlyValues["tempBase"],
                          dailyHumidityValues=dailyValues["humidityBase"], weeklyHumidityValues=weeklyValues["humidityBase"],
                          monthlyHumidityValues=monthlyValues["humidityBase"], yearlyHumidityValues=yearlyValues["humidityBase"])


@app.route("/tools")
def tools():
  return render_template('tools.html')


if __name__ == "__main__":
  # initializing_network()
  app.run(debug=True, host='0.0.0.0',port=8081)
