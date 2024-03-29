# DESCRIPTION
# Contains functions useful for processing data in the local SQLite DB
# as well as pushing/pulling data from teh SQLite DB.
#
# AUTHOR
# Meia Copeland

import sqlite3
import datetime
import random


# Process daily data into weekly data, where averages are taken every 1 hour
def processWeeklyAverages(cursor, dayOfWeek):
    # Can get time and date from beginning of day,
    # since doing processing at end of day
    try:
        date = cursor.execute(''' SELECT date FROM dailyDB ''').fetchone()[0]
    except sqlite3.Error as er:
        print("SQLite error: " + er)

    # Loop through every hour and minute, averaging all values over 1 hour
    for hour in range(24):
        sumTempBase = 0
        sumTempInside = 0
        sumTempOutside = 0
        sumHumidBase = 0
        sumHumidInside = 0
        sumHumidOutside = 0
        sumCo2 = 0
        sumPressure = 0
        for minute in range(60):
            # Get tempBase at time
            try:
                values = cursor.execute(''' SELECT tempBase, tempInside, tempOutside,
                                        humidityBase, humidityInside,
                                        humidityOutside, co2,
                                        pressure FROM dailyDB WHERE time=? ''',
                                        (getFormattedTime(minute + (hour * 60)),)).fetchone()
            except sqlite3.Error as er:
                print("SQLite error: " + er)

            # Sum all values within 1 hour
            sumTempBase += values[0]
            sumTempInside += values[1]
            sumTempOutside += values[2]
            sumHumidBase += values[3]
            sumHumidInside += values[4]
            sumHumidOutside += values[5]
            sumCo2 += values[6]
            sumPressure += values[7]

        # Calculate averages over 3 hours
        avgTempBase = round(sumTempBase / 60, 2)
        avgTempInside = round(sumTempInside / 60, 2)
        avgTempOutside = round(sumTempOutside / 60, 2)
        avgHumidBase = round(sumHumidBase / 60)
        avgHumidInside = round(sumHumidInside / 60)
        avgHumidOutside = round(sumHumidOutside / 60)
        avgCo2 = round(sumCo2 / 60, 2)
        avgPressure = round(sumPressure / 60, 2)

        # Get dayHour string in format 'dayOfWeek-hour'
        dayHour = str(dayOfWeek) + "-" + str(hour)

        # Post values to DB
        try:
            cursor.execute(''' INSERT OR REPLACE INTO weeklyDB values (?,?,?,?,?,?,?,?,?,?,?)''',
                           (dayHour, hour, date,
                            avgTempBase, avgTempInside, avgTempOutside,
                            avgHumidBase, avgHumidInside, avgHumidOutside,
                            avgPressure, avgCo2))
        except sqlite3.Error as er:
            print("SQLite error: " + er)


# Process daily data into monthly data, where averages are taken every 3 hours
def processMonthlyAverages(cursor, dayOfMonth):
    # Can get time and date from beginning of day, since doing processing at end of day
    try:
        date = cursor.execute(''' SELECT date FROM dailyDB ''').fetchone()[0]
    except sqlite3.Error as er:
        print("SQLite error: " + er)

    # Loop through every hour and minute, averaging all values over 1 hour

    for hour in range(0, 24, 3):
        sumTempBase = 0
        sumTempInside = 0
        sumTempOutside = 0
        sumHumidBase = 0
        sumHumidInside = 0
        sumHumidOutside = 0
        sumCo2 = 0
        sumPressure = 0
        for minute in range(180):
            # Get tempBase at time
            try:
                values = cursor.execute(''' SELECT tempBase, tempInside, tempOutside, humidityBase, humidityInside,
                                        humidityOutside, co2,
                                        pressure FROM dailyDB WHERE time=? ''',
                                        (getFormattedTime(minute + (hour * 60)),)).fetchone()
            except sqlite3.Error as er:
                print("SQLite error: " + er)

            # Sum all values within 1 hour
            sumTempBase += values[0]
            sumTempInside += values[1]
            sumTempOutside += values[2]
            sumHumidBase += values[3]
            sumHumidInside += values[4]
            sumHumidOutside += values[5]
            sumCo2 += values[6]
            sumPressure += values[7]

        # Calculate averages over 1 hour
        avgTempBase = round(sumTempBase / 180, 2)
        avgTempInside = round(sumTempInside / 180, 2)
        avgTempOutside = round(sumTempOutside / 180, 2)
        avgHumidBase = round(sumHumidBase / 180, 2)
        avgHumidInside = round(sumHumidInside / 180, 2)
        avgHumidOutside = round(sumHumidOutside / 180, 2)
        avgCo2 = round(sumCo2 / 180, 2)
        avgPressure = round(sumPressure / 180, 2)

        # Get dayHour string in format 'dayOfWeek-hour'
        dayHour = str(dayOfMonth) + "-" + str(hour)

        # Post values to DB
        try:
            cursor.execute(''' INSERT OR REPLACE INTO monthlyDB values (?,?,?,?,?,?,?,?,?,?,?)''',
                           (dayHour, hour, date,
                            avgTempBase, avgTempInside, avgTempOutside,
                            avgHumidBase, avgHumidInside, avgHumidOutside,
                            avgPressure, avgCo2))
        except sqlite3.Error as er:
            print("SQLite error: " + er)


