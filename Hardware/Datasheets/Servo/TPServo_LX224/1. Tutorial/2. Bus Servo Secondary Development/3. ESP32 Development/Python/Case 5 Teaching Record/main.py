import time
from BusServo import BusServo
# 示教记录(teaching record)
bus_servo = BusServo() 

if __name__ == '__main__':
  ID =bus_servo.get_ID(254)                     # 获取舵机ID(obtain servo ID) 
    
  print('ID:', bus_servo.get_ID(254))
  time.sleep_ms(2000)         # 延时1000毫秒(delay for 2000ms)

  bus_servo.run(ID, 500, 1000) # 设置舵机运行到500脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with pulse width 500 in 1000ms)
  time.sleep_ms(1000)         # 延时1000毫秒(delay for 1000ms)
  print('Start turning the servo')
  
  bus_servo.unload(ID)
  time.sleep_ms(3000)         # 延时3000毫秒(delay for 3000ms)
  
  pos=bus_servo.get_position(ID) #记录舵机位置(record servo position)
  time.sleep_ms(2000)
  
  bus_servo.run(ID, 500, 2000) # 设置舵机运行到500脉宽位置，运行时间为2000毫秒(Set the servo to rotate to the position with pulse width 500 in 2000ms)
  time.sleep_ms(3000)
  
  bus_servo.run(ID, pos, 2000) # 设置舵机运行到500脉宽位置，运行时间为1000毫秒(Set the servo to rotate to the position with previous pulse width in 1000ms)
  time.sleep_ms(2000)








