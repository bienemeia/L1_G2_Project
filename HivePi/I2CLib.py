import smbus
import time
from gpiozero import LED
blinkLed = LED(4)
bus = smbus.SMBus(1)
address1 = 0x3C
address2 = 0x3d


# This method gets the Id of the arduino at address 0x3d.
# The last 3 bit of the byte are masked out to correct for the 128 bit being set by the arduino.
def getBaseArduinoID():
    try:
        return(bus.read_byte_data(address2, 0) & 0x03)
    except OSError:
        print("failed to read i2c")


# This method gets the temperature in C at the base board of the hive.
# It is /10.00 to convert the int from the byte array to a float.
def getBaseArduinoTemp():
    try:
        return((bus.read_word_data(address2, 1)) / 10.0)
    except OSError:
        print("failed to read i2c")


# This method get the humidity in r% at the base board of the hive.
# It is /10.00 to convert the int from the byte array to a float.
def getBaseArduinoHumidity():
    try:
        return((bus.read_word_data(address2, 2)) / 10.0)
    except OSError:
        print("failed to read i2c")


# This method gets the status of the heater. This function returns True if the heater is on.
# The last 3 bit of the byte are masked out to correct for the 128 bit being set by the arduino.
def getBaseArduinoHeaterStatus():
    try:
        if (bus.read_byte_data(address2, 3) & 0x03) == 1:
            return(True)
        else:
            return(False)
    except OSError:
        print("failed to read i2c")


# This method turns on the heater.
# If there was a write error this function returns false.
def setBaseArduinoHeaterOn():
    try:
        if bus.read_byte_data(address2, 4) == 0xF:  # all 1s
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")


# This method turns off the heater.
# If there was a write error this function returns false.
def setBaseArduinoHeaterOff():
    try:
        if bus.read_byte_data(address2, 5) == 0xF:
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")


# This method gets the amount of light detected by the first Ice detector.
# Higher means more light.
def getBaseArduinoIceSensor1():
    try:
        return((bus.read_word_data(address2, 6)))
    except OSError:
        print("failed to read i2c")


# This method gets the amount of light detected by the second Ice detector.
# Higher means more light.
def getBaseArduinoIceSensor2():
    try:
        return(bus.read_word_data(address2, 7))
    except OSError:
        print("failed to read i2c")


# This method gets the amount of light detected by the third Ice detector.
# Higher means more light.
def getBaseArduinoIceSensor3():
    try:
        return(bus.read_word_data(address2, 8))
    except OSError:
        print("failed to read i2c")


# This method gets the amount of light detected by the forth Ice detector.
# Higher means more light.
def getBaseArduinoIceSensor4():
    try:
        return(bus.read_word_data(address2, 9))
    except OSError:
        print("failed to read i2c")


''' Hive arduino below '''


# This method gets the Id of the arduino at address 0x3c.
# The last 3 bit of the byte are masked out to correct for the 128 bit being set by the arduino.
def getHiveArduinoID():
    try:
        return(bus.read_byte_data(address1, 0) & 0x03)
    except OSError:
        print("failed to read i2c")


# This method gets the temperature in C in the seasonal inner cover of the hive.
# It is /10.00 to convert the int from the byte array to a float.
def getHiveArduinoInsideTemp():
    try:
        return((bus.read_word_data(address1, 1)) / 10.0)
    except OSError:
        print("failed to read i2c")


# This method gets the humidty in r% in the seasonal inner cover of the hive.
# It is /10.00 to convert the int from the byte array to a float.
def getHiveArduinoInsideHumidty():
    try:
        return((bus.read_word_data(address1, 2)) / 10.0)
    except OSError:
        print("failed to read i2c")


# This method gets the pressure in hPa in the seasonal inner cover of the hive.
# It is /1.0 to convert the int from the byte array to a float.
def getHiveArduinoPressure():
    try:
        return((bus.read_word_data(address1, 3)) / 1.00)
    except OSError:
        print("failed to read i2c")


# This method gets the amount of co2 in ohms detected by the hive.
def getHiveArduinoCo2():
    try:
        return(bus.read_word_data(address1, 4))
    except OSError:
        print("failed to read i2c")


