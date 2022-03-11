from . import firebase
import pyrebase
import json
import sqlite3
import datetime

def getTemperatures(data):
	temps = []
	temps.append(data['temperature']['base'])
	temps.append(data['temperature']['inside'])
	temps.append(data['temperature']['outside'])
	return temps

def getHumidity(data):
	humidity = []
	humidity.append(data['humidity']['base'])
	humidity.append(data['humidity']['inside'])
	humidity.append(data['humidity']['outside'])
	return humidity

def getPressure(data):
	return data['pressure']

def getCo2(data):
	return data['co2']
	
def getTest(data):
	return data['test']
	
def getTimeLessOne(time):
	
