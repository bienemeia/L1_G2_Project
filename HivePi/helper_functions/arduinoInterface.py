import smbus
import time

bus = smbus.SMBus(1)
address = 0x3C

def ledON():
    bus.write_byte(address,1)

def ledOFF():
    bus.write_byte(address,0)

def read():
    return bus.read_byte_data(address, 2)