# This method gets the temperature in C outside the hive.
# It is /10.00 to convert the int from the byte array to a float.
def getHiveArduinoOutsideTemp():
    try:
        return((bus.read_word_data(address1, 5)) / 10.0)
    except OSError:
        print("failed to read i2c")


# This method gets the humidty in r% outside the hive.
# It is /10.00 to convert the int from the byte array to a float.
def getHiveArduinoOutsideHumidty():
    try:
        temp = bus.read_word_data(address1, 6)
        return(temp / 10.0)
    except OSError:
        print("failed to read i2c")


# This method opens the flapper. If a write error occurs this function return false.
def setHiveArduinoFlapperOpen():
    try:
        if bus.read_byte_data(address1, 7) == 0xF:
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")


# This method closes the flapper. If a write error occurs this function return false.
def setHiveArduinoFlapperClosed():
    try:
        if bus.read_byte_data(address1, 8) == 0xF:
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")


# This method gets if the flapper is open or closed. This method will return true if the flapper is open.
# This method ueses the 0x3 bit mask to correct for the 128th bit being set.
def getHiveArduinoFlapperStatus():
    try:
        if(bus.read_byte_data(address1, 9) & 0x3 == 1):
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")


# This method gets if the CO2 is ready to be mesured. True means it is ready to go.
def getHiveArduinoCO2Status():  # 1 = ready
    try:
        if(bus.read_byte_data(address1, 10) & 0x3 == 1):
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")


# This method test if communication can be established.
def I2CCheck():
    blinkLed.off()
    ID1 = getHiveArduinoID()
    ID2 = getBaseArduinoID()

    if ID1 == 0x01 and ID2 == 0x02:
        return True

    else:
        print("I2C check failed node 1 ID: " + str(ID1) + " node 2 ID: " + str(ID2))
        blinkI2CFaliure()
        return False


# This method gets and prints every pices of information atanable from the arduino.
def getAllValues():
    print("node 1 ID: " + str(getHiveArduinoID()))
    print("node 1 inside temp in C: " + str(getHiveArduinoInsideTemp()))
    print("node 1 inside humidity in r%: " + str(getHiveArduinoInsideHumidty()))
    print("node 1 Pressure in hpa: " + str(getHiveArduinoPressure()))
    print("node 1 co2 in ohms: " + str(getHiveArduinoCo2()))
    print("node 1 outside temp in C: " + str(getHiveArduinoOutsideTemp()))
    print("node 1 outside humidity in r%: " + str(getHiveArduinoOutsideHumidty()))
    print("node 1 flapper status: " + str(getHiveArduinoFlapperStatus()))
    print("node 1 co2 status: " + str(getHiveArduinoCO2Status()))

    print("\n")
    print("opening flapper will idle for 10s")
    setHiveArduinoFlapperOpen()
    print("node 1 flapper status: " + str(getHiveArduinoFlapperStatus()))
    time.sleep(10)
    print("closeing flapper")
    setHiveArduinoFlapperClosed()

    print("\n")
    print("node 2 ID: " + str(getBaseArduinoID()))
    print("node 2 temp in C: " + str(getBaseArduinoTemp()))
    print("node 2 humidity r%: " + str(getBaseArduinoHumidity()))
    print("node 2 heater status befor functions: " + str(getBaseArduinoHeaterStatus()))
    print("node 2 turn on heater call: " + str(setBaseArduinoHeaterOn()))
    print("node 2 heater status after turn on call: " + str(getBaseArduinoHeaterStatus()))
    print("node 2 turn off heater call: " + str(setBaseArduinoHeaterOff()))
    print("node 2 heater status after turn off call: " + str(getBaseArduinoHeaterStatus()))

    print("Ice Sensor 1: " + str(getBaseArduinoIceSensor1()))
    print("Ice Sensor 2: " + str(getBaseArduinoIceSensor2()))
    print("Ice Sensor 3: " + str(getBaseArduinoIceSensor3()))
    print("Ice Sensor 4: " + str(getBaseArduinoIceSensor4()))


# This method blinks a LED to show a I2C fault.
def blinkI2CFaliure():
    for x in range(3):
        blinkLed.on()
        time.sleep(0.5)
        blinkLed.off()
        time.sleep(0.5)
    time.sleep(2)