# Process daily data into yearly data, where averages are taken every day
def processYearlyAverages(cursor):
    # Can get time and date from beginning of day, since doing processing at end of day
    try:
        date = cursor.execute(''' SELECT date FROM dailyDB ''').fetchone()[0]
    except sqlite3.Error as er:
        print("SQLite error: " + er)

    # Loop through every hour and minute, averaging all values over 1 hour
    sumTempBase = 0
    sumTempInside = 0
    sumTempOutside = 0
    sumHumidBase = 0
    sumHumidInside = 0
    sumHumidOutside = 0
    sumCo2 = 0
    sumPressure = 0
    for hour in range(0, 24, 3):
        for minute in range(180):
            # Get tempBase at time
            try:
                values = cursor.execute(''' SELECT tempBase, tempInside, tempOutside, humidityBase, humidityInside,
                                        humidityOutside, co2, pressure FROM dailyDB WHERE time=? ''',
                                        (getFormattedTime(minute + (hour * 60)),)).fetchone()
            except sqlite3.Error as er:
                print("SQLite error: " + er)

            # Sum all values within 1 hour
            sumTempBase += values[0]
            sumTempInside += values[1]
            sumTempOutside += values[2]
            sumHumidBase += values[3]
            sumHumidInside += values[4]
            sumHumidOutside += values[5]
            sumCo2 += values[6]
            sumPressure += values[7]

    # Calculate averages over 1 day
    avgTempBase = round(sumTempBase / 1440, 2)
    avgTempInside = round(sumTempInside / 1440, 2)
    avgTempOutside = round(sumTempOutside / 1440, 2)
    avgHumidBase = round(sumHumidBase / 1440, 2)
    avgHumidInside = round(sumHumidInside / 1440, 2)
    avgHumidOutside = round(sumHumidOutside / 1440, 2)
    avgCo2 = round(sumCo2 / 1440, 2)
    avgPressure = round(sumPressure / 1440, 2)

    # Post values to DB
    try:
        cursor.execute(''' INSERT OR REPLACE INTO yearlyDB values (?,?,?,?,?,?,?,?,?)''',
                       (date,
                        avgTempBase, avgTempInside, avgTempOutside,
                        avgHumidBase, avgHumidInside, avgHumidOutside,
                        avgPressure, avgCo2))
    except sqlite3.Error as er:
        print("SQLite error: " + er)


# Get array of daily data
def getDailyArray(cursor):
    values = {'time': [], 'date': [], 'tempBase': [], 'tempInside': [], 'tempOutside': [],
              'humidityBase': [], 'humidityInside': [], 'humidityOutside': [],
              'pressure': [], 'co2': []}
    try:
        tempBase = cursor.execute('''SELECT time, date, tempBase, tempInside, tempOutside,
                                    humidityBase, humidityInside, humidityOutside,
                                    pressure, co2 FROM dailyDB ORDER BY date, time''').fetchall()
    except sqlite3.Error as er:
        print("SQLite error: " + er)

    for row in tempBase:
        values["time"].append(row[0])
        values["date"].append(row[1])
        values["tempBase"].append(row[2])
        values["tempInside"].append(row[3])
        values["tempOutside"].append(row[4])
        values["humidityBase"].append(row[5])
        values["humidityInside"].append(row[6])
        values["humidityOutside"].append(row[7])
        values["pressure"].append(row[8])
        values["co2"].append(row[9])

    return values

# Get array of weekly data
def getWeeklyArray(cursor):
    values = {'dayHour': [], 'hour': [], 'date': [], 'tempBase': [], 'tempInside': [], 'tempOutside': [],
              'humidityBase': [], 'humidityInside': [], 'humidityOutside': [],
              'pressure': [], 'co2': []}
    try:
        tempBase = cursor.execute('''SELECT dayHour, hour, date, tempBase, tempInside, tempOutside,
                                    humidityBase, humidityInside, humidityOutside,
                                    pressure, co2 FROM weeklyDB ORDER BY date, dayHour''').fetchall()
    except sqlite3.Error as er:
        print("SQLite error: " + er)

    for row in tempBase:
        values["dayHour"].append(row[0])
        values["hour"].append(row[1])
        values["date"].append(row[2])
        values["tempBase"].append(row[3])
        values["tempInside"].append(row[4])
        values["tempOutside"].append(row[5])
        values["humidityBase"].append(row[6])
        values["humidityInside"].append(row[7])
        values["humidityOutside"].append(row[8])
        values["pressure"].append(row[9])
        values["co2"].append(row[10])

    return values


