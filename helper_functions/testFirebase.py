import firebase
import pyrebase
import random
import time
import json
import random
from datetime import date, datetime
import unittest
from collections import OrderedDict

class TestFirebaseHelper(unittest.TestCase):
	# Set up Firebase authentication
	meia_config = {
	"apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
	"authDomain":"testhive-2bca5.firebaseapp.com",
	"databaseURL":"https://testhive-2bca5-default-rtdb.firebaseio.com/",
	"storageBucket":"testhive-2bca5.appspot.com"
	}

	# Initialize Firebase DB
	test_firebase = pyrebase.initialize_app(meia_config)
	test_db = test_firebase.database()
	testId = "test"
	testTime = "00:00"

	# Test that helper functions to push and pull name from Firebase work
	def testHiveName(self):
		expected = "Big Bertha"
		firebase.pushHiveName(self.test_db, self.testId, "Big Bertha")
		actual = firebase.getHiveName(self.test_db, self.testId)
		self.assertEqual(actual, expected)
		
	def testGetTime(self):
		now = str(datetime.now().time())
		now = now.split(":", 2)
		expected = now[0] + ":" + now[1]
		actual = firebase.getTime()
		self.assertEqual(actual, expected)
		
	def testDate(self):
		expected = str(date.today())
		firebase.pushDate(self.test_db, self.testId, self.testTime)
		actual = firebase.getDate(self.test_db, self.testId, self.testTime)
		self.assertEqual(actual, expected)
		
	def testTemperature(self):
		expected = OrderedDict([('base', 5), ('inside', 6), ('outside', 7)])
		firebase.pushTemperature(self.test_db, self.testId, self.testTime, 5, 6, 7)
		actual = firebase.getTemperature(self.test_db, self.testId, self.testTime)
		self.assertEqual(actual, expected)
		
	def testHumidity(self):
		expected = OrderedDict([('base', 30), ('inside', 35), ('outside', 40)])
		firebase.pushHumidity(self.test_db, self.testId, self.testTime, 30, 35, 40)
		actual = firebase.getHumidity(self.test_db, self.testId, self.testTime)
		self.assertEqual(actual, expected)
		
	def testPressure(self):
		expected = 110
		firebase.pushPressure(self.test_db, self.testId, self.testTime, 110)
		actual = firebase.getPressure(self.test_db, self.testId, self.testTime)
		self.assertEqual(actual, expected)
		
	def testCo2(self):
		expected = 300
		firebase.pushCo2(self.test_db, self.testId, self.testTime, 300)
		actual = firebase.getCo2(self.test_db, self.testId, self.testTime)
		self.assertEqual(actual, expected)
		
	def testIceStatus(self):
		expected = False
		firebase.pushIceStatus(self.test_db, self.testId, False)
		actual = firebase.getIceStatus(self.test_db, self.testId)
		self.assertEqual(actual, expected)
		
	def testHeaterStatus(self):
		expected = False
		firebase.pushHeaterStatus(self.test_db, self.testId, False)
		actual = firebase.getHeaterStatus(self.test_db, self.testId)
		self.assertEqual(actual, expected)
		
	def testFlapperStatus(self):
		expected = False
		firebase.pushFlapperStatus(self.test_db, self.testId, False)
		actual = firebase.getFlapperStatus(self.test_db, self.testId)
		self.assertEqual(actual, expected)

	def testFanStatus(self):
		expected = False
		firebase.pushFanStatus(self.test_db, self.testId, False)
		actual = firebase.getFanStatus(self.test_db, self.testId)
		self.assertEqual(actual, expected)
