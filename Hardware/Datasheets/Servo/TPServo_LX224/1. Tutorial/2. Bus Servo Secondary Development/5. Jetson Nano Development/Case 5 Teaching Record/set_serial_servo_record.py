#!/usr/bin/env python3
# encoding: utf-8
import sys
import time
sys.path.append("..")
from sdk import hiwonder_servo_controller

servo_control = hiwonder_servo_controller.HiwonderServoController('/dev/ttyTHS1', 115200)

servo_id = servo_control.get_servo_id()
print('id:',servo_id)
print('可以开始转动舵机')
servo_control.set_servo_position(servo_id, 500, 500)
print('可以开始转动舵机')
servo_control.unload_servo(servo_id,False)

print('可以开始转动舵机')
time.sleep(3)
mode = int(input('input mode:'))
if mode == 0:
    servo_control.get_servo_position(servo_id)
    pos = servo_control.get_servo_position(servo_id)
    servo_control.set_servo_position(servo_id, 0, 500)
    time.sleep(3)
    servo_control.set_servo_position(servo_id, pos, 500)

                  

