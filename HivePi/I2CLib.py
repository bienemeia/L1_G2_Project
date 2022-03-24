import smbus
import time
from gpiozero import LED
blinkLed = LED(4)
bus = smbus.SMBus(1)
address1 = 0x3C
address2 = 0x3d

def getBaseArduinoID():
    try:
        return(bus.read_byte_data(address2, 0)&0x03)
    except OSError:
        print("failed to read i2c")

def getBaseArduinoTemp():
    try:
        temp = bus.read_word_data(address2,1)
        return(temp/10.0)
    except OSError:
        print("failed to read i2c")
        
def getBaseArduinoHumidity():
    try:
        temp = bus.read_word_data(address2,2)
        return(temp/10.0)
    except OSError:
        print("failed to read i2c")
        
def getBaseArduinoHeaterStatus():
    try:
        temp = bus.read_byte_data(address2,3)&0x03
        return(temp)
    except OSError:
        print("failed to read i2c")
        
def setBaseArduinoHeaterOn():
    try:
        temp = bus.read_byte_data(address2,4)
        if temp == 0xF:
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")
        
def setBaseArduinoHeaterOff():
    try:
        temp = bus.read_byte_data(address2,5)
        if temp == 0xF:
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")
        
def getBaseArduinoIceSensor1():
    try:
        temp = bus.read_word_data(address2,6)
        return(temp)
    except OSError:
        print("failed to read i2c")
      
def getBaseArduinoIceSensor2():
    try:
        temp = bus.read_word_data(address2,7)
        return(temp)
    except OSError:
        print("failed to read i2c")

def getBaseArduinoIceSensor3():
    try:
        temp = bus.read_word_data(address2,8)
        return(temp)
    except OSError:
        print("failed to read i2c")
        
def getBaseArduinoIceSensor4():
    try:
        temp = bus.read_word_data(address2,9)
        return(temp)
    except OSError:
        print("failed to read i2c")



def getHiveArduinoID():
    try:
        return(bus.read_byte_data(address1, 0) &0x03)
    except OSError:
        print("failed to read i2c")

def getHiveArduinoInsideTemp():
    try:
        temp = bus.read_word_data(address1,1)
        return(temp/10.0)
    except OSError:
        print("failed to read i2c")
        
def getHiveArduinoInsideHumidty():
    try:
        temp = bus.read_word_data(address1,2)
        return(temp/10.0)
    except OSError:
        print("failed to read i2c")
        
def getHiveArduinoPressure():
    try:
        temp = bus.read_word_data(address1,3)
        return(temp)
    except OSError:
        print("failed to read i2c")
        
def getHiveArduinoCo2():
    try:
        temp = bus.read_word_data(address1,4)
        return(temp)
    except OSError:
        print("failed to read i2c")
        
def getHiveArduinoOutsideTemp():
    try:
        temp = bus.read_word_data(address1,5)
        return(temp/10.0)
    except OSError:
        print("failed to read i2c")
        
def getHiveArduinoOutsideHumidty():
    try:
        temp = bus.read_word_data(address1,6)
        return(temp/10.0)
    except OSError:
        print("failed to read i2c")
        
def setHiveArduinoFlapperOpen():
    try:
        temp = bus.read_byte_data(address1,7)
        if temp == 0xF:
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")
        
def setHiveArduinoFlapperClosed():
    try:
        temp = bus.read_byte_data(address1,8)
        if temp == 0xF:
            return True
        else:
            return False
    except OSError:
        print("failed to read i2c")
        
def getHiveArduinoFlapperStatus():##1=open
    try:
        temp = bus.read_byte_data(address1,9)
        return(temp)
    except OSError:
        print("failed to read i2c")
       
def getHiveArduinoCO2Status():##1=redy
    try:
        temp = bus.read_byte_data(address1,10)
        return(temp)
    except OSError:
        print("failed to read i2c")
        
def I2CCheck():
    blinkLed.off()
    code1 = getHiveArduinoID()
    code2 = getBaseArduinoID()
    
    if code1 == 0x01 and code2 == 0x02:
        return True
        
    else:
        print("I2C check failed node 1 ID: " + str(code1) + " node 2 ID: " + str(code2))
        blinkI2CFaliure()
        return False
  

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
    
def blinkI2CFaliure():
    blinkLed.on()
    time.sleep(0.5)
    blinkLed.off()
    time.sleep(0.5)
    blinkLed.on()
    time.sleep(0.5)
    blinkLed.off()
    time.sleep(0.5)
    blinkLed.on()
    time.sleep(0.5)
    blinkLed.off()
    time.sleep(0.5)
    
    
I2CCheck()
getAllValues()
