# DESCRIPTION
# This code gets sensor values from 2 Arduinos using a custom library,
# I2CLib, written by another teammate.
# The values are then posted to Firebase.
# In some cases, values are pulled from Firebase to compare,
# and mechanisms on the Arduino are activated.
#
# AUTHOR
# Meia Copeland

import sys
sys.path.append('..')
from helper_functions import firebase
import I2CLib as i2c
import pyrebase
import time


HUMIDITY_THRESHOLD = 70
HEATER_THRESHOLD = -5
ICE_THRESHOLD= 3800


def main():
    # Set up Firebase authentication
    firebaseConfig = {
        "apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
        "authDomain": "testhive-2bca5.firebaseapp.com",
        "databaseURL": "https://testhive-2bca5-default-rtdb.firebaseio.com/",
        "storageBucket": "testhive-2bca5.appspot.com"
    }

    # Initialize Firebase DB
    hive_firebase = pyrebase.initialize_app(firebaseConfig)
    hive_db = hive_firebase.database()
    hive_id = 1

    try:
        i2c.I2CCheck()
    except OSError:
        print("I2C failed on startup")

    while True:

        # Get values from Arduino
        # Order is base, inside, outside
        # If value is None, use same value as last run.
        if i2c.getBaseArduinoTemp() != None and i2c.getHiveArduinoInsideTemp() != None and i2c.getHiveArduinoOutsideTemp() != None:
            temp = [i2c.getBaseArduinoTemp(), i2c.getHiveArduinoInsideTemp(), i2c.getHiveArduinoOutsideTemp()]
        if i2c.getBaseArduinoHumidity() != None and i2c.getHiveArduinoInsideHumidty() != None and i2c.getHiveArduinoOutsideHumidty() != None:
            humidity = [i2c.getBaseArduinoHumidity(), i2c.getHiveArduinoInsideHumidty(), i2c.getHiveArduinoOutsideHumidty()]
        if i2c.getHiveArduinoPressure() != None:
            pressure = i2c.getHiveArduinoPressure()
        # Must check that CO2 sensor is ready, as it requires 20 minutes to 'warm up'
        if i2c.getHiveArduinoCO2Status():
            co2 = i2c.getHiveArduinoCo2()
        else:
            co2 = 0  # default CO2 values when CO2 sensor not ready

        # Get current time
        now = firebase.getTime()

        # Push values to Firebase DB
        firebase.pushTemperature(hive_db, hive_id, now, temp[0], temp[1], temp[2])
        firebase.pushHumidity(hive_db, hive_id, now, humidity[0], humidity[1], humidity[2])
        firebase.pushPressure(hive_db, hive_id, now, pressure)
        firebase.pushCo2(hive_db, hive_id, now, co2)
        firebase.pushDate(hive_db, hive_id, now)
        
        # Only automatically change if manual status is off
        if firebase.getManualStatus(hive_db, hive_id):
            # Get instructions from Firebase DB and send to Arduino
            if firebase.getHeaterStatus(hive_db, hive_id):
                # Check if heater running. If not, turn on
                if not i2c.getBaseArduinoHeaterStatus():
                    i2c.setBaseArduinoHeaterOn()
            else:  # Heater should be set off
                # Check if heater is on. If it is, turn it off
                if i2c.getBaseArduinoHeaterStatus():
                    i2c.setBaseArduinoHeaterOff()

            if firebase.getFlapperStatus(hive_db, hive_id):
                # Check if flapper is open. If not, open
                if not i2c.getHiveArduinoFlapperStatus():
                    i2c.setHiveArduinoFlapperOpen()
            else:  # Flapper should be closed
                # Check if flapper is open. If it is, close it.
                if i2c.getHiveArduinoFlapperStatus():
                    i2c.setHiveArduinoFlapperClosed()

        iceControl(temp, hive_db, hive_id)
        humidityControl(humidity, hive_db, hive_id)

        # Waits 30 seconds to guarantee having values every minute of the day.
        # 30 seconds allows for some overlap in case of delay in execution.
        # If data is already present, it is overwritten rather than duplicated.
        time.sleep(30)


# Checks ice sensors for presence of ice, and activates heater if ice is present.
# The temperature in the base of the hive needs to be low enough, or the heat may
# disturb the bees' hibernation.
def iceControl(temp, db, hive_id):
    # Check for ice
    ice1 = i2c.getBaseArduinoIceSensor1()
    ice2 = i2c.getBaseArduinoIceSensor2()
    ice3 = i2c.getBaseArduinoIceSensor3()
    ice4 = i2c.getBaseArduinoIceSensor4()
    print(ice1)
    print(ice2)
    print(ice3)
    print(ice4)
    if ice1 != None and ice2 != None and ice3 != None and ice4 != None:
        # Ice buildup will cause issues for humidity
        # Ice exists if sum of values is over 2000
        if (ice1 + ice2 + ice3 + ice4) > ICE_THRESHOLD:
            # Change status on firebase
            firebase.pushIceStatus(db, hive_id, True)
            if temp[0] != None and not firebase.getManualStatus(db, hive_id):
                # Turn on heater if temp in base of hive is not too high
                if temp[0] < HEATER_THRESHOLD:
                    firebase.pushHeaterStatus(db, hive_id, True)
                    i2c.setBaseArduinoHeaterOn()
                else:  # Turn off heater if temperature is high
                    firebase.pushHeaterStatus(db, hive_id, False)
                    i2c.setBaseArduinoHeaterOff()
        else:  # If there is no more ice detected, turn off heater
            firebase.pushIceStatus(db, hive_id, False)
            if not firebase.getManualStatus(db, hive_id):
                firebase.pushHeaterStatus(db, hive_id, False)
                i2c.setBaseArduinoHeaterOff()


# Checks humidity inside the hive, and activates the flapper if humidity is too high.
# The humidity outside of the hive must be lower than inside the hive, otherwise venting
# the hive may not be effective.
def humidityControl(humidity, db, hive_id):
    # Only open flap if outside humidity is lower than inside
    if humidity[0] != None and humidity[2] != None and not firebase.getManualStatus(db, hive_id):
        if humidity[0] > HUMIDITY_THRESHOLD:
            if humidity[2] < humidity[0]:
                firebase.pushFlapperStatus(db, hive_id, True)
                i2c.setHiveArduinoFlapperOpen()
            else:  # If humidity outside is greater than inside hive, won't make a difference
                firebase.pushFlapperStatus(db, hive_id, False)
                i2c.setHiveArduinoFlapperClosed()
        else:  # If humidity is below threshold, close flapper
            firebase.pushFlapperStatus(db, hive_id, False)
            i2c.setHiveArduinoFlapperClosed()


if __name__ == "__main__":
    main()
