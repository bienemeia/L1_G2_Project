#include <Wire.h>
#include <SoftWire.h>
#include "Soft_DFRobot_SHT3x.h"


//Ice Detector
const int LED1 = 3;//D3
const int DETECTOR1 = A7;//A7

const int LED2 = 4;//D4
const int DETECTOR2 = A6;//A6

const int LED3 = 5;//D3
const int DETECTOR3 = A2;//A2

const int LED4 = 6;//D6
const int DETECTOR4 = A1;//A1

//Relay
const int RELAY = 2;

//Blink LED
const int BLINKLED = 13;

//TempSensor
const int sdaPin = 8;
const int sclPin = 7;
char swTxBuffer[32];
char swRxBuffer[32];
SoftWire sw(sdaPin, sclPin);
Soft_DFRobot_SHT3x tempSensor( &sw,/*address=*/0x45,/*RST=*/4);


//state vars
int currTemp = 0;
uint16_t currHumidty = 0;
int iceStatus[4] = {0,0,0,0};
bool heatStatus = false;

byte regRequest = 0;

const byte systemNumber = 0x02;

void setup() {

  //serial
  Serial.begin(9600);
  Serial.println("Starting! Base Arduino");
  Serial.println("Enter 'h' for heater test");
  Serial.println("Enter 't' for temp sensor test");
  Serial.println("Enter 'l' for light sensor test\n\n");

  //SoftWire
  sw.setTxBuffer(swTxBuffer, sizeof(swTxBuffer));
  sw.setRxBuffer(swRxBuffer, sizeof(swRxBuffer));
  sw.begin();

  //I2C
  Wire.begin(0x3D);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);

  //Ice Detector
  pinMode(LED1,OUTPUT);
  pinMode(DETECTOR1,INPUT);

  pinMode(LED2,OUTPUT);
  pinMode(DETECTOR2,INPUT);

  pinMode(LED3,OUTPUT);
  pinMode(DETECTOR3,INPUT);

  pinMode(LED4,OUTPUT);
  pinMode(DETECTOR4,INPUT);

  digitalWrite(LED1,LOW);
  digitalWrite(LED2,LOW);
  digitalWrite(LED3,LOW);
  digitalWrite(LED4,LOW);

  //relay
  pinMode(RELAY,OUTPUT);

  //Blink LED
  pinMode(BLINKLED,OUTPUT);
  digitalWrite(BLINKLED,LOW);

  //tests
  testHeater();

  while(!testIceSensor()){
    Serial.println("Ice Sensor Error");
    blinkIceSensorError();
  }

   //TempSensor
  while (tempSensor.begin() != 0) {
    Serial.println("Failed to Initialize the chip, please confirm the wire connection");
    blinkTempSensorError();
  }

  Serial.print("Chip serial number: ");
  Serial.println(tempSensor.readSerialNumber());

}



void loop() {

  //update States
  currTemp = (uint16_t)(tempSensor.getTemperatureC() * 10.00);
  currHumidty = (uint16_t)(tempSensor.getHumidityRH() * 10.00);

  iceStatus[0] = analogRead(DETECTOR1);
  iceStatus[1] = analogRead(DETECTOR2);
  iceStatus[2] = analogRead(DETECTOR3);
  iceStatus[3] = analogRead(DETECTOR4);

  //update heater
  if(heatStatus){
    digitalWrite(RELAY,HIGH);
    Serial.println("Heater is on");
  }else{
    digitalWrite(RELAY,LOW);
    Serial.println("Heater is off");
  }


  Serial.print(((float)currTemp)/10.0);
  Serial.print(" C\n");

  Serial.print(((float)currHumidty)/10.0);
  Serial.print(" %H\n");


  Serial.print("Light values: ");
  Serial.print(analogRead(DETECTOR1));
  Serial.print("  ");

  Serial.print(analogRead(DETECTOR2));
  Serial.print("  ");

  Serial.print(analogRead(DETECTOR3));
  Serial.print("  ");

  Serial.print(analogRead(DETECTOR4));
  Serial.print("  \n");
  Serial.print("  \n");

  delay(5000);

  if(Serial.available() > 0){
    char command = Serial.read();

    if(command == 'h'){
      Serial.println("Starting Heater Test");
      testHeater();
      Serial.println("Test Completed");

    }else if(command == 't'){
      Serial.println("Starting Temp Sensor Chip Test");
      while (tempSensor.begin() != 0) {
        Serial.println("Failed to Initialize the chip, please confirm the wire connection");
        blinkTempSensorError();
      }
      Serial.println("Test Completed");

    }else if(command == 'l'){
      Serial.println("Starting Ice Sensor Test");
      testIceSensor();
      Serial.println("Test Completed");
    }
  }

}

/*
Sensor Blink Code (blink 3 times)
Ice Sensor Blink Code (blink 2 times)
*/


