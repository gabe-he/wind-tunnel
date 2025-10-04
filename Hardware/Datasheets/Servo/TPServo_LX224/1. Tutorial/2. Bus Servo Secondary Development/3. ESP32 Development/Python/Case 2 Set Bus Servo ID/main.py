import time
from BusServo import BusServo

# 读取总线舵机信息(obtain bus servo information)

bus_servo = BusServo() 

if __name__ == '__main__':
  
  ID =bus_servo.get_ID(254)                     # 获取舵机ID(obtain servo ID)
    
  print('ID:', bus_servo.get_ID(254))           # 打印舵机ID(print servo ID)
  
  print('Position:', bus_servo.get_position(ID)) # 获取舵机位置(obtain servo position)
  
  print('Vin:', bus_servo.get_vin(ID)/1000)      # 获取舵机电压(obtain servo position)
  
  print('Offset:', bus_servo.get_offset(ID))     # 获取舵机偏差值(obtain servo deviation value)
  
  print('Temp:', bus_servo.get_temp(ID))         # 获取舵机温度(obtain servo temperature)
 
  








