#!/usr/bin/env python3
# encoding: utf-8
import sys
import time
sys.path.append("..")
from sdk import hiwonder_servo_controller

servo_control = hiwonder_servo_controller.HiwonderServoController('/dev/ttyTHS1', 115200)

print('serial servo move at different speed')


servo_id = 6  # 舵机id(0-253)(servo ID (0-253))
position = 500  # 位置(0-1000)(position(0-1000))
duration = 1000  # 时间(20-30000)(time(20-30000))
servo_control.set_servo_position(servo_id, position, duration)
time.sleep(duration/1000.0 + 0.1)
        
servo_id = 6
position = 1000
duration = 500
servo_control.set_servo_position(servo_id, position, duration)
time.sleep(duration/1000.0 + 0.1)

servo_id = 6  # 舵机id(0-253)(servo ID (0-253))
position = 500  # 位置(0-1000)(position(0-1000))
duration = 1000  # 时间(20-30000)(time(20-30000))
servo_control.set_servo_position(servo_id, position, duration)
time.sleep(duration/1000.0 + 0.1)
        
servo_id = 6
position = 0
duration = 500
servo_control.set_servo_position(servo_id, position, duration)
time.sleep(duration/1000.0 + 0.1)
