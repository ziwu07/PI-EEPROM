from gpiozero import DigitalInputDevice, DigitalOutputDevice
from EEPROM_INFO import *
from time import sleep

ce = DigitalOutputDevice(pin=CE_PIN, active_high=False)
we = DigitalOutputDevice(pin=WE_PIN, active_high=False)
oe = DigitalOutputDevice(pin=OE_PIN, active_high=False)

io: list[DigitalInputDevice] = list()
adr: list[DigitalOutputDevice] = list()
for pin in IO_PINS:
    io.append(DigitalInputDevice(pin=pin, pull_up=False))
for pin in ADDR_PINS:
    adr.append(DigitalOutputDevice(pin=pin))

adr1 = int(input("0x"), 16)
adr2 = int(input("0x"), 16)

if (adr1 > 0x8000 or adr2 > 0x8000) or (adr1 < 0x0000 or adr2 < 0x0000):
    print(adr1, adr2)
    exit()
sleep(0.1)
for cadr in range(adr1, adr2):
    for i in range(15):
        adr[i].value = (cadr >> i) & 1
    ce.on()
    oe.on()
    sleep(0.0000002)
    result = 0
    for i in range(8):
        result |= io[i].value << i
    oe.off()
    ce.off()
    print(f"{hex(cadr):<7} {bin(result):<11} {hex(result)}")
