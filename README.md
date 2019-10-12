# Makefile targets to use during development
##   to flash it with new firmware:

`
$ make reflash
`

## Edit main.py then put the new code on the board:

`$ make put
`

### then connect like:

`$ make connect 
ctl-A ctl-D` 

### to disconnect

`ctl-ADD` to detach and disconnect

## then you can:

`$ make reconnect`

## or disconnect the session

`$ make disconnect`

## to disable it while it is running, attach then:
`
import os
os.remove('main.py')
or
or.rename('main.py', 'old_main.py')
`

# Hardware
## Board
Adafruit Feather Huzzah esp-8266  https://learn.adafruit.com/adafruit-feather-huzzah-esp8266/overview

## Relays
Adafruit Non-Latching Mini Relay FeatherWing PRODUCT ID: 2895  https://www.adafruit.com/product/2895

## Float switches

## Pumps


