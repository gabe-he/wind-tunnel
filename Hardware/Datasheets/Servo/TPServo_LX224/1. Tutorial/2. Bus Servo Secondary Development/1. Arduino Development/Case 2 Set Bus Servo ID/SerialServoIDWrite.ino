#include "include.h"
#include "SerialServo.h"

void setup() {
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  LobotSerialServoSetID(Serial, ID_ALL, 3);
  delay(500);
  int id = LobotSerialServoReadID(Serial);
  Serial.println("");
  Serial.print("new ID:");
  Serial.println(id);
  delay(1000);
}
