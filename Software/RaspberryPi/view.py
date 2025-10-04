import tkinter as tk
import tkinter.font as Font
import matplotlib as plot
import time
import json
from functools import partial

import model as Model
from model import model

ScanBtnTxt="Scan & Draw Tilt-Lift Graph"

def run():
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry("1280x720")

    def on_escape(event):
        root.destroy()

    global help_press_time
    help_press_time = 0
    def help_press(event):
        global help_press_time
        help_press_time = time.time()

    def help_release(event):
        if time.time() - help_press_time >= 3:
            root.destroy()

    def save_status():
        data = {
            "tilt": model["tilt_cur"],
            "lift": model["lift_newton"],
            "drag": model["drag_newton"]
            }
        model["records"].append(data)

    def tare_add():
        global tare_config
        if "lift_tare" not in tare_config:
            tare_config["lift_tare"] =  []
        if "drag_tare" not in tare_config:
            tare_config["drag_tare"] =  []
        lift_data = {
            "tilt": model["tilt_cur"],
            "force": model["lift_raw"]
            }
        tare_config["lift_tare"].append( lift_data )
        drag_data = {
            "tilt": model["tilt_cur"],
            "force": model["drag_raw"]
            }
        tare_config["drag_tare"].append( drag_data )

    def reset():
        model["records"] = []

    def update_tilt(value):
        model["tilt_to"] = int(value)
        model["tilt_set"] = 1

    global autotest, autotest_tilt, autotest_delay
    global tilt_min, tilt_max
    global tilt_display_min, tilt_display_max

    autotest = 0 # 0: not start, 1: auto test, 2: tare
    tilt_min = -70
    tilt_max = 70
    tilt_display_min = -75
    tilt_display_max = 75

    global tare_config
    tare_config = {}

    def resetAllBt_update():
        if autotest != 2:
            resetAllBt.config(text="TARE\n(Admin only, FAN off)", bg="#b3b3b3")
        else:
            resetAllBt.config(text="TARE" + "." * (autotest_delay + 1), bg=resetAllBt.cget("bg"), activebackground=resetAllBt.cget("activebackground"))

    def autoBt_update():
        if autotest != 1:
            autoBt.config(text=ScanBtnTxt, bg=autoBt.cget("bg"), activebackground=autoBt.cget("activebackground"))
        else:
            autoBt.config(text=ScanBtnTxt + "." * (autotest_delay + 1), bg=autoBt.cget("bg"), activebackground=autoBt.cget("activebackground"))

    def tare():
        global autotest, autotest_tilt, autotest_delay
        global tilt_min, tilt_max

        if autotest == 1:
            autotest = 0
        elif autotest == 2:
            autotest = 0
        else:
            tare_config = {}
            autotest_tilt = tilt_min # start tilt
            autotest_delay = 0
            autotest = 2
        resetAllBt_update()
        autoBt_update()


    def autotest_start():
        global autotest, autotest_tilt, autotest_delay
        global tilt_min, tilt_max
        if autotest == 1:
            autotest = 0
        elif autotest == 2:
            autotest = 0
        else:
            reset()
            autotest_tilt = tilt_min # start tilt
            autotest_delay = 0
            autotest = 1
        resetAllBt_update()
        autoBt_update()

    root.bind("<Escape>", on_escape)

    myFont = Font.Font(family = "Arial", size = 40, weight = "bold")
    smallfontBt = Font.Font(family = "Arial", size = 12, weight = "normal")
    tiltfontBt = Font.Font(family = "Arial", size = 14, weight = "bold")
    fontBt = Font.Font(family = "Arial", size = 20, weight = "bold")
    fontLabel = Font.Font(family = "Courier", size = 36, weight = "normal")
    fontStatus = Font.Font(family = "Arial", size = 18, weight = "normal")
    smallfontStatus = Font.Font(family = "Arial", size = 14, weight = "normal")
    fontGraph = Font.Font(family = "Courier", size = 24, weight = "bold")

    frame = tk.Frame(root)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    '''
    bt = tk.Button(frame, text="Quit", command=on_button_click)
    bt.place(x=400, y=400, width=100, height=100)
    '''

    #top section of the screen
    upperFrame = tk.Frame(frame)
    upperFrame.place(x=0, y=0, width=1280, height=80)

    #top horizontal line
    canvas = tk.Canvas(upperFrame, bg="black")
    canvas.place(x=0, y=70 ,width=1280, height=10)

    helpBt = tk.Button(upperFrame, text="HELP", font = smallfontBt, bg = "#B3B3B3")
    helpBt.place(x=10, y=10, width=200, height=60)
    helpBt.bind("<ButtonPress-1>", help_press)
    helpBt.bind("<ButtonRelease-1>", help_release)

    resetAllBt = tk.Button(upperFrame, text="TARE", font = smallfontBt,  bg = "#B3B3B3", command = tare)
    resetAllBt.place(x=1050, y=10, width=220, height = 60)
    resetAllBt_update()

    #right side from under the top line to the bottom
    rightFrame = tk.Frame(frame)
    rightFrame.place(x = 700, y = 80, width = 580, height = 640)

    statsLb = tk.Label(rightFrame, text = "REAL TIME STATUS", font = myFont)
    statsLb.place(x = 20, y = 0, width = 550, height = 100)

    tiltLb = tk.Label(rightFrame, text = "Tilt: ___", font = fontLabel, anchor = "w")
    tiltLb.place(x = 140, y =  110, width = 510, height = 50)

    liftLb = tk.Label(rightFrame, text = "Lift: ___", font = fontLabel, anchor = "w")
    liftLb.place(x = 140, y =  160, width = 510, height = 50)

    dragLb = tk.Label(rightFrame, text = "Drag: ___", font = fontLabel, anchor = "w")
    dragLb.place(x = 140, y =  210, width = 510, height = 50)

    tiltScaleLb = tk.Label(rightFrame, text = "Tilt: ", font = fontLabel, anchor = "w")
    tiltScaleLb.place(x = 20, y = 275, width = 120, height = 50)

    liftStatusLb = tk.Label(rightFrame, text = "LIFT STATUS: ", font = fontStatus, anchor = "e")
    liftStatusLb.place(x = 20, y = 570, width = 250, height = 40)

    liftConnectedLb = tk.Label(rightFrame, text = "NOT CONNECTED", font = fontStatus, anchor = "w", fg = "red")
    liftConnectedLb.place(x = 300, y = 570, width = 250, height = 40)

    motorStatusLb = tk.Label(rightFrame, text = "MOTOR STATUS: ", font = fontStatus, anchor = "e")
    motorStatusLb.place(x = 20, y = 600, width = 250, height = 40)

    motorConnectedLb = tk.Label(rightFrame, text = "NOT CONNECTED", font = fontStatus, anchor = "w", fg = "red")
    motorConnectedLb.place(x = 300, y = 600, width = 250, height = 40)

    global scale_update_delay
    scale_update_delay = 0
    def on_scale_release(event):
        global scale_update_delay
        update_tilt(tiltScale.get())
        scale_update_delay = 4

    def on_scale_press(event):
        global scale_update_delay
        scale_update_delay = 10

    tiltScale = tk.Scale(rightFrame, from_ =tilt_min, to = tilt_max, orient = tk.HORIZONTAL, width = 100)
    tiltScale.place(x = 140, y = 250, width = 420, height = 80)
    tiltScale.bind("<ButtonPress-1>", on_scale_press)
    tiltScale.bind("<ButtonRelease-1>", on_scale_release)

    #tiltGoBt = tk.Button(rightFrame, text = "GO", font = fontBt)
    #tiltGoBt.place(x = 450, y = 370, width = 100, height = 50)

    def tiltset(angle):
        update_tilt(angle)

    # -60, -40, -20, 0, 20, 40, 60
    for i in range(7):
        tk.Button(rightFrame, text = f'{i*20-60}', font = tiltfontBt, command = partial(tiltset, i*20-60), bg='light blue', activebackground="light blue").place(x = 30+i*75, y = 340, width = 70, height = 50)
    # -50, -30, -10, 10, 30, 50
    for i in range(6):
        tk.Button(rightFrame, text = f'{i*20-50}', font = tiltfontBt, command = partial(tiltset, i*20-50), bg='light blue', activebackground="light blue").place(x = 72+i*75, y = 390, width = 70, height = 50)

    autoBt = tk.Button(rightFrame, text = ScanBtnTxt, font = fontBt, command = autotest_start)
    autoBt.place(x = 100, y = 460, width = 390, height = 60)
    autoBt_update()
    tk.Label(rightFrame, text = "Set Fan Speed >= 10 to get better Graph", font = smallfontStatus, anchor = "w").place(x = 120, y = 520, width = 500, height = 30)

    #vertical line
    canvas = tk.Canvas(rightFrame, bg="black")
    canvas.place(x=0, y=0 ,width=10, height=630)

    #2nd horizontal line
    canvas = tk.Canvas(rightFrame, bg = "black")
    canvas.place(x = 10, y = 90, width = 560, height = 8)

    #3rd horizontal line
    #canvas = tk.Canvas(rightFrame, bg="black")
    #canvas.place(x=10, y=340 ,width=560, height=10)

    #4th horizontal line
    canvas = tk.Canvas(rightFrame, bg="black")
    canvas.place(x=10, y=550 ,width=560, height=10)

    #left side from under the top line to the bottom
    leftFrame = tk.Frame(frame)
    leftFrame.place(x = 0, y = 80, width = 700, height = 660)


    tk_image = tk.PhotoImage(file="./record_background.png")
    record_canvas = tk.Canvas(leftFrame)
    record_canvas.place(x=0, y=0 ,width=700, height=560)
    RECORD_CURVE_WIDTH=550
    RECORD_CURVE_HEIGHT=500 # leave some space to draw the x/y axis label

    def save_graph():
        if "records" not in model or len(model["records"]) < 2:
            return
        try:
            with open('save.json', 'w') as f:
                json.dump(model["records"], f, indent=4)
        except Exception as e:
            print(f'ERROR: write save.json fail')

    def load_graph():
        try:
            with open('save.json', 'r') as f:
                records = json.load(f)
                if len(records) < 1:
                    return
                model["records"] = records
        except Exception as e:
            pass

    if "lift_tare" not in model or len(model["lift_tare"]) < 1:
        print(f'WARNING: init lift tare with default')
        model["lift_tare"] = model["lift_tare_default"]
        pass

    saveBt = tk.Button(leftFrame, text = "Save\n(admin only)", font = smallfontBt, command = save_graph)
    saveBt.place(x = 50, y = 560, width = 100, height = 50)

    restoreBt = tk.Button(leftFrame, text = "LOAD", font = smallfontBt, command = load_graph)
    restoreBt.place(x = 200, y = 560, width = 150, height = 50)

    resetBt = tk.Button(leftFrame, text = "RESET", font = smallfontBt, command = reset)
    resetBt.place(x = 400, y = 560, width = 150, height = 50)

    def update():
        global autotest, autotest_tilt, autotest_delay
        global tilt_display_min, tilt_display_max
        # auto test
        if autotest > 0:
            # set tilt when delay is 0
            if autotest_delay == 0:
                if autotest_tilt > tilt_max:
                    if autotest == 2:
                        global tare_config
                        Model.update_tare( tare_config )
                        autotest = 0 # stop autotest
                        resetAllBt_update()
                    elif autotest == 1:
                        autotest = 0 # stop autotest
                        autoBt_update()
                else:
                    # update tilt
                    update_tilt(autotest_tilt)
                    autotest_tilt += 5 # next tilt increase 5 deg
                autotest_delay += 1
            # record value after 5 seconds
            elif autotest_delay >= 5:
                if autotest == 1:
                    save_status()
                elif autotest == 2:
                    tare_add()
                autotest_delay = 0
            else:
                autotest_delay += 1

            if autotest == 2:
                resetAllBt_update()
            if autotest == 1:
                autoBt_update()

        # update tilt label
        #tiltLb.config(text='Tilt: ' + tiltInput)
        tiltLb.config(text = f'Tilt: {model["tilt_cur"]:d}')
        #liftLb.config(text = f'Lift: {model["lift_raw"]:.2f}')
        #dragLb.config(text = f'Drag: {model["drag_raw"]:.2f}')
        liftLb.config(text = f'Lift: {model["lift_newton"]:.2f}')
        dragLb.config(text = f'Drag: {model["drag_newton"]:.2f}')

        global scale_update_delay
        if scale_update_delay > 0 and scale_update_delay < 10:
            scale_update_delay -= 1
        if scale_update_delay == 0:
            tiltScale.set(model["tilt_cur"])

        # updata status
        status_text=[ "NOT CONNECTED", "CONNECTED", "NOT FOUND", "ERROR" ]
        status_color=[ "orange", "green", "red", "red" ]
        liftConnectedLb.config(text = status_text[model["lift_status"]], fg = status_color[model["lift_status"]])
        motorConnectedLb.config(text = status_text[model["tilt_status"]], fg = status_color[model["tilt_status"]])

        # draw record_canvas
        record_canvas.delete("all")

        # update background
        record_canvas.create_image(0, 0, image=tk_image, anchor = 'nw')

        # TODO: calc the min/max of lift/drag, here just hard coded from test data
        if len(model["records"]) > 0:
            y_min = -2
            y_max = 2
            liftGraph = []
            dragGraph = []
            for rec in model["records"]:
                p_x = int(RECORD_CURVE_WIDTH * (rec["tilt"] - tilt_display_min) / (tilt_display_max - tilt_display_min) + 100)
                p_y = int(RECORD_CURVE_HEIGHT * (y_max - rec["lift"]) / (y_max - y_min)) # y from top down, so use lift_max - rec["lift"], because lift_max is Y=0
                liftGraph.append(p_x)
                liftGraph.append(p_y)
            if len(liftGraph) == 2:
                record_canvas.create_oval(p_x - 1, p_y - 1, p_x + 1, p_y + 1, fill = "red", outline = "red")
            else:
                record_canvas.create_line(liftGraph, fill="red", width=2, smooth=True)

            for rec in model["records"]:
                p_x = int(RECORD_CURVE_WIDTH * (rec["tilt"] - tilt_display_min) / (tilt_display_max - tilt_display_min) + 100)
                p_y = int(RECORD_CURVE_HEIGHT * (y_max - rec["drag"]) / (y_max - y_min)) # y from top down, so use lift_max - rec["lift"], because lift_max is Y=0
                dragGraph.append(p_x)
                dragGraph.append(p_y)
            if len(dragGraph) == 2:
                record_canvas.create_oval(p_x - 1, p_y - 1, p_x + 1, p_y + 1, fill = "blue", outline = "blue")
            else:
                record_canvas.create_line(dragGraph, fill="blue", width=2, smooth=True)


        # update again after 1s
        root.after(1000, update)

    update()

    root.mainloop()
