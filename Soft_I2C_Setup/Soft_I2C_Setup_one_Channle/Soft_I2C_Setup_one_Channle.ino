#include <SoftWire.h>

#include <Wire.h>
#include "Soft_DFRobot_SHT3x.h"
#include "Zanshin_BME680.h"

char swTxBuffer[16];
char swRxBuffer[16];

int sdaPin = 8;
int sclPin = 7;



SoftWire sw(sdaPin, sclPin);

Soft_DFRobot_SHT3x tempSensor( &sw,/*address=*/0x45,/*RST=*/4);

BME680_Class climateSensor(&sw);
 
void setup() {

  

  sw.setTxBuffer(swTxBuffer, sizeof(swTxBuffer));
  sw.setRxBuffer(swRxBuffer, sizeof(swRxBuffer));
  sw.begin();

  Serial.begin(9600);
  Serial.println(" Starting! ");

  while (tempSensor.begin() != 0) {
    Serial.println("Failed to Initialize the chip, please confirm the wire connection");
    delay(1000);
  }

  Serial.print("Chip serial number");
  Serial.println(tempSensor.readSerialNumber());

  while (!climateSensor.begin()) {        // Find on I2C bus
    Serial.println("Error, unable to find BME680."); // Show error message
    delay(5000);                                     // Wait 5 seconds 
  }

  climateSensor.setOversampling(TemperatureSensor,Oversample1); // 16x sampling to temperature
  climateSensor.setOversampling(HumiditySensor,Oversample1); // Don't measure humidity
  climateSensor.setOversampling(PressureSensor,Oversample1); // 8x oversampling for pressure
  climateSensor.setIIRFilter(IIR4);  // Use enumerated type values
  Serial.print(F("- Setting gas measurement to 320\xC2\xB0\x43 for 150ms\n"));
  climateSensor.setGas(320, 150);  
  
}


void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(tempSensor.getTemperatureC());
  Serial.print(" C\n");

  Serial.print(tempSensor.getHumidityRH());
  Serial.print(" C\n");

  int32_t temperature,humidity,pressure,gas;
  uint8_t status = climateSensor.getSensorData(temperature,humidity,pressure,gas);

  Serial.print((int)temperature);
  Serial.print(" C says Climat Sensor\n");

  Serial.print(pressure/100);
  Serial.print(" hPA says Climat Sensor\n");

  Serial.print(HumiditySensor);
  Serial.print(" r% says Climat Sensor\n");

  Serial.print(gas);
  Serial.print(" Gas says Climat Sensor\n");

  delay(10000);
}
