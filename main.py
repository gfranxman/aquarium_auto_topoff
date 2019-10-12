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

# for the relays
p13 = Pin(13, Pin.OUT)
p13.off()

p15 = Pin(15, Pin.OUT)
p15.off()

relay_1 = p13
relay_2 = p15

top_float_switch = p4
bottom_float_switch = p5

fresh_pump = p0
dirty_pump = p2

print("p4 = top switch")
print("p5 = bottom switch")
print("p13 = r1 = fill pump")
print("p15 = r2 = drain pump")

IDLE = -1
DRAINING = 0
FILLING = 1

mode = IDLE
top = True
bottom = True

last_top = top
last_bottom = bottom

top_went_high = False
top_went_low = False

bottom_went_high = False
bottom_went_low = False


def read_switches():
    global top, last_top, top_went_high, top_went_low
    global bottom, last_bottom, bottom_went_high, bottom_went_low


    top = top_float_switch.value()
    bottom = bottom_float_switch.value()

    if top and not last_top:
        top_went_high = True
        top_wwent_low = False
    elif last_top and not top:
        top_went_low = True
        top_went_high = False
    last_top = top

    if bottom and not last_bottom:
        bottom_went_high = True
        bottom_went_low = False
    elif last_bottom and not bottom:
        bottom_went_low = True
        bottom_went_high = False
    last_bottom = bottom


def print_mode():
    global mode
    if mode == IDLE:
        print("IDLE")
    elif mode == DRAINING:
        print("DRAINING")
    elif mode == FILLING:
        print("FILLING")
    else:
        print("BAD MODE:" + str(mode))

def set_mode(new_mode):
    global mode
    global top_went_high, top_went_low, bottom_went_high, bottom_went_low

    mode = new_mode
    if mode == IDLE:
        print("changing to IDLE, relays off")
        fresh_pump.on()
        relay_1.off()

        dirty_pump.on()
        relay_2.off()

    elif mode == DRAINING:
        print("changing to DRAINING, r1 OFF, r2 ON")
        fresh_pump.on()
        relay_1.off()

        dirty_pump.off()
        relay_2.on()

    elif mode == FILLING:
        print("changing to FILLING, r1 ON, r2 OFF")
        fresh_pump.off()  # ON
        relay_1.on()

        dirty_pump.on()
        relay_2.off()

    else:
        print("BAD MODE:" + str(mode))

    clear_transitions()


def clear_transitions():
    global top_went_high, top_went_low, bottom_went_high, bottom_went_low
    top_went_high = False
    top_went_low = False
    bottom_went_high = False
    bottom_went_low = False


def tick(t):
    global mode, top_went_high, top_went_low, bottom_went_high, bottom_went_low
    global top, bottom

    read_switches()

    if top_went_low and bottom:
        set_mode(DRAINING)

    elif bottom_went_low and not top:
        set_mode(FILLING)

    if top and mode == FILLING:
        set_mode(IDLE)

    if top and not bottom:
        print("error -- top is floating, but bottom is sinking")
        set_mode(IDLE)

    #print_mode()

rt.init(period=1000, mode=Timer.PERIODIC, callback=tick)