/**
A function that blink the erreo led for the number of times to reprent a temp sensor erreo
*/
void blinkTempSensorError(){

  for(int i = 0; i < 4; i++){
    digitalWrite(BLINKLED,HIGH);
    delay(500);
    digitalWrite(BLINKLED,LOW);
    delay(500);
  }
  delay(1000);
}

/**
A function that blink the erreo led for the number of times to reprent a Ice sensor erreo
*/
void blinkIceSensorError(){
  for(int i = 0; i < 3; i++){
    digitalWrite(BLINKLED,HIGH);
    delay(500);
    digitalWrite(BLINKLED,LOW);
    delay(500);
  }
  delay(1000);
}

/**
A function that test the heater relay.
*/
bool testHeater(){
  digitalWrite(RELAY,LOW);
  delay(1000);
  digitalWrite(RELAY,HIGH);
  Serial.println("Relay sould have clicked on.");
  delay(2000);
  digitalWrite(RELAY,LOW);
  Serial.println("Relay sould have clicked off.");
  delay(250);
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

  if(regRequest == 4){
    heatStatus = true;
  }else if(regRequest == 5){
    heatStatus = false;
  }
  
}

/**
An interrupt handler for i2c requestEvent
*/
void requestEvent() {

  if(regRequest == 0){
    Wire.write((uint8_t)systemNumber &0xFF);
    Serial.println("Sent System Number");

  }else if(regRequest == 1){
    send16BitNumber(currTemp); 
    Serial.println("Sent Tempature");

  }else if(regRequest == 2){
    send16BitNumber(currHumidty); 
    Serial.println("Sent Humidty");

  }else if(regRequest == 3){
    Wire.write(heatStatus&0xFF);
    Serial.println("Sent Heat Status");

  }else if(regRequest == 4){
    Wire.write(0xF);
    regRequest = 6;
    Serial.println("Heater Turned On");

  }else if(regRequest == 5){
    Wire.write(0xF);
    regRequest = 6;
    Serial.println("Heater Turned Off");

  }else if(regRequest == 6){
    send16BitNumber(iceStatus[0]); 
    Serial.println("Sent Ice Status");

  }else if(regRequest == 7){
    send16BitNumber(iceStatus[1]); 
    Serial.println("Sent Ice Status");

  }else if(regRequest == 8){
    send16BitNumber(iceStatus[2]);  
    Serial.println("Sent Ice Status");

  } else if(regRequest == 9){
    send16BitNumber(iceStatus[3]); 
    Serial.println("Sent Ice Status");

  }
  
}

/**
A function that converts a uint16_t to a byte array and send it.
*/
void send16BitNumber(uint16_t sendNumber){
    byte sendArray[2];
    sendArray[1] = ((sendNumber&0xFF00) >>8);
    sendArray[0] = (sendNumber & 0xFF);

    Serial.println(sendArray[0],HEX);
    Serial.println(sendArray[1],HEX);

    Wire.write(sendArray,2);
}

/**
A method that test the ice sensor.
*/
bool testIceSensor(){
  int lightValues1[4];
  int lightValues2[4];

  Serial.println("Testing Ice Sensor");

  digitalWrite(LED1,LOW);
  digitalWrite(LED2,LOW);
  digitalWrite(LED3,LOW);
  digitalWrite(LED4,LOW);

  delay(250);

  lightValues1[0] = analogRead(DETECTOR1);
  lightValues1[1] = analogRead(DETECTOR2);
  lightValues1[2] = analogRead(DETECTOR3);
  lightValues1[3] = analogRead(DETECTOR4);

  Serial.print(lightValues1[0]);
  Serial.print("  ");

  Serial.print(lightValues1[1]);
  Serial.print("  ");

  Serial.print(lightValues1[2]);
  Serial.print("  ");

  Serial.print(lightValues1[3]);
  Serial.print("  \n");

  delay(250);

  digitalWrite(LED1,HIGH);
  digitalWrite(LED2,HIGH);
  digitalWrite(LED3,HIGH);
  digitalWrite(LED4,HIGH);

  delay(250);

  lightValues2[0] = analogRead(DETECTOR1);
  lightValues2[1] = analogRead(DETECTOR2);
  lightValues2[2] = analogRead(DETECTOR3);
  lightValues2[3] = analogRead(DETECTOR4);

  Serial.print(lightValues2[0]);
  Serial.print("  ");

  Serial.print(lightValues2[1]);
  Serial.print("  ");

  Serial.print(lightValues2[2]);
  Serial.print("  ");

  Serial.print(lightValues2[3]);
  Serial.print("  \n");

  if(lightValues1[0] > lightValues2[0] && lightValues1[1] > lightValues2[1] && lightValues1[2] > lightValues2[2] && lightValues1[3] > lightValues2[3]){
    return true;
  }

  return false;
}
