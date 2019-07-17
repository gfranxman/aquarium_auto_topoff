from machine import Pin
from machine import Timer

rt = Timer(-1)
rt.deinit() # turn off current timers

p0 = Pin(0, Pin.OUT)
p0.off()  # red light on

p2 = Pin(2, Pin.OUT)
p2.off()   # blue light on

p4 = Pin(4, Pin.IN, Pin.PULL_UP)  # p4 with internal pull resister
p5 = Pin(5, Pin.IN, Pin.PULL_UP)  # p5 with internal pull resister

# up is 1, down is 0  for the float switches

top_float_switch = p4
bottom_float_switch = p5

fresh_pump = p0
dirty_pump = p2



DRAINING = 0
FILLING = 1

mode = DRAINING

def tick(t):
    global mode
    top = top_float_switch.value()
    bottom = bottom_float_switch.value()

    if top:
        if bottom:
            fresh_pump.on()
            dirty_pump.on()
            mode = DRAINING  # next for next time we are between states
        else:
            print("error -- top is floating, but bottom is sinking")

    else:
        if bottom:
            # keep filling or draining
            print("mode:" + str(mode))
            if mode == DRAINING:
                print("draining")
                fresh_pump.on()
                dirty_pump.off()  # keep draining
            else:
                print("filling")
                fresh_pump.off()
                dirty_pump.on()

        else:
           # top and bottom have sunk.
           # time to decide if we are filling or draining
           mode = FILLING
           fresh_pump.off()  # ON
           dirty_pump.on()


rt.init(period=1000, mode=Timer.PERIODIC, callback=tick)

    
