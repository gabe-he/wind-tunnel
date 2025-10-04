import time
import Board

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，串口舵机变速例程(function:Hiwonder Raspberry Pi expansion board, bus servo speed control)*******
**********************************************************
----------------------------------------------------------
Official website:http://www.lobot-robot.com/pc/index/index
Online mall:https://lobot-zone.taobao.com/
----------------------------------------------------------

----------------------------------------------------------
Usage:
    sudo python3 BusServo_Speed.py
----------------------------------------------------------
Version: --V1.0  2021/08/16
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！(Press 'Ctrl+C' to exit this program. If it fails, please try again!)
----------------------------------------------------------
''')
servo_id = Board.getBusServoID()
while True:
	# 参数：参数1：舵机id; 参数2：位置; 参数3：运行时间(Parameters: parameter 1: servo ID; parameter 2: position; parameter 3: running time)
	# 舵机的转动范围0-240度，对应的脉宽为0-1000,即参数2的范围为0-1000(The range of rotation for the servo is 0-240 degrees, and the corresponding pulse width is 0-1000. Therefore, the range of parameter 2 is 0-1000)

	Board.setBusServoPulse(servo_id, 500, 1000) 
	time.sleep(2)

	Board.setBusServoPulse(servo_id, 1000, 500) 
	time.sleep(1) 

	Board.setBusServoPulse(servo_id, 500, 1500) 
	time.sleep(2)

	Board.setBusServoPulse(servo_id, 0, 2500) 
	time.sleep(3) 
	     
	Board.setBusServoPulse(servo_id, 500, 3500) 
	time.sleep(4) 
	     
