from flask import Flask, render_template
from helper_functions import firebase, process
import pyrebase
app = Flask(__name__)

# Set up Firebase authentication
meia_config = {
"apiKey": "AIzaSyBVpD3QAJ7NQsmobIABC95vOX8-e-aZQX0",
"authDomain":"testhive-2bca5.firebaseapp.com",
"databaseURL":"https://testhive-2bca5-default-rtdb.firebaseio.com/",
"storageBucket":"testhive-2bca5.appspot.com"
}

# Initialize Firebase DB
hive_firebase = pyrebase.initialize_app(meia_config)
hive_db = hive_firebase.database()


@app.route("/")
def index():
  # We can grab the values from firebase using python, and insert them into the html pretty easily
  # Still need to decide how to update regularly
  names = "Meia, Graham and Boshen"
  #time = "8:45"
  time = firebase.getTimeMinus1()
  data = firebase.getValues(hive_db, 1)
  test = process.getTest(data[time])
  #test = 46
  return render_template('index.html', names=names, test=test, time=time)
  
@app.route("/bees")
def bees():
  return render_template('bees.html')

@app.route("/login")
def login():
  # Login logic here
  return render_template('login.html')

@app.route("/video")
def video():
  # video logic here
  return render_template('video.html')

@app.route("/background_test")
def test():
  print("Hello")
  if firebase.getTestLed1Status(hive_db, 1):
    firebase.pushTestLed1Status(hive_db, 1, False)
  else:
    firebase.pushTestLed1Status(hive_db, 1, True)
  return("nothing")
  
if __name__ == "__main__":
  initializing_network()
  app.run(debug=True, host='0.0.0.0')
