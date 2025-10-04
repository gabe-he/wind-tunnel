#include "include.h"
#include "SerialServo.h"

void setup() {
  Serial.begin(115200);
  delay(1000);
}

void loop() {
  LobotSerialServoMove(Serial, ID_ALL, 0, 1000);
  delay(1000);
  LobotSerialServoMove(Serial, ID_ALL, 1000, 1000);
  delay(1000);
}
