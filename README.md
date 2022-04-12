## SYSC 3010 Project: Honey, I'm a Smart Home!
### Group number: L1-G2
### Date: April 12, 2022
### TA: Victoria Ajila
### Group members:
#### Meia Copeland
#### Graham C. Bell
#### Boshen Zhang

---

The Honey, I'm a Smart Home! is a modular smart beehive system that allows beekeepers to keep track of temperature, humidity, pressure, and CO2 levels inside the hive. Beehives are vulnerable in the winter, due to heavy snowfalls and low temperatures. Snow can block the ventilation in the lower section of the hive, causing the humidity to increase inside and put the bees at risk of freezing. When the Honey, I'm a Smart Home! detects the presence of ice or snow using photo-detectors, it activates a heating system that will melt the blockage. Alternatively, if there is no ice or snow and the humidity it high, a ventilation flap will automatically open until humidity reaches an acceptable level. A website is also provided, which displays the data from the hive sensors, and provides the beekeeper with a manual override for the automatic systems.

# Installation instructions

## Assembling Hardware

### Wiring

#### BaseBoard Arduino Subsystem

This subsystem is the bottom board temperature measurement, Ice Sensor and Heater. The wiring diagram and setup diagram is available for this subsystem. 
The [wiring diagram is available here ](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%202%20System_Skeam.png) and the 
[setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%202%20System.png)
 
#### Hive Top Arduino Subsystem

This subsystem is the hive top temperature measurement, outside temperature measurement and flapper. The wiring diagram and setup diagram is available for this subsystem. 
The [wiring diagram is available here ](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%201%20System_schem.png) and the 
[setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%201%20System.png)

#### BackBone Communication and Hive Top RPI 
This subsystem is the main communication system for the hive top pi and the Arduino subsystem. 
The [wiring diagram is available here ](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Seasonal%20Innercove%20and%20BaseBoard%20Communication%20system_schem.png) and the [setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Seasonal%20Innercove%20and%20BaseBoard%20Communication%20system..png)

#### Web Server Pi
This Subsystem is responsible for hosting the website. The [setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Raspberry%20Pi%201.png)

## Installing software

### Arduinos

- Before installing data on the Arduinos, you will need to install the Arduino IDE. Instructions can be found here: https://www.arduino.cc/en/main/howto
- Clone the Git repository locally.

