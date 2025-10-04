#include "LobotSerialServoControl.h" // 导入库文件(import library file)

// 控制总线舵机速度例程(bus servo speed control program)

#define SERVO_SERIAL_RX   35
#define SERVO_SERIAL_TX   12
#define receiveEnablePin  13
#define transmitEnablePin 14
HardwareSerial HardwareSerial(2);
LobotSerialServoControl BusServo(HardwareSerial,receiveEnablePin,transmitEnablePin);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);        // 设置串口波特率(set baud rate of serial port)
  Serial.println("start...");  // 串口打印"start..."(serial port prints "start...")
  BusServo.OnInit();           // 初始化总线舵机库(initialize bus servo library)
  HardwareSerial.begin(115200, SERIAL_8N1, SERVO_SERIAL_RX, SERVO_SERIAL_TX);
  delay(500);                  // 延时500毫秒(delay for 500ms)
}

bool start_en = true;

void loop() {
   
   if(start_en){  
    Serial.print("oldID: ");
    Serial.println(BusServo.LobotSerialServoReadID(0xFE)); // 获取舵机ID并通过串口打印(obtain servo ID and print via serial port)
    delay(1000); // 延时(delay)
    
    uint8_t oldID =BusServo.LobotSerialServoReadID(0xFE);
    delay(1000); // 延时(delay)
    
    uint8_t newID =2;
    BusServo.LobotSerialServoSetID(oldID,newID);
    delay(1000); // 延时(delay)
    
    Serial.print("newID: ");
    Serial.println(String(newID)); // 获取舵机位置并通过串口打印(obtain servo position and print via serial port)
    delay(500); // 延时(delay)
  
    start_en = false;
  }
  else{
    delay(500); // 延时500毫秒(delay for 500ms)
  }

}
