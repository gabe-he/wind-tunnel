#!/usr/bin/env python3
# encoding: utf-8
import serial
import threading

class Force:
    def __init__(self, port):
        self.status = 0
        self.v0 = 0
        self.v1 = 0
        self.v2 = 0
        self.handle = serial.Serial(port, 115200, timeout=2)
        if self.handle == None:
            self.status = 2
        else:
            self.task_thread = threading.Thread(target=self.task, daemon=True)
            self.task_thread.start()
            self.status = 1

    def task(self):
        while True:
            try:
                data = self.handle.readline().decode('utf-8').strip()
                if data.startswith("0:"):
                    self.v0 = int(data[2:])
                elif data.startswith("1:"):
                    self.v1 = int(data[2:])
                elif data.startswith("2:"):
                    self.v2 = int(data[2:])
                #print(data)
            except Exception as e:
                self.status = 3
                break

    def get_status(self):
        return self.status

    def get_v(self, id):
        if id==0:
            return self.v0
        elif id==1:
            return self.v1
        elif id==2:
            return self.v2
        else:
            return 0