#### Base Board Arduino
- Open the IDE and import the C++ and Header files from the [Base_Board_Arduino folder](/Hive_Hardware_Subsystem/Final_Product_Code/Base_Board_Arduino)
- Install the [softI2C libary.](https://www.arduino.cc/reference/en/libraries/softwire/)
- Install the necessary board drivers.
- Connect the Base Board Arduino to your computer.
- Use the Arduino IDE to install the code to the Arduino.
- Unplug the Arduino and fix to Base Board of hive.

#### Inner Seasonal Cover Arduino
- Open the IDE and import the C++ and Header files, Soft_DFRobot_SHT3x.cpp and Soft_DFRobot_SHT3x.h, from the [Seasonal_Cover_Arduino folder](/Hive_Hardware_Subsystem/Final_Product_Code/Seasonal_Cover_Arduino).
- Install the [softI2C libary.](https://www.arduino.cc/reference/en/libraries/softwire/)
- Install the necessary board drivers.
- Connect the Inner Seasonal Cover Arduino to your computer.
- Use the Arduino IDE to install the code to the Arduino.
- Unplug the Arduino and fix to Inner Seasonal Cover of hive.

### Raspberry Pis
#### Create Firebase account
- Go to https://firebase.google.com/
- Log in/Create account.
- Add project.
- Beside the 'Project Overview' heading on the left side of the page, click the gear icon, then 'Project Settings'.
- Scroll down to 'Your apps' section.
- Copy the <code>const firebaseConfig</code> dictionary to a safe place. You will need this later.

#### Hive RPi
- Connect RPi to a monitor, keyboard, and mouse OR connect to RPI in headless mode ([instructions](https://pimylifeup.com/headless-raspberry-pi-setup/)).
- Clone Git repository locally.
- Navigate to [HivePi folder](/HivePi/).
- Open the [hiveMain.py](/HivePi/hiveMain.py) file in a text editor.
- Replace <code>firebaseConfig</code> contents with the contents you copied earlier. This connects the code to your Firebase DB.

#### Webserver RPi
- Connect RPi to a monitor, keyboard, and mouse OR connect to RPI in headless mode ([instructions](https://pimylifeup.com/headless-raspberry-pi-setup/)).
- Clone Git repository locally.
- Navigate to [WebApp folder](/WebApp/).

##### Connect to Firebase
- Open the [mainDataProcessing.py](/WebApp/mainDataProcessing.py) file in a text editor.
- Replace <code>firebaseConfig</code> contents with the contents you copied earlier. This connects the code to your Firebase DB.

##### Set up local SQLite DB
- Run [createDatabaseTables.py](/WebApp/createDatabaseTables.py).
	<p><code>python3 createDatabaseTables.py</code></p>
- This initializes the SQLite DB for use later.

#### Set up Webserver
- Set up NGINX webserver that creates a reverse proxy server with Flask ([instructions](https://www.raspberrypi-spy.co.uk/2018/12/running-flask-under-nginx-raspberry-pi/)).
	- Ensure that the [flaskMain.py](/WebApp/flask/flaskMain.py) file is used for serving the website.

# Run instructions

If all instructions have been done to set up scripts to run on boot of RPis, all that is needed is to turn on the RPis and Arduinos.

## Start Python script on startup
- Follow this [tutorial](https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/) to set up scripts on startup of the RPi. The files that should execute on startup are:
	- Webserver RPi - [mainDataProcessing.py](/WebApp/mainDataProcessing.py).
	- Hive RPi - [hiveMain.py](/HivePi/hiveMain.py).
- NGINX webserver starts automatically on boot.

# Repository Structure
```
L1_G2_Project/
├── 3010 GUI Design/ #contains wireframe images for website
├── helper_functions/ ##contains functions used by multiple files, and unit test files for those functions/
│   ├── firebase.py
│   ├── mock_db.py
│   ├── process.py
│   ├── testFirebase.py
│   └── testProcess.py
├── Hive_Hardware_Subsystem/ ## contains code to install on Arduinos/
│   ├── Final_Product_Code/
│   │   ├── Base_Board_Arduino/
│   │   │   ├── Base_Board_Arduino.ino
│   │   │   ├── Soft_DFRobot_SHT3x.cpp
│   │   │   └── Soft_DFRobot_SHT3x.h
│   │   └── Seasonal_Cover_Arduino/
│   │       ├── arduino-lint.exe
│   │       ├── ClosedCube_BME680.cpp
│   │       ├── ClosedCube_BME680.h
│   │       ├── Seasonal_Cover_Ardino
│   │       ├── Soft_DFRobot_SHT3x.cpp
│   │       └── Soft_DFRobot_SHT3x.h
│   └── Test Code and Proof of Concept Code/ ## contains test code and POF code
├── HivePi/ ## contains Arduino code to install on Arduinos/
│   ├── hiveMain.py
│   ├── hiveTest.py
│   └── I2CLib.py
├── Lab4/ ## contains work for Lab 4 of SYSC 3010
├── Resources/
├── WebApp/ ## all files to run on webserver RPi are here/
│   ├── flask/
│   │   ├── static/ ## contains stylesheet, code for video player, and images to be used on website/
│   │   │   ├── dplayer/
│   │   │   │   ├── DPlayer.min.css
│   │   │   │   └── DPlayer.min.js
│   │   │   └── style.css
│   │   ├── templates/ ## HTML templates for website/
│   │   │   ├── baseLayout.html
│   │   │   ├── bees.html
│   │   │   ├── data.html
│   │   │   ├── index.html
│   │   │   ├── login.html
│   │   │   ├── more.html
│   │   │   ├── permission.html
│   │   │   ├── tools.html
│   │   │   └── video.html
│   │   ├── flaskMain.py
│   │   └── uwsgi.ini
│   ├── createDatabaseTables.py
│   ├── createSampleDatabase.py
│   ├── hiveDB.db
│   ├── hiveDB.sqbpro
│   ├── mainDataProcessing.py
│   └── Web GUI Test Case.pdf
├── WeeklyUpdates/ ## Contains weekly updates for all members
├── .gitignore
├── package-lock.json
└── README.md
```