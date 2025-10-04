import time
import Board

print('''
**********************************************************
********功能:幻尔科技树莓派扩展板，串口舵机运动例程(function:Hiwonder Raspberry Pi expansion board, read servo status)*******
**********************************************************
----------------------------------------------------------
Official website:http://www.lobot-robot.com/pc/index/index
Online mall:https://lobot-zone.taobao.com/
----------------------------------------------------------

----------------------------------------------------------
Usage:
    sudo python3 BusServo_Move.py
----------------------------------------------------------
Version: --V1.0  2021/08/16
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！(Press 'Ctrl+C' to exit this program. If it fails, please try again!)
----------------------------------------------------------
''')

while True:
	# 参数：参数1：舵机id; 参数2：位置; 参数3：运行时间(paramete: parameter 1: servo ID; parameter 2: position; parameter 3: runtime)
	# 舵机的转动范围0-240度，对应的脉宽为0-1000,即参数2的范围为0-1000(The range of rotation for the servo is 0-240 degrees, and the corresponding pulse width is 0-1000. Therefore, the range of parameter 2 is 0-1000)

	Board.setBusServoPulse(1, 800, 1000) # 6号舵机转到800位置，用时1000ms(Rotate servo 1 to position 800 in 1000ms)
	time.sleep(0.5) # 延时0.5s(delay for 0.5s)

	Board.setBusServoPulse(1, 200, 1000) # 6号舵机转到200位置，用时1000ms(Rotate servo 1 to position 200 in 1000ms)
	time.sleep(0.5) # 延时0.5s(delay for 0.5s)
	# for i in range(10):
	# 	Board.setBusServoPulse(1, 800, 1000) # 6号舵机转到800位置，用时1000ms(Rotate servo 1 to position 800 in 1000ms)
	# 	time.sleep(3) # 延时0.5s(delay for 0.5s)
	# 	print(i)
    
    
