import sys
sys.path.append('..')
from helper_functions import process, firebase
from flask import Flask, Markup, render_template
import time
import sqlite3
from datetime import date, datetime, timedelta
import random


def main():
    # Open connection to database
    db = sqlite3.connect("hiveDB.db")
    cursor = process.getDBCursor(db)

    try:
        process.createDailyDB(cursor)
    except:
        print("Already created")
        
    try:
        process.createWeeklyDB(cursor)
    except:
        print("Already created")
        
    try:
        process.createMonthlyDB(cursor)
    except:
        print("Already created")
        
    try:
        process.createYearlyDB(cursor)
    except:
        print("Already created")

    # Get date
    currentDate = datetime(2022, 3, 1).date()
    
    # Get time
    now = "00:00"

    dayOfWeek = 1
    dayOfMonth = 1

    nowNext = getNextMinute(now)
    tempRnd = round(random.randint(-20, 20), 2)
    humidRnd = round(random.randint(10,90), 2)

    while True:
        db = sqlite3.connect("hiveDB.db")
        cursor = process.getDBCursor(db)

        temperature = [tempRnd, tempRnd+1, tempRnd-1]
        humidity = [humidRnd, humidRnd+1, humidRnd-1]
        pressure = round(random.randrange(110,120))
        co2 = round(random.randrange(330,440))

        tempRnd = round(tempRnd + random.randint(0,4)/100, 2)
        humidRnd = round(humidRnd + random.randint(0,4)/100, 2)

        cursor.execute('''INSERT OR REPLACE INTO dailyDB values (?,?,?,?,?,?,?,?,?,?)''',
                       (now, currentDate, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2))
        
        if now == "23:59":  # Process data at the end of every day
            process.processWeeklyAverages(cursor, dayOfWeek)
            process.processMonthlyAverages(cursor, dayOfMonth)
            process.processYearlyAverages(cursor)

            # reset base temp and humidity at end of day
            tempRnd = round(random.randint(-20, 20), 2)
            humidRnd = round(random.randint(10,60), 2)
            updated = True
            currentDate = getNextDay(currentDate)

            if dayOfWeek == 7:
                dayOfWeek = 1
            else:
                dayOfWeek += 1

            if dayOfMonth == 31:
                dayOfMonth = 1
            else:
                dayOfMonth += 1

        db.commit()
        db.close()


        now = getNextMinute(now)


def getNextDay(current):
    nextDay = current + timedelta(days=1)
    return nextDay

def getNextMinute(current):
    now = current.split(":", 2)
    hr = int(now[0])
    mn = int(now[1])

    if mn == 59:
        mn = 0
        if hr == 23:
            hr = 0
        else:
            hr = hr + 1
    else:
        mn += 1


    if hr < 10:
        now[0] = "0" + str(hr)
    else:
        now[0] = str(hr)
    if mn < 10:
        now[1] = "0" + str(mn)
    else:
        now[1] = str(mn)
    return(now[0] + ":" + now[1])

if __name__ == "__main__":
    main()
