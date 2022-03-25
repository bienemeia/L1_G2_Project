from mock_db import MockDB
import process
import sqlite3
import random
import time
import json
import random
from datetime import date, datetime
import unittest
from unittest.mock import Mock
from collections import OrderedDict

class TestProcessHelper(MockDB):
	
	def testProcessWeekly(self):
		process.processWeeklyAverages(self.cursor, 1)
		
	def testProcessMonthly(self):
		process.processMonthlyAverages(self.cursor, 1)
		
	def testProcessYearly(self):
		process.processYearlyAverages(self.cursor, 1)