# Get array of monthly data
def getMonthlyArray(cursor):
    values = {'dayHour': [], 'hour': [], 'date': [], 'tempBase': [], 'tempInside': [], 'tempOutside': [],
              'humidityBase': [], 'humidityInside': [], 'humidityOutside': [],
              'pressure': [], 'co2': []}
    try:
        tempBase = cursor.execute('''SELECT dayHour, hour, date, tempBase, tempInside, tempOutside,
                                    humidityBase, humidityInside, humidityOutside,
                                    pressure, co2 FROM monthlyDB ORDER BY date, dayHour''').fetchall()
    except sqlite3.Error as er:
        print("SQLite error: " + er)

    for row in tempBase:
        values["dayHour"].append(row[0])
        values["hour"].append(row[1])
        values["date"].append(row[2])
        values["tempBase"].append(row[3])
        values["tempInside"].append(row[4])
        values["tempOutside"].append(row[5])
        values["humidityBase"].append(row[6])
        values["humidityInside"].append(row[7])
        values["humidityOutside"].append(row[8])
        values["pressure"].append(row[9])
        values["co2"].append(row[10])

    return values


# Get array of yearly data
def getYearlyArray(cursor):
    values = {'date': [], 'tempBase': [], 'tempInside': [], 'tempOutside': [],
              'humidityBase': [], 'humidityInside': [], 'humidityOutside': [],
              'pressure': [], 'co2': []}
    try:
        tempBase = cursor.execute('''SELECT date, tempBase, tempInside, tempOutside,
                                    humidityBase, humidityInside, humidityOutside,
                                    pressure, co2 FROM yearlyDB ORDER BY date''').fetchall()
    except sqlite3.Error as er:
        print("SQLite error: " + er)

    for row in tempBase:
        values["date"].append(row[0])
        values["tempBase"].append(row[1])
        values["tempInside"].append(row[2])
        values["tempOutside"].append(row[3])
        values["humidityBase"].append(row[4])
        values["humidityInside"].append(row[5])
        values["humidityOutside"].append(row[6])
        values["pressure"].append(row[7])
        values["co2"].append(row[8])

    return values


# Get DB cursor for given db
def getDBCursor(db):
    db.row_factory = sqlite3.Row
    return db.cursor()


# The following methods are for setting up the system with DBs

# Method for creating daily DB
# Only to be used if DB doesn't exist on system
def createDailyDB(cursor):
    try:
        cursor.execute('''CREATE TABLE dailyDB
            (time TEXT, date TEXT,
            tempBase REAL, tempInside REAL, tempOutside REAL,
            humidityBase REAL, humidityInside REAL, humidityOutside REAL,
            pressure REAL, co2 REAL,
            UNIQUE(time))''')
    except sqlite3.Error as er:
        print("SQLite error: " + er)


# Method for creating weekly DB
# Only to be used if DB doesn't exist on system
def createWeeklyDB(cursor):
    try:
        cursor.execute('''CREATE TABLE weeklyDB
            (dayHour TEXT, hour INT, date TEXT,
            tempBase REAL, tempInside REAL, tempOutside REAL,
            humidityBase REAL, humidityInside REAL, humidityOutside REAL,
            pressure REAL, co2 REAL,
            UNIQUE(dayHour))''')
    except sqlite3.Error as er:
        print("SQLite error: " + er)


# Method for creating monthly DB
# Only to be used if DB doesn't exist on system
def createMonthlyDB(cursor):
    try:
        cursor.execute('''CREATE TABLE monthlyDB
            (dayHour TEXT, hour INT, date TEXT,
            tempBase REAL, tempInside REAL, tempOutside REAL,
            humidityBase REAL, humidityInside REAL, humidityOutside REAL,
            pressure REAL, co2 REAL,
            UNIQUE(dayHour))''')
    except sqlite3.Error as er:
        print("SQLite error: " + er)


# Method for creating yearly DB
# Only to be used if DB doesn't exist on system
def createYearlyDB(cursor):
    try:
        cursor.execute('''CREATE TABLE yearlyDB
            (date TEXT,
            tempBase REAL, tempInside REAL, tempOutside REAL,
            humidityBase REAL, humidityInside REAL, humidityOutside REAL,
            pressure REAL, co2 REAL,
            UNIQUE(date))''')
    except sqlite3.Error as er:
        print("SQLite error: " + er)


# Method to format time given an integer
def getFormattedTime(num):
    hr = num // 60
    mn = num % 60
    time = [hr, mn]
    if hr < 10:
        time[0] = "0" + str(hr)
    if mn < 10:
        time[1] = "0" + str(mn)
    return(str(time[0]) + ":" + str(time[1]))

