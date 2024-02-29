from gpiozero import DigitalInputDevice, DigitalOutputDevice
from pinout import *
from time import sleep

ce = DigitalOutputDevice(pin=ce_pin, active_high=False)
we = DigitalOutputDevice(pin=we_pin, active_high=False)
oe = DigitalOutputDevice(pin=oe_pin, active_high=False)

io: list[DigitalInputDevice] = list()
adr: list[DigitalOutputDevice] = list()
for pin in io_pin_list:
    io.append(DigitalInputDevice(pin=pin, pull_up=False))
for pin in adr_pin_list:
    adr.append(DigitalOutputDevice(pin=pin))

var1 = int(input("0x"), 16)
var2 = int(input("0x"), 16)

if (var1 > 0x8000 or var2 > 0x8000) or (var1 < 0x0000 or var2 < 0x0000):
    print(var1, var2)
    exit()
sleep(0.1)
for cadr in range(var1, var2):
    for i in range(15):
        adr[i].value = (cadr >> i) & 1
    ce.on()
    sleep(0.00001)
    oe.on()
    sleep(0.00001)
    result = 0
    for i in range(8):
        result |= io[i].value << i
    oe.off()
    ce.off()
    print(f"{hex(cadr):<7} {bin(result):<11} {hex(result)}")
