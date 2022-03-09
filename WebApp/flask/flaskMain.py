from flask import Flask, render_template
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
  
if __name__ == "__main__":
  initializing_network()
  app.run(debug=True, host='0.0.0.0')
