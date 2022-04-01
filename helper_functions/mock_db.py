from unittest import TestCase
import process
import sqlite3


class MockDB(TestCase):
	
	@classmethod
	def setUp(cls):
		
		# Create database in memory
		try:
			cls.MY_DB = sqlite3.connect(":memory:")
			cls.cursor = process.getDBCursor(cls.MY_DB)
		except:
			print("Error connecting to DB")
		
		# Create tables and enter test values to dailyDB

		process.createDailyDB(cls.cursor)
		process.createWeeklyDB(cls.cursor)
		process.createMonthlyDB(cls.cursor)
		process.createYearlyDB(cls.cursor)
		
		process.testValues(cls.cursor)

	@classmethod
	def tearDown(cls):	
		cls.MY_DB.commit()
		cls.MY_DB.close()
		
		
