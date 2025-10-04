#include "LobotSerialServoControl.h" // 导入库文件(import library file)

// 控制总线舵机转动例程(bus servo rotation control program)

#define SERVO_SERIAL_RX   35
#define SERVO_SERIAL_TX   12
#define receiveEnablePin  13
#define transmitEnablePin 14
HardwareSerial HardwareSerial(2);
LobotSerialServoControl BusServo(HardwareSerial,receiveEnablePin,transmitEnablePin);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // 设置串口波特率(set baud rate of serial port)
  Serial.println("start...");  // 串口打印"start..."(serial port prints "start...")
  BusServo.OnInit();
  HardwareSerial.begin(115200,SERIAL_8N1,SERVO_SERIAL_RX,SERVO_SERIAL_TX);
  delay(500); // 延时500毫秒(delay for 500ms)
}
bool start_en = true;

void loop() {
  if (start_en) {
    Serial.print("ID: ");
    Serial.println(BusServo.LobotSerialServoReadID(0xFE)); // 获取舵机ID并通过串口打印(obtain servo ID and print via serial port)
    delay(500); // 延时(delay)
    
    uint8_t ID =BusServo.LobotSerialServoReadID(0xFE);
    
    BusServo.LobotSerialServoMove(ID,500,1000); // 设置舵机运行到500脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with pulse width 500 in 1000ms)
    delay(1000); // 延时1000毫秒(delay for 1000ms)
    
    Serial.println("Start turning the servo");
    BusServo.LobotSerialServoUnload(ID);//设置舵机掉电三秒钟(set the servo to power off for 3s)
    delay(3000); // 延时3000毫秒(delay for 3000ms)
    
    int16_t position=BusServo.LobotSerialServoReadPosition(ID);// 获取舵机现在的脉宽位置，运行时间为2000毫秒(obtain the current pulse width position of the servo, with the runtime of 2000ms)
    delay(2000); // 延时2000毫秒(delay for 2000ms)
    BusServo.LobotSerialServoMove(ID,500,1000); // 设置舵机运行到500脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with pulse width 500 in 1000ms)
    delay(2000); // 延时2000毫秒(delay for 2000ms)

    BusServo.LobotSerialServoMove(ID,position,1000); // 设置舵机运行到上一次的脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with previous pulse width in 1000ms)
    delay(1000); // 延时1000毫秒(delay for 1000ms)
    
    start_en = false;
  }
  else {
    delay(500); // 延时500毫秒(delay for 500ms)
  }
} 
