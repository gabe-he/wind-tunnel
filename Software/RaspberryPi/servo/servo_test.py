from servo.Servo import Servo
import time

servo = Servo("/dev/ttyUSB0")
servo.open()
id = servo.get_id()
print(f'Servo ID: {id}')
pos = servo.get_pos()
print(f'Servo Position: {pos}')
tmp = servo.get_tmp()
print(f'Servo Temperature: {tmp} deg C')
vin = servo.get_vin()
print(f'Servo Voltage: {vin/1000}V')
servo.set_pos(None, 500)
time.sleep(3)
servo.set_pos(None, 400)
