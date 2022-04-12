#include <Wire.h>
/**
This is a test program to test if hard I2C is working.
This code implements a I2C responder. It is designed to demonstrate a unit test where a RPI is able to communicate with an arduino.
This code is designed specifically to work with an arduino due.
 
By Graham C. Bell 101150239
*/

int outPut = 0;

void setup() {
  Wire.begin(0x3C);

  Wire.onRequest(requestEvent);
  
  Wire.onReceive(receiveEvent);
  
  Serial.begin(9600);
  Serial.println("I2C Responder Demonstration");
  pinMode(LED_BUILTIN, OUTPUT);

}

/**
ISR for a i2C receive event.
*/
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    digitalWrite(LED_BUILTIN, c);
  }

  Serial.println("Receive Event");
}


void loop() {
  delay(100);
  if (Serial.available() > 1 ) {
    outPut = Serial.parseInt();
    Serial.println("Out Put set to");
    Serial.println(outPut);
  }
 
}

/**
ISR for a i2C receive event.
*/
void requestEvent() {
  
  Wire.write((byte)outPut);
  Serial.println("Request event");
}
