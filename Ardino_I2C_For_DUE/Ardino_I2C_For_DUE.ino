#include <Wire.h>

void setup() {
  Wire.begin(0x3C);

  Wire.onRequest(requestEvent);
  
  Wire.onReceive(receiveEvent);
  
  Serial.begin(9600);
  Serial.println("I2C Responder Demonstration");
  pinMode(LED_BUILTIN, OUTPUT);

}

void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    digitalWrite(LED_BUILTIN, c);
  }

  Serial.println("Receive Event");
}


void loop() {
  delay(100);
}

void requestEvent() {
  
  Wire.write((byte)1);
  Serial.println("Request event");
}
