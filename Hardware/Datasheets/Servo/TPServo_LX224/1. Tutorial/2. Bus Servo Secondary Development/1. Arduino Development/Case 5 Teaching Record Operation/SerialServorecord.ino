#include "include.h"
#include "SerialServo.h"

#define KEY1   2    //定义按键1(define button 1)
#define KEY2   4    //定义按键2(define button 2)

void setup() {
  Serial.begin(115200);
  pinMode(2, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  delay(1000);
}

int id;

void loop() {
   static bool run = false;
  static char step = 0;
  static char mode = 0;
  static int pos[4] = {100,200,300,400};
  uint16_t temp;
  id = LobotSerialServoReadID(Serial);
  while (1) {
    if (mode == 0)
    {
      if (run)
      {
        LobotSerialServoMove(Serial, id, pos[step++], 500);
        if (step == 4)
        {
          step = 0;
          run = false;
        }
        delay(1000);
      }
      if (!digitalRead(KEY2))
      {
        delay(10);
        if (!digitalRead(KEY2))
        {
          run = true;
          step = 0;
          delay(500);
        }
      }
      if (!digitalRead(KEY1))
      {
        delay(10);
        if (!digitalRead(KEY1))
        {
          LobotSerialServoUnload(Serial, id);
          mode = 1;
          step = 0;
          delay(500);
        }
      }
    }
    if (mode == 1)
    {
      if (!digitalRead(KEY2))
      {
        delay(10);
        if (!digitalRead(KEY2))
        {
          pos[step++] = LobotSerialServoReadPosition(Serial, id);
          if (step == 4)
            step = 0;
          delay(500);
        }
      }
      if (!digitalRead(KEY1))
      {
        delay(10);
        if (!digitalRead(KEY1))
        {
          temp = LobotSerialServoReadPosition(Serial, id);
          LobotSerialServoMove(Serial, id, temp, 200);
          mode = 0;
          delay(500);
        }
      }
    }
  }
}
