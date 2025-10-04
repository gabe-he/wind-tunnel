import json
import os

# default model value
model = {
    "lift0_raw": 0, # lift0 current raw video from sensor, updated by controller
    "lift1_raw": 0, # lift1 current raw video from sensor, updated by controller
    "lift_raw" : 0, # lift0_raw + lift1_raw, updated by controller
    "lift_tare_default": [ # lift0 + lift1 tare number, updated by view
        { "tilt": 0,
          "force": -10900
        }
    ],
    "lift_per_newton": 8860, # how many lift in one newton, constant value
    "lift_newton" : 0.0, # current lift in newton, updated by controller, shown in view
    "drag_raw": 0, 
    "drag_tare_default" : [
        { "tilt": 0,
          "force": -260500
        }
    ],
    "drag_per_newton": 16320, # how many drag in one newton
    "drag_newton": 0, # drag in newton
    "tilt_cur": 0, # current tile angle, -90 ~ 90
    "tilt_to": 0, # set to new tilt, -90 ~ 90
    "tilt_set": 0, # View set to 1 to let Controller do tilt update. Controller set to 0 after finish.
    "tilt_tare": 500,
    "tilt_raw":0,
    # 0: "NOT CONNECTED": initial status, not started
    # 1: "CONNECTED": connected and works well
    # 2: "NOT FOUND": open the device fail
    # 3: "ERROR": device found but not working well
    "lift_status": 0,
    "tilt_status": 0,
    "records": [
    ]
}

def init():
    global model
    try:
        # load config.json into dict
        with open('config.json', 'r') as f:
            config = json.load(f)
            if "lift_tare" in config:
                model["lift_tare"] = config["lift_tare"]
            if "drag_tare" in config:
                model["drag_tare"] = config["drag_tare"]
    except Exception as e:
        pass

    if "lift_tare" not in model or len(model["lift_tare"]) < 1:
        print(f'WARNING: init lift tare with default')
        model["lift_tare"] = model["lift_tare_default"]
    if "drag_tare" not in model or len(model["drag_tare"]) < 1:
        print(f'WARNING: init drag tare with default')
        model["drag_tare"] = model["drag_tare_default"]

def update_tare(config):
    global model
    # update current
    if "lift_tare" not in config or len(config["lift_tare"]) < 1:
        print(f'ERROR: update_tare param lift_tare error')
        return
    if "drag_tare" not in config or len(config["drag_tare"]) < 1:
        print(f'ERROR: update_tare param drag_tare error')
        return
    
    # update model
    model["lift_tare"] = config["lift_tare"]
    model["drag_tare"] = config["drag_tare"]

    # save to config.json
    try:
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f'ERROR: write config.json fail')
        pass

def raw_to_newton(tilt, raw, tare, per_newton):
    if len(tare) == 1:
        t = tare[0]["force"]
    elif tilt <= tare[0]["tilt"]:
        t = tare[0]["force"]
    elif tilt >= tare[-1]["tilt"]:
        t = tare[-1]["force"]
    else:
        for i in range(1, len(tare)):
            if tilt <= tare[i]["tilt"]:
                if tare[i]["tilt"] - tare[i-1]["tilt"] == 0:
                    t = tare[i]["force"]
                else:
                    t = ((tilt - tare[i-1]["tilt"]) * tare[i]["force"] + (tare[i]["tilt"] - tilt) * tare[i-1]["force"]) / (tare[i]["tilt"] - tare[i-1]["tilt"])
                break

    newton = (raw - t) / per_newton
    #print(f'[DEBUG] {raw} -> {newton}, tilt {tilt}, t {t} ')
    return newton

def lift_raw_to_newton(tilt, raw):
    if "lift_tare" not in model or len(model["lift_tare"]) < 1:
        print(f'model["lift_tare"] not exist')
        return raw
    return raw_to_newton(tilt, raw, model["lift_tare"], model["lift_per_newton"])

def drag_raw_to_newton(tilt, raw):
    if "drag_tare" not in model or len(model["drag_tare"]) < 1:
        print(f'model["drag_tare"] not exist')
        return raw
    return raw_to_newton(tilt, raw, model["drag_tare"], model["drag_per_newton"])
