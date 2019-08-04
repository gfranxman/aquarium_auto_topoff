
.PHONY: reflash
reflash:
	esptool.py --port /dev/cu.SLAB_USBtoUART erase_flash
	esptool.py --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 esp8266-20190529-v1.11.bin 
    

.PHONY: connect
connect:
	screen -L /dev/cu.SLAB_USBtoUART 115200 -L 

.PHONY: reconnect
reconnect:
	screen -r

.PHONY: ls
ls:
	ampy -p /dev/cu.SLAB_USBtoUART ls

.PHONY:put
put: reset
	ampy -p /dev/cu.SLAB_USBtoUART put main.py

.PHONY: reset
reset:
	ampy -p /dev/cu.SLAB_USBtoUART reset

