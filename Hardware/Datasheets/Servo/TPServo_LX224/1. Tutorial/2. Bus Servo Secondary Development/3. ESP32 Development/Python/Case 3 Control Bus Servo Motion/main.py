import time
from BusServo import BusServo

# 控制总线舵机转动例程(bus servo rotation control program)

bus_servo = BusServo() 

if __name__ == '__main__':
  ID =bus_servo.get_ID(254)                     # 获取舵机ID(obtain servo ID) 
  
  bus_servo.run(ID, 500, 1000) # 设置舵机运行到500脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with pulse width 500 in 1000ms)
  time.sleep_ms(1000)         # 延时1000毫秒（delay for 1000ms)
  
  bus_servo.run(ID, 1000, 1000) # 设置舵机运行到1000脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with pulse width 1000 in 1000ms)
  time.sleep_ms(1000)
  
  bus_servo.run(ID, 0, 2000) # 设置舵机运行到0脉宽位置，运行时间为2000毫秒(Set the servo to rotate to the position with pulse width 0 in 2000ms)
  time.sleep_ms(2000)
  
  bus_servo.run(ID, 500, 1000) # 设置舵机运行到500脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with pulse width 500 in 1000ms)
  time.sleep_ms(1000)




