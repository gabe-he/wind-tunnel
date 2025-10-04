import _thread
from machine import I2C, Pin, Timer, PWM
from I2C_LCD import I2CLcd
from hx711 import *
import time

# init LCD
lcd_en = True
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
devices = i2c.scan()
if devices == []:
    lcd_en = False
else:
    lcd = I2CLcd(i2c, devices[0], 4, 20)
    #lcd.move_to(0, 1)
    #lcd.putstr("Hello, world!")

# init LoadCells
hxs = [
    {
        "pin_clk" : 7,
        "pin_dat" : 6
    },
    {
        "pin_clk" : 10,
        "pin_dat" : 9
    },
    {
        "pin_clk" : 13,
        "pin_dat" : 11
    }
]
for hx_idx in range(len(hxs)):
    hx = hx711(Pin(hxs[hx_idx]["pin_clk"]), Pin(hxs[hx_idx]["pin_dat"]), hx_idx)
    hx.set_power(hx711.power.pwr_up)
    hx.set_gain(hx711.gain.gain_128)
    hx.set_power(hx711.power.pwr_down)
    hx711.wait_power_down()
    hx.set_power(hx711.power.pwr_up)
    hx711.wait_settle(hx711.rate.rate_10)
    hx.active(0)
    hxs[hx_idx]["hx"] = hx

# init LED
led_status = Pin(25, machine.Pin.OUT)
led_on = True
led_status.high()

while True:
    # get all result
    for hx_idx in range(len(hxs)):
        hx = hxs[hx_idx]["hx"]
        hx.active(1)
        hxs[hx_idx]["v"] = hx.get_value()
        hx.active(0)
    if lcd_en:
        # print result in LCD
        for hx_idx in range(len(hxs)):
            lcd.move_to(0, hx_idx)
            lcd.putstr(str(hxs[hx_idx]["v"]))
    # print result in console
    for hx_idx in range(len(hxs)):
        print(hxs[hx_idx]["v"])
    time.sleep(0.5)
    # toggle LED
    if led_on:
        led_status.low()
        led_on = False
    else:
        led_status.high()
        led_on = True

