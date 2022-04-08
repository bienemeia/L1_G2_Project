#include <Wire.h>
#include <SoftWire.h>
#include "Soft_DFRobot_SHT3x.h"
#include "ClosedCube_BME680.h"
#include <Stepper.h>
//Sensor setup values
ClosedCube_BME680 climateSensor;

char swTxBuffer[128];
char swRxBuffer[128];
int sdaPin = 8;
int sclPin = 7;
SoftWire sw(sdaPin, sclPin);
Soft_DFRobot_SHT3x tempSensor(&sw, /*address=*/0x45, /*RST=*/4);

//flapper
Stepper flapper = Stepper(2048, A3, A1, A2, A0);

//Blink LED
const int BLINKLED = 13;

//state vars
int currTempClimate = 0;
int currHumidtyClimate = 0;
int currPressureClimate = 0;
uint32_t currCO2Climate = 0;
bool sensorWarm = 0;
int currTempTemp = 0;
int currHumidtyTemp = 0;
bool flapperState = false;
int regRequest = 0;
const byte systemNumber = 0x01;

//time info
unsigned int sensorWarmUpTime = 0;  //36001 minumum time to read co2
unsigned int mesurmentTime = 0;

//Commands
const byte getID = 0;
const byte getTempatureInside = 1;
const byte getHumidityInside = 2;
const byte getPressureInside = 3;
const byte getCO2Inside = 4;
const byte getTempatureOutside = 5;
const byte getHumidityOutside = 6;
const byte openFlapper = 7;
const byte closeFlapper = 8;
const byte getFlapperStatus = 9;
const byte getCO2Status = 10;

void setup() {
  //Soft I2C
  sw.setTxBuffer(swTxBuffer, sizeof(swTxBuffer));
  sw.setRxBuffer(swRxBuffer, sizeof(swRxBuffer));
  sw.begin();

  //I2C
  Wire.begin(0x3C);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);

  //Serial setup
  Serial.begin(9600);
  Serial.println("Starting Hive Arduino!");
  Serial.println("Enter 'm' for flapper test");
  Serial.println("Enter 'c' for climate sensor test");
  Serial.println("Enter 't' for temp sensor test\n\n");


  //bme680 setup
  climateSensor.init(0x77, &sw);  // I2C address: 0x76 or 0x77
  climateSensor.reset();

  while (climateSensor.getChipID() != 0x61) {
    Serial.println("Failed to Initialize the climate sensor, please confirm the wire connection");
    blinkClimateSensorFailure();
  }

  Serial.print("BME680 Chip ID=0x");
  Serial.println(climateSensor.getChipID(), HEX);
  // oversampling: humidity = x16, temperature = x16, pressure = x16
  climateSensor.setOversampling(BME680_OVERSAMPLING_X1, BME680_OVERSAMPLING_X2, BME680_OVERSAMPLING_X16);
  climateSensor.setIIRFilter(BME680_FILTER_3);
  climateSensor.setGasOn(300, 100);  // 300 degree Celsius and 100 milliseconds
  climateSensor.setForcedMode();

  //SHT31 Setup
  while (tempSensor.begin() != 0) {
    Serial.println("Failed to Initialize the chip, please confirm the wire connection");
    blinkTempSensorError();
  }

  Serial.print("SHT31 Chip serial number: ");
  Serial.println(tempSensor.readSerialNumber());

  //setUpflapper
  flapper.setSpeed(1);
  testFlapper();
}



/**
This is the main for this Arduino. It operates on a system time skeem so that the flapper does not interrupt the co2 measurement status.
*/
void loop() {
  //update Flapper
  static int flapperOpening = 0;
  if (flapperState && flapperOpening <= 512) {
    flapper.step(1);
    flapperOpening++;
  } else if (!flapperState && flapperOpening >= 0) {
    flapper.step(-1);
    flapperOpening--;

  }

  //update values
  if (40 == mesurmentTime) {
    mesurmentTime = 0;
    takeMesurments();
  } else {
    mesurmentTime++;
  }

  //update sensorWarmUpTime
  if (sensorWarmUpTime <= 36001 && !sensorWarm) {
    sensorWarmUpTime++;
  }
  if (sensorWarmUpTime >= 36000) {
    sensorWarm = true;
  }

  //get Test commands

  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'm') {
      testFlapper();
      Serial.println("Test Completed");

    } else if (command == 'c') {
      Serial.println("Starting Climate Sensor Chip test");
      while (climateSensor.getChipID() != 0x61) {
        Serial.println("Failed to Initialize the climate sensor, please confirm the wire connection");
        blinkClimateSensorFailure();
      }
      Serial.println("Test Completed");

    } else if (command == 't') {
      Serial.println("Starting Temp Sensor Chip test");
      while (tempSensor.begin() != 0) {
        Serial.println("Failed to Initialize the chip, please confirm the wire connection");
        blinkTempSensorError();
      }
      Serial.println("Test Completed");
    }
  }

  delay(50);
}

