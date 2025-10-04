#include "include.h"
#include "SerialServo.h"

void setup() {
  Serial.begin(115200);
  LobotSerialServoMove(Serial, ID_ALL, 0, 500);   //初始设置舵机位置为0(initialize servo position to 0)
  delay(1000);
}

void loop() {
  LobotSerialServoMove(Serial, ID_ALL, 500, 1000);
  delay(1000);
  LobotSerialServoMove(Serial, ID_ALL, 1000, 500);
  delay(1000);
  LobotSerialServoMove(Serial, ID_ALL, 500, 1000);
  delay(1000);
  LobotSerialServoMove(Serial, ID_ALL, 0, 500); 
  delay(1000);
}
