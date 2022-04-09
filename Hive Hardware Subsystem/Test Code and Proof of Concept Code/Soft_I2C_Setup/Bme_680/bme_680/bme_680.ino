/**
This code is a testing ground and proof of concept for softI2C. Specifically for the BME680.
Section of this code is based on an example program from the ClosedCube library Written by AA. 
This code requres the https://www.arduino.cc/reference/en/libraries/softwire/ libary.
 
By Graham C. Bell 101150239
*/


#include <SoftWire.h>

#include <Wire.h>
#include "ClosedCube_BME680.h"

ClosedCube_BME680 bme680;

char swTxBuffer[128];
char swRxBuffer[128];

int sdaPin = 8;
int sclPin = 7;

SoftWire sw(sdaPin, sclPin);

void setup()
{

  sw.setTxBuffer(swTxBuffer, sizeof(swTxBuffer));
  sw.setRxBuffer(swRxBuffer, sizeof(swRxBuffer));
  sw.begin();

	Serial.begin(9600);
	Serial.println("ClosedCube BME680 ([T]empeature,[P]ressure,[H]umidity) Arduino Test");



	bme680.init(0x77,&sw); // I2C address: 0x76 or 0x77
	bme680.reset();

	Serial.print("Chip ID=0x");
	Serial.println(bme680.getChipID(), HEX);


	// oversampling: humidity = x1, temperature = x2, pressure = x16
	bme680.setOversampling(BME680_OVERSAMPLING_X1, BME680_OVERSAMPLING_X2, BME680_OVERSAMPLING_X16);
	bme680.setIIRFilter(BME680_FILTER_3);
  bme680.setGasOn(300, 100); // 300 degree Celsius and 100 milliseconds 

	bme680.setForcedMode();
  
}

void loop()
{
  
	ClosedCube_BME680_Status status = readAndPrintStatus();
	if (status.newDataFlag) {
		Serial.print("result: ");
		double temp = bme680.readTemperature();
		double pres = bme680.readPressure();
		double hum = bme680.readHumidity();

		Serial.print("T=");
		Serial.print(temp);
		Serial.print("C, RH=");
		Serial.print(hum);
		Serial.print("%, P=");
		Serial.print(pres);
		Serial.print("hPa");

    uint32_t gas = bme680.readGasResistance();

		Serial.print(", G=");
		Serial.print(gas);
		Serial.print(" Ohms");

		Serial.println();

		delay(2000); // let's do nothing and wait a bit before perform next measurements

		bme680.setForcedMode();
	} else {
		delay(200); // sensor data not yet ready
	}
  
}

ClosedCube_BME680_Status readAndPrintStatus() {
	ClosedCube_BME680_Status status = bme680.readStatus();
	d
}