/**
This function takes all mesurments and updates there values.
*/
void takeMesurments() {
  ClosedCube_BME680_Status status = readBME680Status();

  if (status.newDataFlag) {

    double temp = climateSensor.readTemperature();
    double pres = climateSensor.readPressure();
    double hum = climateSensor.readHumidity();
    uint32_t gas = climateSensor.readGasResistance();

    currTempClimate = (int)(temp * 10.00);
    currHumidtyClimate = (int)(hum * 10.00);
    currPressureClimate = (int)(pres);
    currCO2Climate = gas;

    currTempTemp = (int)(tempSensor.getTemperatureC() * 10.00);
    currHumidtyTemp = (int)(tempSensor.getHumidityRH() * 10.00);

    Serial.print((float)(currTempTemp / 10));
    Serial.print(" C\n");

    Serial.print((float)(currHumidtyTemp / 10));
    Serial.print(" %H\n");

    Serial.print("result: ");

    Serial.print("T=");
    Serial.print((float)(currTempClimate / 10));
    Serial.print("C, RH=");
    Serial.print((float)(currHumidtyClimate / 10));
    Serial.print("%, P=");
    Serial.print((float)(currPressureClimate));
    Serial.print("hPa");

    Serial.print(", G=");
    Serial.print(currCO2Climate);
    Serial.print(" Ohms");

    Serial.println();

    climateSensor.setForcedMode();
  } else {
  }
}

/**
A function that checks is the climate sensor is redy to be readed. 
*/
ClosedCube_BME680_Status readBME680Status() {
  ClosedCube_BME680_Status status = climateSensor.readStatus();
  return status;
}

/**
A interrupt handler for i2c receiveEvent
*/
void receiveEvent(int howMany) {
  while (0 < Wire.available()) {
    regRequest = Wire.read();
  }
  Serial.print("Reg Request: ");
  Serial.println(regRequest);

  if (regRequest == openFlapper) {
    flapperState = true;
    Serial.println("Opened flapper");

  } else if (regRequest == closeFlapper) {
    flapperState = false;
    Serial.println("Closed flapper");

  }
}

/**
An interrupt handler for i2c requestEvent
*/
void requestEvent() {
  if (regRequest == getID) {
    Wire.write((uint8_t)systemNumber & 0xFF);
    Serial.println("Sent System Number");

  } else if (regRequest == getTempatureInside) {
    send16BitNumber(currTempClimate);
    Serial.println("Sent Tempature inturnal");

  } else if (regRequest == getHumidityInside) {
    send16BitNumber(currHumidtyClimate);
    Serial.println("Sent Humidty inturnal");

  } else if (regRequest == getPressureInside) {
    send16BitNumber(currPressureClimate);
    Serial.println("Sent Humidty inturnal");

  } else if (regRequest == getCO2Inside) {
    send16BitNumber(currCO2Climate);
    Serial.println("Sent Pressure inturnal");

  } else if (regRequest == getTempatureOutside) {
    send16BitNumber(currTempTemp);
    Serial.println("Sent Tempature external");

  } else if (regRequest == getHumidityOutside) {
    send16BitNumber(currHumidtyTemp);
    Serial.println("Sent Humidty external;");

  } else if (regRequest == openFlapper) {
    Wire.write(0xF);
    regRequest = getFlapperStatus;

  } else if (regRequest == closeFlapper) {
    Wire.write(0xF);
    regRequest = getFlapperStatus;

  } else if (regRequest == getFlapperStatus) {
    Wire.write(flapperState & 0xF);
    Serial.println("Sent flapper Status");

  } else if (regRequest == getCO2Status) {
    Wire.write(sensorWarm & 0xF);
    Serial.println("Sent sensorWarm Status");

  }
}

/**
A function that converts a uint16_t to a byte array and send it.
*/
void send16BitNumber(uint16_t sendNumber) {
  byte sendArray[2];
  sendArray[1] = ((sendNumber & 0xFF00) >> 8);
  sendArray[0] = (sendNumber & 0xFF);

  Serial.println(sendArray[0], HEX);
  Serial.println(sendArray[1], HEX);

  Wire.write(sendArray, 2);
}

/**
A function that tests the plapper valve.
*/
void testFlapper() {
  Serial.println("Commencing flapper Test");
  delay(1000);
  flapper.step(512);
  Serial.println("Flapper sould now be open");
  delay(1000);
  flapper.step(0 - (512));
  Serial.println("Flapper sould now be closed");
}



/**
A function that blinks the error led 2 time to show a climate sensor error.
*/
void blinkClimateSensorFailure() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(BLINKLED, HIGH);
    delay(500);
    digitalWrite(BLINKLED, LOW);
    delay(500);
  }
  delay(1000);
}

/**
A function that blinks the error led 3 time to show a Temp sensor error.
*/
void blinkTempSensorError() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(BLINKLED, HIGH);
    delay(500);
    digitalWrite(BLINKLED, LOW);
    delay(500);
  }
  delay(1000);
}
