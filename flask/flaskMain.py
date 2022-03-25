from flask import Flask, render_template
from helper_functions import firebase
app = Flask(__name__)

@app.route("/")
def index():
  # We can grab the values from firebase using python, and insert them into the html pretty easily
  # Still need to decide how to update regularly
  names = "Meia, Graham and Boshen"
  return render_template('index.html', names=names)
  
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

@app.route("/more")
def more():
  return render_template('more.html')

@app.route("/permission")
def permission():
  return render_template('permission.html')

@app.route("/data")
def data():
  return render_template('data.html')

@app.route("/tools")
def tools():
  return render_template('tools.html')

if __name__ == "__main__":
  # initializing_network()
  app.run(debug=True, host='0.0.0.0',port=8080)
