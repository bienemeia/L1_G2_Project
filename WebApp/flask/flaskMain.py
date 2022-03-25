import sys
sys.path.append('../..')
from helper_functions import process
from flask import Flask, Markup, render_template
import time
import sqlite3

app = Flask(__name__)

db = sqlite3.connect("../hiveDB.db")
cursor = process.getDBCursor(db)

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route("/")
def index():
	names = "Meia, Graham and Boshen"
	return render_template('index.html', names=names)
  
@app.route("/bees")
def bees():
	line_labels=labels
	line_values=values
	return render_template('bees.html', max=17000, labels=line_labels, values=line_values)

@app.route("/login")
def login():
	# Login logic here
	return render_template('login.html')

@app.route("/video")
def video():
	# video logic here
	return render_template('video.html')

# @app.route("/background_test")
# def test():
  # print("Hello")
  
if __name__ == "__main__":
	initializing_network()
	app.run(debug=True, host='0.0.0.0')
