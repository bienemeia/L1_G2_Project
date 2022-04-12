/**
This is a test program to test if hard I2C is working.
This code implements an I2C responder. It can be installed on most Arduinos.
 
By Graham C. Bell 101150239
*/


#include <Wire.h>

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
void receiveEvent(int y) {

  byte x;

  // Read while data received
  while (0 < Wire.available()) {
    x = Wire.read();
  }
  
  if(x = 0x0){
      digitalWrite(LED_BUILTIN, HIGH);
  }else{
      digitalWrite(LED_BUILTIN, LOW);
  }
  
  Serial.println("Receive event");
}


/**
ISR for a i2C request event.
*/
void requestEvent() {
  
  Wire.write((byte)1);
  Serial.println("Request event");
}

void loop() {
  // put your main code here, to run repeatedly:

}
