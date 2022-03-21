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
Soft_DFRobot_SHT3x tempSensor( &sw,/*address=*/0x45,/*RST=*/4);

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

const byte systemNumber = 1;

//time info
unsigned int sensorWarmUpTime = 0;//36001 minumum
unsigned int mesurmentTime = 0;

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
	Serial.println("Starting!");

  //bme680 setup
  climateSensor.init(0x77,&sw); // I2C address: 0x76 or 0x77
	climateSensor.reset();

  while(climateSensor.getChipID() != 0x61){
    Serial.println("Failed to Initialize the climate sensor, please confirm the wire connection");
    blinkClimateSensorFailure();

  }

  Serial.print("BME680 Chip ID=0x");
	Serial.println(climateSensor.getChipID(), HEX);
  // oversampling: humidity = x16, temperature = x16, pressure = x16
	climateSensor.setOversampling(BME680_OVERSAMPLING_X1, BME680_OVERSAMPLING_X2, BME680_OVERSAMPLING_X16);
	climateSensor.setIIRFilter(BME680_FILTER_3);
  climateSensor.setGasOn(300, 100); // 300 degree Celsius and 100 milliseconds 
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
  
  /*
  pinMode(FLAPPERPIN,OUTPUT);
  analogWrite(FLAPPERPIN,0);
  testFlapper();
*/
}


void loop()
{
  //update Flapper
  static int flapperOpening = 0;
  if(flapperState && flapperOpening <= 512){
    flapper.step(1);
    flapperOpening++;
  }else if(!flapperState && flapperOpening >= 0){
    flapper.step(-1);
    flapperOpening--;

  }else {
    
  }

  
  //update values
  if(40 == mesurmentTime){
    mesurmentTime = 0;
    takeMesurments();
  }else{
    mesurmentTime++;
  }

  //update time
  if (sensorWarmUpTime <= 36001 && !sensorWarm){
      sensorWarmUpTime++;
  }
  if(sensorWarmUpTime >= 36000){
    sensorWarm = true;
  }

  delay(50);
}

void takeMesurments(){
  	ClosedCube_BME680_Status status = readAndPrintStatus();

	if (status.newDataFlag) {

    double temp = climateSensor.readTemperature();
		double pres = climateSensor.readPressure();
		double hum = climateSensor.readHumidity();
    uint32_t gas = climateSensor.readGasResistance();

    currTempClimate = (int)(temp*10.00);
    currHumidtyClimate = (int)(hum*10.00) ;
    currPressureClimate = (int)(pres);
    currCO2Climate = gas;

    currTempTemp = (int)(tempSensor.getTemperatureC() * 10.00);
    currHumidtyTemp = (int)(tempSensor.getHumidityRH() * 10.00);

    Serial.print((float)(currTempTemp/10));
    Serial.print(" C\n");

    Serial.print((float)(currHumidtyTemp/10));
    Serial.print(" %H\n");

		Serial.print("result: ");

		Serial.print("T=");
		Serial.print((float)(currTempClimate/10));
		Serial.print("C, RH=");
		Serial.print((float)(currHumidtyClimate/10));
		Serial.print("%, P=");
		Serial.print((float)(currPressureClimate/10));
		Serial.print("hPa");



		Serial.print(", G=");
		Serial.print(currCO2Climate);
		Serial.print(" Ohms");

		Serial.println();

    //update state values
    

		climateSensor.setForcedMode();
	} else {
	}

}

ClosedCube_BME680_Status readAndPrintStatus() {
	ClosedCube_BME680_Status status = climateSensor.readStatus();
  return status;
}

void receiveEvent(int howMany) {
  while (Wire.available()) { 
    regRequest = Serial.parseInt();
  }
  Serial.print("Reg Request: ");
  Serial.println(regRequest);

  if(regRequest == 7){
    flapperState = true;
    Wire.write(0xF);
    regRequest = 9;
    Serial.println("Heater Turned On");

  }else if(regRequest == 8){
    flapperState = false;
    Wire.write(0xF);
    regRequest = 9;
    Serial.println("Heater Turned Off");

  }
  
}

void requestEvent() {

  if(regRequest == 0){
    Wire.write((byte)systemNumber);
    Serial.println("Sent System Number");

  }else if(regRequest == 1){
    Wire.write(currTempClimate);
    Serial.println("Sent Tempature inturnal");

  }else if(regRequest == 2){
    Wire.write(currHumidtyClimate);
    Serial.println("Sent Humidty inturnal");

  }else if(regRequest == 3){
    Wire.write(currPressureClimate);
    Serial.println("Sent Humidty inturnal");

  }else if(regRequest == 4){
    Wire.write(currCO2Climate);
    Serial.println("Sent Pressure inturnal");

  }else if(regRequest == 5){
    Wire.write(currTempTemp);
    Serial.println("Sent Tempature external");

  }else if(regRequest == 6){
    Wire.write(currHumidtyTemp);
    Serial.println("Sent Humidty external;");

  }else if(regRequest == 9){
    Wire.write(flapperState);
    Serial.println("Sent flapper Status");
  }else if(regRequest == 10){
    Wire.write(sensorWarm);
    Serial.println("Sent sensorWarm Status");
  }
  
}



void testFlapper(){
  Serial.println("Commencing flapper Test");
  delay(1000);
  flapper.step(512);
  Serial.println("Flapper sould now be open");
  delay(1000);
  flapper.step(0-(512));
  Serial.println("Flapper sould now be closed");
  
}

/*
  blink codes
  climate sensor 2
  temp sensor 3
*/

void blinkClimateSensorFailure(){
  digitalWrite(BLINKLED,HIGH);
  delay(250);
  digitalWrite(BLINKLED,LOW);
  delay(250);
  digitalWrite(BLINKLED,HIGH);
  delay(250);
  digitalWrite(BLINKLED,LOW);
  delay(1000);
}

void blinkTempSensorError(){
  digitalWrite(BLINKLED,HIGH);
  delay(500);
  digitalWrite(BLINKLED,LOW);
  delay(500);
  digitalWrite(BLINKLED,HIGH);
  delay(500);
  digitalWrite(BLINKLED,LOW);
  delay(500);
  digitalWrite(BLINKLED,HIGH);
  delay(500);
  digitalWrite(BLINKLED,LOW);
  delay(1000);
}
	