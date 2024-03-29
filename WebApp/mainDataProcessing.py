# DESCRIPTION
# This code pulls data from the Firebase DB and processes
# it into the dailyDB every minute. At the end of every day,
# it processes the dailyDB data into Weekly, Monthly, and Yearly 
# averages where:
#   Weekly - Average values over every hour of 1 week (7 days)
#   Monthly - Average values over every 3 hours of ~1 month (31 days)
#   Yearly - Average values every day of the year, for as many years 
#   as hive has been running.
#
# An email alert is sent whenever the temperature or humidity is too high (over threshold).
#
# AUTHOR
# Meia Copeland

import sys
sys.path.append('..')
from helper_functions import firebase, process
import pyrebase
import json
import sqlite3
from datetime import datetime
import time
import smtplib

# Thresholds where values are too high, and a notification email will be sent
TEMP_THRESHOLD = 30
HUMIDITY_THRESHOLD = 80

def main():

    # Set up Firebase authentication
    meia_config = {
        "apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
        "authDomain": "testhive-2bca5.firebaseapp.com",
        "databaseURL": "https://testhive-2bca5-default-rtdb.firebaseio.com/",
        "storageBucket": "testhive-2bca5.appspot.com"
    }
    
    # Setup email data
    gmail_user = "grahamhive@gmail.com"
    gmail_password = "bellFarm"
    destination_email = "meiacopeland@cmail.carleton.ca"
    subjectTemperature = "Hive temperature is high!"
    subjectHumidity = "Hive humidity is high!"
    bodyText =  "Please check the website for more information"

    bodyTemp = "\r\n".join((
                "From: %s" % gmail_user,
                "To: %s" % destination_email,
                "Subject: %s" % subjectTemperature ,
                "",
                bodyText
                ))
    bodyHumid = "\r\n".join((
                "From: %s" % gmail_user,
                "To: %s" % destination_email,
                "Subject: %s" % subjectHumidity ,
                "",
                bodyText
                ))
                
    # Initialize Firebase DB
    hive_firebase = pyrebase.initialize_app(meia_config)
    hive_db = hive_firebase.database()
    dayOfWeek = 1
    dayOfMonth = 1
    updated = False

    while True:
        db = sqlite3.connect("hiveDB.db")
        cursor = process.getDBCursor(db)
        now = firebase.getTime()

        date = firebase.getDate(hive_db, 1, now)
        tempDict = firebase.getTemperature(hive_db, 1, now)
        temperature = [tempDict['base'], tempDict['inside'], tempDict['outside']]
        humidityDict = firebase.getHumidity(hive_db, 1, now)
        humidity = [humidityDict['base'], humidityDict['inside'], humidityDict['outside']]
        pressure = firebase.getPressure(hive_db, 1, now)
        co2 = firebase.getCo2(hive_db, 1, now)
        
        # Send emails if temperature or humidity is too high
        if temperature[0] > TEMP_THRESHOLD or temperature[1] > TEMP_THRESHOLD:
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(gmail_user, destination_email, bodyTemp)
            except:
                print("Something went wrong")
                
        if humidity[0] > HUMIDITY_THRESHOLD or humidity[1] > HUMIDITY_THRESHOLD:
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(gmail_user, destination_email, bodyHumid)
            except:
                print("Something went wrong")       

        # Add values from firebase into local DB
        cursor.execute('''INSERT OR REPLACE INTO dailyDB values (?,?,?,?,?,?,?,?,?,?)''',
                       (now, date, temperature[0], temperature[1], temperature[2], humidity[0], humidity[1], humidity[2], pressure, co2))

        if not updated and now == "23:59":  # Process data at the end of every day
            process.processWeeklyAverages(cursor, dayOfWeek)
            process.processMonthlyAverages(cursor, dayOfMonth)
            process.processYearlyAverages(cursor)
            updated = True
            if dayOfWeek == 7:
                dayOfWeek = 1
            else:
                dayOfWeek += 1
            if dayOfMonth == 31:
                dayOfMonth = 1
            else:
                dayOfMonth += 1
        if now != "23:59":
            updated = False

        db.commit()
        db.close()

        # Loop waits 30 seconds to guarantee that every minute there is an update.
        # 30 seconds handles any delays
        time.sleep(30)


if __name__ == "__main__":
    main()
