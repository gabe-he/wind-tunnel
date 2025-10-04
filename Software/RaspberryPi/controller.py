import model as Model
from model import model

import threading
import time

demo = 0

from servo.Servo import Servo
from force.Force import Force
import time

def task():
    servo = None
    while True:
        if demo == 1:
            model["tilt_cur"] += 1
            model["lift_newton"] += 1
            model["drag_newton"] += 1
        else:
            # init
            if model["tilt_status"] == 0:
                servo = Servo("/dev/ttyUSB0")
                ret = servo.open()
                if ret == None:
                    model["tilt_status"] = 2
                else:
                    model["tilt_status"] = 1
            if model["tilt_status"] != 1:
                # Do nothing if fail
                continue

            if model["lift_status"] == 0:
                force = Force("/dev/ttyACM0")
                model["lift_status"] = force.get_status()
            if model["lift_status"] != 1:
                # Do nothing if fail
                continue

            # calc Servo Motor
            model["tilt_raw"] = servo.get_pos()
            #print(f'pos: {pos}')
            # 500: 0deg
            # 1000: 120deg
            # 0: -120deg
            model["tilt_cur"] = int((model["tilt_raw"] - model["tilt_tare"]) * 120 / 500) * -1

            #calc Lift/Drag
            model["lift0_raw"] = force.get_v(0)
            model["lift1_raw"] = force.get_v(1)
            #model["lift_raw"] = model["lift0_raw"] + model["lift1_raw"]
            model["lift_raw"] = model["lift1_raw"]
            model["lift_newton"] = Model.lift_raw_to_newton(model["tilt_cur"], model["lift_raw"])

            model["drag_raw"] = force.get_v(2)
            model["drag_newton"] = Model.drag_raw_to_newton(model["tilt_cur"], model["drag_raw"])

            # set new tilt
            if model["tilt_set"] == 1:
                servo.set_pos(None, int(((model["tilt_to"]*-1) * 500 / 120) + model["tilt_tare"]))
                model["tilt_set"] = 0

        # sleep one second
        time.sleep(1)

def run():
    task_thread = threading.Thread(target=task, daemon=True)
    task_thread.start()
