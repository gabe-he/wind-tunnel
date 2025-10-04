#!/usr/bin/env python3
# encoding: utf-8
import time
import ctypes
import serial

LOBOT_SERVO_FRAME_HEADER         = 0x55
LOBOT_SERVO_MOVE_TIME_WRITE      = 1
LOBOT_SERVO_MOVE_TIME_READ       = 2
LOBOT_SERVO_MOVE_TIME_WAIT_WRITE = 7
LOBOT_SERVO_MOVE_TIME_WAIT_READ  = 8
LOBOT_SERVO_MOVE_START           = 11
LOBOT_SERVO_MOVE_STOP            = 12
LOBOT_SERVO_ID_WRITE             = 13
LOBOT_SERVO_ID_READ              = 14
LOBOT_SERVO_ANGLE_OFFSET_ADJUST  = 17
LOBOT_SERVO_ANGLE_OFFSET_WRITE   = 18
LOBOT_SERVO_ANGLE_OFFSET_READ    = 19
LOBOT_SERVO_ANGLE_LIMIT_WRITE    = 20
LOBOT_SERVO_ANGLE_LIMIT_READ     = 21
LOBOT_SERVO_VIN_LIMIT_WRITE      = 22
LOBOT_SERVO_VIN_LIMIT_READ       = 23
LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE = 24
LOBOT_SERVO_TEMP_MAX_LIMIT_READ  = 25
LOBOT_SERVO_TEMP_READ            = 26
LOBOT_SERVO_VIN_READ             = 27
LOBOT_SERVO_POS_READ             = 28
LOBOT_SERVO_OR_MOTOR_MODE_WRITE  = 29
LOBOT_SERVO_OR_MOTOR_MODE_READ   = 30
LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE = 31
LOBOT_SERVO_LOAD_OR_UNLOAD_READ  = 32
LOBOT_SERVO_LED_CTRL_WRITE       = 33
LOBOT_SERVO_LED_CTRL_READ        = 34
LOBOT_SERVO_LED_ERROR_WRITE      = 35
LOBOT_SERVO_LED_ERROR_READ       = 36

class ServoCmd:
    def __init__(self, port):
        self.port = port
        self.handle = None

    def open(self):
        if self.handle is not None:
            return self.handle
        self.handle = serial.Serial(self.port, 115200)
        return self.handle

    def close(self):
        if self.handle != None:
            self.handle.close()
            self.handle = None

    def checksum(self, buf):
        sum = 0x00
        for b in buf:
            sum += b
        sum = sum - 0x55 - 0x55  # remove the first two 0x55 of a command
        sum = ~sum  # bitwise
        return sum & 0xff

    def write(self, id=None, w_cmd=None, dat1=None, dat2=None):
        '''
        :param id:
        :param w_cmd:
        :param dat1:
        :param dat2:
        :return:
        '''
        buf = bytearray(b'\x55\x55')  # frame header
        buf.append(id)
        # command length
        if dat1 is None and dat2 is None:
            buf.append(3)
        elif dat1 is not None and dat2 is None:
            buf.append(4)
        elif dat1 is not None and dat2 is not None:
            buf.append(7)

        buf.append(w_cmd)  # command
        # write data
        if dat1 is None and dat2 is None:
            pass
        elif dat1 is not None and dat2 is None:
            buf.append(dat1 & 0xff)  # deviation
        elif dat1 is not None and dat2 is not None:
            # # split a 16-bit integer into its low 8 bits and high 8 bits
            buf.extend([(0xff & dat1), (0xff & (dat1 >> 8))])
            buf.extend([(0xff & dat2), (0xff & (dat2 >> 8))])
        # checksum
        buf.append(self.checksum(buf))
        # for i in buf:
        #     print('%x' %i)
        self.handle.write(buf)  # send

    def read_cmd(self, id=None, r_cmd=None):
        '''
        :param id:
        :param r_cmd:
        :param dat:
        :return:
        '''
        buf = bytearray(b'\x55\x55')  # frame header
        buf.append(id)
        buf.append(3)  # command length
        buf.append(r_cmd)  # command
        buf.append(self.checksum(buf))  # checksum
        self.handle.write(buf)  # send
        time.sleep(0.00034)

    def get_rmsg(self, cmd):
        '''
        :param cmd
        :return:
        '''
        self.handle.flushInput()  # clear received chach        
        time.sleep(0.005)  # Delay for a while and wait the reception to complete
        count = self.handle.inWaiting()    # get the number of bytes in the received buffer
        if count != 0:  # if the received data is not empty
            recv_data = self.handle.read(count)  # read the received data
            # for i in recv_data:
            #     print('%#x' %ord(i))
            # if it is the command for reading ID
            try:
                if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[4] == cmd:
                    dat_len = recv_data[3]
                    self.handle.flushInput()  # clear received chach
                    if dat_len == 4:
                        # print ctypes.c_int8(ord(recv_data[5])).value    # convert a byte string to a signed integer
                        return recv_data[5]
                    elif dat_len == 5:
                        pos = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                        return ctypes.c_int16(pos).value
                    elif dat_len == 7:
                        pos1 = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                        pos2 = 0xffff & (recv_data[7] | (0xff00 & (recv_data[8] << 8)))
                        return ctypes.c_int16(pos1).value, ctypes.c_int16(pos2).value
                else:
                    return None
            except BaseException as e:
                print(e)
        else:
            self.handle.flushInput()  # clear received chach
        return None

    def read(self, id, cmd):
        self.read_cmd(id, cmd)
        return self.get_rmsg(cmd)

class Servo:
    def __init__(self, port):
        self.servocmd = ServoCmd(port)
        self.id = None
        self.retry = 3

    def open(self):
        if self.servocmd.open() is None:
            return None
        return self.servocmd

    def get_id(self):
        if self.id is None:
            for i in range(self.retry):
                msg = self.servocmd.read(0xfe, LOBOT_SERVO_ID_READ)
                if msg is not None:
                    self.id = msg
                    return msg
            return None
        else:
            return self.id
        return self.id

    def get_pos(self, id=None):
        if id is None:
            if self.id is None:
                self.id = self.get_id()
            id = self.id
        for i in range(self.retry):
            msg = self.servocmd.read(id, LOBOT_SERVO_POS_READ)
            if msg is not None:
                return msg
        return None

    def set_pos(self, id=None, pos=500, use_time=1000):
        if id is None:
            if self.id is None:
                self.id = self.get_id()
            id = self.id
        self.servocmd.write(id, LOBOT_SERVO_MOVE_TIME_WRITE, pos, use_time)

    def get_tmp(self, id=None):
        if id is None:
            if self.id is None:
                self.id = self.get_id()
            id = self.id
        for i in range(self.retry):
            msg = self.servocmd.read(id, LOBOT_SERVO_TEMP_READ)
            if msg is not None:
                return msg
        return None

    def get_vin(self, id=None):
        if id is None:
            if self.id is None:
                self.id = self.get_id()
            id = self.id
        for i in range(self.retry):
            msg = self.servocmd.read(id, LOBOT_SERVO_VIN_READ)
            if msg is not None:
                return msg
        return None
