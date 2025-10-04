import time
from BusServo import BusServo

# 控制总线舵机速度例程(bus servo speed control program)

bus_servo = BusServo() 

if __name__ == '__main__':
  ID =bus_servo.get_ID(254)                     # 获取舵机ID(obtain servo ID) 
  
  bus_servo.run(ID, 500, 500) # 设置舵机运行到500脉宽位置，运行时间为500毫秒(Set the servo to rotate to the position with pulse width 500 in 500ms)
  time.sleep_ms(1000)         # 延时1000毫秒(delay for 1000ms)
  
  bus_servo.run(ID, 1000, 500) # 设置舵机运行到1000脉宽位置，运行时间为500毫秒(Set the servo to rotate to the position with pulse width 1000 in 500ms)
  time.sleep_ms(1000)
  
  bus_servo.run(ID, 500, 1500) # 设置舵机运行到500脉宽位置，运行时间为1500毫秒(Set the servo to rotate to the position with pulse width 500 in 1500ms)
  time.sleep_ms(2000)
  
  bus_servo.run(ID, 0, 2500) # 设置舵机运行到0脉宽位置，运行时间为2500毫秒(Set the servo to rotate to the position with pulse width 0 in 2500ms)
  time.sleep_ms(3000)
  
  bus_servo.run(ID, 500, 3500) # 设置舵机运行到500脉宽位置，运行时间为3500毫秒(Set the servo to rotate to the position with pulse width 500 in 3500ms)
  time.sleep_ms(4000)





