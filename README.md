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

# Run instructions
To run the Honey, I'm a Smart Home! system, the beekeeper simply needs to run some programs:

- on the Hive RPi, navigate to the HivePi folder and run 
	<c>python3 hiveMain.py</c>

# Repository Structure
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