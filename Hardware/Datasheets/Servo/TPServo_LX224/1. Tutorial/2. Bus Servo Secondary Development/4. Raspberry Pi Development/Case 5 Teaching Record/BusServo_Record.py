import time
import Board

print('''
**********************************************************
*****功能:幻尔科技树莓派扩展板，串口舵机读取状态例程(function:Hiwonder Raspberry Pi expansion board, read servo status)******
**********************************************************
----------------------------------------------------------
Official website:http://www.lobot-robot.com/pc/index/index
Online mall:https://lobot-zone.taobao.com/
----------------------------------------------------------

----------------------------------------------------------
Usage:
    sudo python3 BusServo_ReadStatus.py
----------------------------------------------------------
Version: --V1.0  2021/08/16
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！(Press 'Ctrl+C' to exit this program. If it fails, please try again!)
----------------------------------------------------------
''')

servo_id = Board.getBusServoID()
print('id:',servo_id)
Board.setBusServoPulse(servo_id, 500, 1000) # 1号舵机转到500位置用时1000ms(control servo 1 to rotate to position 500 in 1000ms)
time.sleep(1)
pos1 = Board.setBusServoPulse(servo_id, 500, 1000)
print('pos1:',pos1)
# servo_control.unload_servo(servo_id,False)
Board.unloadBusServo(servo_id)

print('可以开始转动舵机')
time.sleep(4)
mode = int(input('input mode:'))
if mode == 0:
    Board.getBusServoPulse(servo_id)
    pos = Board.getBusServoPulse(servo_id)
    print('pos:',pos)
    Board.setBusServoPulse(servo_id, 0, 1000)
    time.sleep(3)
    Board.setBusServoPulse(servo_id, pos, 1000)
    time.sleep(3)
   
    
 
