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

# Run instructions (really, should set up so the right code runs on boot)
To run the Honey, I'm a Smart Home! system, the beekeeper simply needs to run some programs:

## Run Hive RPi code

- on the Hive RPi, navigate to the HivePi folder and run 
	<p><code>python3 hiveMain.py</code></p>
	The Hive RPi will begin reading sensor data and sending it to Firebase.

## Create DB and run data processing code

- on the Webserver RPi, navigate to the WebApp folder and run
	<p><code>python3 createDatabaseTables.py</code></p>
	The RPi will create the SQLite database needed. If the DB already exists, "Already exists" will print to the console.

- on the Webserver RPi, in the same WebApp folder, run
	<p><code>python3 mainDataProcessing.py</code></p>
	The RPi will begin pulling data from Firebase, and processing it into the local database.

## Start server

<p><em>If running on local network</em></p>

- on Webserver RPi, open a new terminal. Navigate to the WebApp/flask folder. Enter
	<p><code>export FLASK_APP=flaskMain.py</code></p>
	Then enter
	<p><code>flask run</code></p>
	A URL will appear in the terminal that can be used on any computer in the local area network to access the website.

<p><em>If running a Webserver</em></p>
- Access the website through a URL set up during the web server set up.

## Wiring

### BaseBoard Arduino Subsystem

This subsystem is the bottom board temperature measurement, Ice Sensor and Heater. The wiring diagram and setup diagram is available for this subsystem. 
The [wiring diagram is available here ](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%202%20System_Skeam.png) and the 
[setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%202%20System.png)
 
### Hive Top Arduino Subsystem

This subsystem is the hive top temperature measurement, outside temperature measurement and flapper. The wiring diagram and setup diagram is available for this subsystem. 
The [wiring diagram is available here ](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%201%20System_schem.png) and the 
[setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Arduino%201%20System.png)

### BackBone Communication and Hive Top RPI 
This subsystem is the main communication system for the hive top pi and the Arduino subsystem. 
The [wiring diagram is available here ](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Seasonal%20Innercove%20and%20BaseBoard%20Communication%20system_schem.png) and the [setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Seasonal%20Innercove%20and%20BaseBoard%20Communication%20system..png)

### Web Server Pi
This Subsystem is responsible for hosting the website. The [setup diagram is available here.](https://github.com/bienemeia/L1_G2_Project/blob/main/Wiring%20Diagrams/Raspberry%20Pi%201.png)

	

# Repository Structure
```
L1_G2_Project/
├── 3010 GUI Design //contains wireframe images for website
├── helper_functions/ #contains 
├── Hive Hardware Subsystem/
├── HivePi/
├── Lab4/ contains work for Lab 4 of SYSC 3010
├── Resources/
├── WebApp // all files to run on webserver RPi are here/
│   └── flask/
├── WeeklyUpdates // Contains weekly updates for all members
├── .gitignore
├── package-lock.json
└── README.md
```