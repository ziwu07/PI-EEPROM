from gpiozero import DigitalInputDevice, DigitalOutputDevice
from EEPROM_INFO import *
from time import sleep
import sys, os

ce = DigitalOutputDevice(pin=CE_PIN, active_high=False)
we = DigitalOutputDevice(pin=WE_PIN, active_high=False)
oe = DigitalOutputDevice(pin=OE_PIN, active_high=False)

io: list[DigitalInputDevice] = list()
adr: list[DigitalOutputDevice] = list()
for pin in IO_PINS:
    io.append(DigitalInputDevice(pin=pin, pull_up=False))
for pin in ADDR_PINS:
    adr.append(DigitalOutputDevice(pin=pin))

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = input("file:")

if sys.argv[1] == "--":
    file = sys.stdout.buffer
else:
    file = open(file_name, "wb")
byte_arr = bytearray(EEPROM_SIZE)
sleep(0.1)
for cadr in range(0, EEPROM_SIZE):
    for i in range(15):
        adr[i].value = (cadr >> i) & 1
    ce.on()
    oe.on()
    sleep(0.0000002)
    result = 0
    for i in range(8):
        result |= io[i].value << i
    byte_arr[cadr] = result
    oe.off()
    ce.off()
    sleep(0.0000002)
file.write(byte_arr)
file.close()
