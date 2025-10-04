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
def getBusServoStatus(servo_id):
    Pulse = Board.getBusServoPulse(servo_id) # 获取舵机的位置信息(obtain position information of the servo)
    Temp = Board.getBusServoTemp(servo_id) # 获取舵机的温度信息(obtain temperature information of the servo)
    Vin = Board.getBusServoVin(servo_id) # 获取舵机的电压信息(obtain voltage information of the servo)
    print('Pulse: {}\nTemp:  {}\nVin:   {}\nid:   {}\n'.format(Pulse, Temp, Vin, servo_id)) # 打印状态信息(print status information)
    time.sleep(0.5) # 延时方便查看(delay for easier check)

   
Board.setBusServoPulse(servo_id, 500, 1000) # 1号舵机转到500位置用时1000ms(Rotate servo 1 to position 500 in 1000ms)
time.sleep(1) # 延时1s(delay for 1s)
getBusServoStatus(servo_id) # 读取总线舵机状态(read bus servo status)
 
